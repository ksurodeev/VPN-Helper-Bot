from command import Command
from docker import errors
from typing import Union


class Traffic_Status(Command):
    def __init__(self, container_id: str) -> None:
        self.container_id = container_id
        self.container = super().ConnectToContainer(self.container_id)

    def Execute(self) -> Union[None, tuple]:
        try:
            return self.container.exec_run(
                'ipsec-vpn-server ipsec trafficstatus'
                )
        except errors.APIError:
            print('Error in docker. Can\'t execute command')
            return None
