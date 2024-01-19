from abc import ABCMeta,abstractmethod

class MqttServerInterface(metaclass=ABCMeta):
    @abstractmethod
    def send_configuration(self):raise NotImplementedError

class MqttClientInterface(metaclass=ABCMeta):

    @abstractmethod
    def request_configuration(self):raise NotImplementedError
    
    @abstractmethod
    def reply_event_changed(self):raise NotImplementedError

    @abstractmethod
    def reply_services(self):raise NotImplementedError

    @abstractmethod
    def reply_error(self):raise NotImplementedError

    @abstractmethod
    def reply_ack(self):raise NotImplementedError

    @abstractmethod
    def retry_request_configuration(self): raise NotImplementedError

    @abstractmethod
    def update_configuration(self): raise NotImplementedError

    @abstractmethod
    def send_message(self): raise NotImplementedError
