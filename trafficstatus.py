from command import Command
from docker import errors
from typing import Union
import re
from datetime import datetime
from tabulate import tabulate


class Traffic_Status(Command):
    def __init__(self, container_id: str) -> None:
        self.container_id = container_id
        self.container = super().ConnectToContainer(self.container_id)

    def Execute(self) -> Union[None, tuple]:
        regex_ike = re.compile(
                           r".* #[\d]+: .*] (?P<ext_ip>[\d.]+), .*,"
                           r" add_time=(?P<start_time>\d+),"
                           r" inBytes=(?P<ingress_bytes>\d+),"
                           r" outBytes=(?P<egress_bytes>\d+),"
                           r" id='(?P<username>.*)',"
                           r" lease=(?P<int_ip>[\d.]+/\d+)"
                          )
        regex_xauth = re.compile(
                           r".* #[\d]+: .*] (?P<ext_ip>[\d.]+),"
                           r" username=(?P<username>.*), .*,"
                           r" add_time=(?P<start_time>\d+),"
                           r" inBytes=(?P<ingress_bytes>\d+),"
                           r" outBytes=(?P<egress_bytes>\d+),"
                           r" lease=(?P<int_ip>[\d.]+\/\d+)"
                           )
        try:
            docker_output = self.container.exec_run(
                'ipsec trafficstatus'
                )[1].decode('utf-8')
#            for match in regex_ike.finditer(docker_output):
#                for timestamp in match.group('start_time'):
#                    datetime.utcfromtimestamp(int(timestamp))
            ike_customers = [
                match.groups() for match in regex_ike.finditer(docker_output)
                ]
            xauth_customers = [
                match.groups() for match in regex_xauth.finditer(docker_output)
            ]
            return tabulate(ike_customers + xauth_customers,
                            headers=['Ext IP', 'Int IP', 'Username',
                                     'Start Time', 'Ingress Bytes',
                                     'Egress Bytes'],)
        except errors.APIError:
            print('Error in docker. Can\'t execute command')
            return None
