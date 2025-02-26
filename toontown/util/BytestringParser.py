# taken from https://github.com/Toontown-Event-Horizon/evhutils/blob/master/src/evh_utils/BytestringParser.py
__all__ = ["ValueType", "StructValueType", "Packers", "migration", "BytestringParser"]


import abc
import dataclasses
import inspect
import struct
from io import BytesIO


class ValueType(abc.ABC):
    @abc.abstractmethod
    def getValue(self, io: BytesIO):
        pass

    @abc.abstractmethod
    def addValue(self, io: BytesIO, value):
        pass


class StructValueType(ValueType):
    def __init__(self, fmt):
        self.fmt = "!" + fmt  # ! enables network order
        self.bytelen = struct.calcsize(self.fmt)

    def getValue(self, io: BytesIO):
        byteInput = io.read(self.bytelen)
        assert len(byteInput) == self.bytelen
        return struct.unpack(self.fmt, byteInput)[0]

    def addValue(self, io: BytesIO, value):
        byteOutput = struct.pack(self.fmt, value)
        io.write(byteOutput)


class TupleValueType(ValueType):
    def __init__(self, *parsers):
        self.parsers = parsers

    def getValue(self, io: BytesIO):
        output = []
        for parser in self.parsers:
            output.append(parser.getValue(io))
        return tuple(output)

    def addValue(self, io: BytesIO, value):
        for parser, item in zip(self.parsers, value):
            parser.addValue(io, item)


class ConstantPacker(ValueType):
    def __init__(self, callback):
        self.callback = callback

    def getValue(self, io: BytesIO):
        return self.callback(None)

    def addValue(self, io: BytesIO, value):
        raise RuntimeError("ConstantPacker should not be used to write bytestrings!")


class Packers:
    uint8 = StructValueType("B")
    int8 = StructValueType("b")
    uint16 = StructValueType("H")
    int16 = StructValueType("h")
    uint32 = StructValueType("L")
    int32 = StructValueType("l")
    uint64 = StructValueType("Q")
    int64 = StructValueType("q")
    float32 = StructValueType("f")
    double64 = StructValueType("d")
    tuple = TupleValueType


@dataclasses.dataclass
class Migration:
    fromVersion: int
    convertedField: str
    added: bool = False
    removed: bool = False
    locatedAfter: str = ""

    callback = None
    oldParser = None

    def __call__(self, funcOrArg):
        if self.callback is None:
            self.callback = funcOrArg
            sig = inspect.signature(funcOrArg)
            if self.added:
                assert len(sig.parameters) == 1
            else:
                assert len(sig.parameters) == 2
                self.oldParser = list(sig.parameters.values())[1].default
            return self
        else:
            return self.callback(funcOrArg)


def migration(
    func=None,
    *,
    fromVersion: int = -1,
    convertedField: str = "",
    added: bool = False,
    removed: bool = False,
    locatedAfter: str = "",
):
    if added and removed:
        raise ValueError("A migration field cannot be both added and removed at the same time!")
    if bool(locatedAfter) != bool(removed):
        raise ValueError("Removed fields must include locatedAfter and other fields must not include locatedAfter!")

    convertedField = convertedField or func.__name__
    migrationObject = Migration(fromVersion, convertedField, added, removed, locatedAfter)
    if func is not None:
        migrationObject(func)
    return migrationObject


class SubclassWatcher(type):
    def __new__(cls, name, bases, classdict, version=None):
        result = type.__new__(cls, name, bases, classdict)
        result.setMembers(classdict, version)  # noqa
        return result


@dataclasses.dataclass(frozen=True)
class ParsingField:
    name: str
    active: bool
    packer: ValueType
    converters: tuple


class BytestringParser(metaclass=SubclassWatcher):
    _parsers = None
    _fields = None
    _version = False

    def __init__(self, *values):
        if len(values) != len(self._fields):
            raise ValueError(f"Invalid number of arguments: expected {len(self._fields)}, got {values}")

        for value, field in zip(values, self._fields):
            setattr(self, field.name, value)

    def __repr__(self):
        fields = [f"{field.name}={getattr(self, field.name)}" for field in self._fields]
        return f"{self.__class__.__name__}({', '.join(fields)})"

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return all(getattr(self, field.name) == getattr(other, field.name) for field in self._fields)

    @classmethod
    def fromBytestring(cls, datagram: bytes):
        io = BytesIO()
        io.write(datagram)
        io.seek(0)
        if not cls._version:
            parser = cls._fields
        else:
            version = Packers.uint8.getValue(io)
            parser = cls._parsers[version - 1]

        fieldValues = []
        for field in parser:
            value = field.packer.getValue(io)
            if field.active:
                for converter in field.converters:
                    value = converter(None, value)
                fieldValues.append(value)

        assert io.read() == b"", "The ending of the datagram was not read!"
        return cls(*fieldValues)

    @property
    def bytestring(self) -> bytes:
        io = BytesIO()
        if self._version:
            Packers.uint8.addValue(io, self._version)
        for field in self._fields:
            field.packer.addValue(io, getattr(self, field.name))
        io.seek(0)
        return io.read()

    @classmethod
    def setMembers(cls, classdict, version):
        cls._version = version

        fields = []
        allMigrations = []
        for name, member in classdict.items():
            if isinstance(member, Migration):
                allMigrations.append(member)
            elif isinstance(member, ValueType):
                fields.append(ParsingField(name, True, member, ()))

        cls._fields = fields
        parsers = [fields]
        if version is not None:
            newFields = fields
            for prevVersion in range(version - 1, 0, -1):
                migrations = {mig.convertedField: mig for mig in allMigrations if mig.fromVersion == prevVersion}
                oldFields = []
                for field in newFields:
                    mig = migrations.get(field.name)
                    if not mig:
                        oldFields.append(field)
                    elif mig.removed:
                        raise ValueError(f"Invalid removal migration detected: {mig}")
                    else:
                        if mig.oldParser is None:
                            packer = ConstantPacker(mig.callback)
                            converters = field.converters
                        else:
                            packer = mig.oldParser
                            converters = (mig.callback, *field.converters)
                        oldFields.append(ParsingField(field.name, field.active, packer, converters))

                # A bit inefficient but this only has to be done once at program initialization
                # (well once per deleted field)
                for mig in migrations.values():
                    if mig.locatedAfter:
                        for idx, field in enumerate(oldFields):
                            if field.name == mig.locatedAfter:
                                oldFields.insert(idx + 1, ParsingField(mig.convertedField, False, mig.oldParser, ()))
                                break

                parsers.append(oldFields)
                newFields = oldFields

        cls._parsers = list(reversed(parsers))