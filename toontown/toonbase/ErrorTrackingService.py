import os
from enum import Enum


class ServiceType(Enum):
    UBERDOG = "UberDOG"
    AI      = "AI/District"
    CLIENT  = "Client"


class ErrorTrackingService:

    def __init__(self, service: ServiceType, version: str):

        self.service_type: ServiceType = service
        self.version = version  # The version of the game

    def want_error_reporting(self) -> bool:
        return os.environ.get('WANT_ERROR_REPORTING', '').lower() in ('1', 'true', 't', 'yes', 'on')

    def report(self, exception: Exception):
        raise NotImplementedError


class SentryErrorTrackingService(ErrorTrackingService):

    DSN = 'https://482b06f87386ea732671d6f30a617b08@o4507298869936128.ingest.us.sentry.io/4507298873671680'

    def __init__(self, service: ServiceType, version: str):
        super().__init__(service, version)

        if not self.want_error_reporting():
            return

        self.__init_sentry()

    def __init_sentry(self):
        import sentry_sdk
        sentry_sdk.init(
            dsn=self.DSN,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
        self.set_tags()

    def set_tags(self):
        import sentry_sdk
        sentry_sdk.set_tag('game-service', self.service_type.value)
        sentry_sdk.set_tag('game-version', self.version)

    def report(self, exception: Exception):

        if not self.want_error_reporting():
            return

        import sentry_sdk
        if not sentry_sdk.is_initialized():
            self.__init_sentry()

        sentry_sdk.capture_exception(exception)
