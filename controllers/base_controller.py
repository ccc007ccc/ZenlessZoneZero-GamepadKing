from abc import ABC, abstractmethod

class BaseController(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def add_callback(self, button, event, callback):
        pass