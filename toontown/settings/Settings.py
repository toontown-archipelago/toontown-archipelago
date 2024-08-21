from dataclasses import asdict, dataclass
import json
from typing import Union, Any
from pathlib import Path

from direct.showbase.MessengerGlobal import messenger
# Valid types for a setting.
ControlSetting = dict[str, str]
Setting = Union[str, int, bool, list, float, ControlSetting]


@dataclass
class ControlSettings:
    MOVE_UP: str = "arrow_up"
    MOVE_DOWN: str = "arrow_down"
    MOVE_LEFT: str = "arrow_left"
    MOVE_RIGHT: str = "arrow_right"
    JUMP: str = "control"
    SPRINT: str = "shift"
    SCREENSHOT: str = "f9"
    MAP_PAGE_HOTKEY: str = "escape"
    FRIENDS_LIST_HOTKEY: str = "f7"
    STREET_MAP_HOTKEY: str = "alt"
    INVENTORY_HOTKEY: str = "home"
    QUEST_HOTKEY: str = "end"
    GALLERY_HOTKEY: str = "g"
    CRANE_GRAB_KEY: str = "control"
    ACTION_BUTTON: str = "delete"
    SECONDARY_ACTION: str = "insert"
    CHAT_HOTKEY: str = "t"


class Settings:
    # All controls with their respective default values.
    controls = ControlSettings()

    # All settings with their respective default values.
    defaultSettings = {
        "borderless": False,
        "music": True,
        "sfx": True,
        "toon-chat-sounds": True,
        "resolution": [1280, 720],
        "music-volume": 0.4,
        "sfx-volume": 0.4,
        "competitive-boss-scoring": True,
        "report-errors": True,
        "anti-aliasing": 0,
        "anisotropic-filter": 8,
        "frame-blending": True,
        "controls": asdict(controls),
        "vertical-sync": True,
        "frame-rate-meter": False,
        "fovEffects": True,
        "cam-toggle-lock": False,
        "movement_mode": "TTCC",
        "sprint_mode": "Hold",
        "magic-word-activator": 0,
        "camSensitivityX": 0.25,
        "camSensitivityY": 0.1,
        "fps-limit": 0,
        # Options below this comment will not be exposed by OptionsPage
        # They can still be configurable by the end user
        "want-legacy-models": False,
        "experimental-multithreading": False,
        'discord-rich-presence': False,
        "archipelago-textsize": 0.5,
        "color-blind-mode": False,
    }
    settingsFile = Path.home() / "Documents" / "Toontown Archipelago" / "settings.json"


    def __init__(self) -> None:
        try:
            with self.settingsFile.open(encoding='utf-8') as f:
                self._settings = json.load(f)
        except FileNotFoundError:
            self.settingsFile.parent.mkdir(parents=True, exist_ok=True)
            self._settings = self.defaultSettings.copy()
        except Exception as e:
            raise e

        # Re-instantiate the ControlSettings with our saved controls.
        self.updateControls(self.get("controls"))
        self.write()

    def get(self, setting: str) -> Setting:
        return self._settings.get(setting, self.defaultSettings.get(setting))

    def set(self, setting: str, value: Setting) -> None:
        if not isinstance(value, type(self.defaultSettings.get(setting))):
            return
        self._settings[setting] = value

    def setControl(self, control: str, keybind: str) -> None:
        # First, get the control setting.
        controls: ControlSetting = self.get("controls")
        # Replace the keybind at the control.
        controls[control] = keybind
        # Update the control settings with our new controls.
        self.updateControls(controls)

    def getControl(self, control: str) -> str:
        return self.getControls().get(control, "")

    def getControls(self) -> dict[str, Any]:
        return asdict(self.controls)

    def updateControls(self, controls: dict[str, str]) -> None:
        self.controls = ControlSettings(**controls)
        self.set("controls", asdict(self.controls))

    def write(self) -> None:
        with self.settingsFile.open("w", encoding='utf-8') as _settings:
            # Clean the settings dictionary before saving it to the file.
            self.clean()
            json.dump(self._settings, _settings, sort_keys=True, indent=4)

    def clean(self) -> None:
        """
        Removes all keys in settings which shouldn't exist.
        (they don't exist in defaultSettings)
        """
        for setting in list(self._settings):
            if setting not in self.defaultSettings:
                del self._settings[setting]
