from abc import ABC, abstractmethod
import docker


class Command(ABC):
    '''
    The Command interface declares a method for executing a command.
    '''

    def ConnectToContainer(self, container_id: str):
        client = docker.from_env()
        container = client.containers.get(container_id)
        return container

    @abstractmethod
    def Execute(self) -> None:
        pass
