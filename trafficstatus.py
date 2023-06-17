from command import Command
from docker import errors
from typing import Union
import re
# from datetime import datetime
from tabulate import tabulate


class Traffic_Status(Command):
    def __init__(self, container_id: str) -> None:
        self.container_id = container_id
        self.container = super().ConnectToContainer(self.container_id)

    def Execute(self) -> Union[None, tuple]:
        regex = re.compile(r".* #[\d]+: .*] (?P<ext_ip>[\d.]+), .*,"
                           r" add_time=(?P<start_time>\d+),"
                           r" inBytes=(?P<ingress_bytes>\d+),"
                           r" outBytes=(?P<egress_bytes>\d+),"
                           r" id='(?P<username>.*)',"
                           r" lease=(?P<int_ip>[\d.]+/\d+)"
                           )
        try:
            docker_output = self.container.exec_run(
                'ipsec trafficstatus'
                )[1].decode('utf-8')
            result = [
                match.groups() for match in regex.finditer(docker_output)
                ]
            return tabulate(result,
                            headers=[
                                'ext_ip',
                                'start_time',
                                'ingress_bytes',
                                'egress_bytes',
                                'username',
                                'int_ip'
                                ],
                            tablefmt='psql'
                            )
        except errors.APIError:
            print('Error in docker. Can\'t execute command')
            return None
