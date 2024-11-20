from dependency_injector.wiring import inject, Provide
from infrastructure.app_container import AppContainer

class LoggerObserver:
    @inject
    def __init__(self, logger=Provide[AppContainer.struct_logger]):
        self.logger = logger

    def update(self, event: str, data: dict) -> None:
        self.logger.info(f"Event: {event}, Data: {data}")
