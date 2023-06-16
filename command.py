from abc import ABC, abstractmethod
from docker import DockerClient


class Command(ABC):
    '''
    The Command interface declares a method for executing a command.
    '''

    @abstractmethod
    def ConnectToContainer(self, container_id: str) -> DockerClient:
        with DockerClient.from_env() as client:
            container = client.containers.get(container_id)
            return container

    @abstractmethod 
    def Execute(self) -> None:
        pass
