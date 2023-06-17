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
            output = self.container.exec_run(
                'ipsec trafficstatus'
                )[1].decode('utf-8')
            match = regex.finditer(output)
            print(tabulate(match, headers='keys', tablefmt='psql'))
            return match.groupdict()
        except errors.APIError:
            print('Error in docker. Can\'t execute command')
            return None
