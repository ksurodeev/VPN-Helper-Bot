from command import Command
from docker import errors
from typing import Union


class Restart(Command):
    def __init__(self, container_id: str) -> None:
        self.container_id = container_id
        self.container = Command.ConnectToContainer(self.container_id)

    def Execute(self) -> Union[None, tuple]:
        try:
            return self.container.exec_run(
                'ipsec-vpn-server service ipsec restart'
                )
        except errors.APIError:
            print('Error in docker prevent the restart of ipsec-vpn-server')
            return None
