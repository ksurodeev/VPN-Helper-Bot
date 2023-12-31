from command import Command
from docker import errors
from typing import Union
import re
from datetime import datetime, timezone
from tabulate import tabulate


class Traffic_Status(Command):
    def __init__(self, container_id: str) -> None:
        self.container_id = container_id
        self.container = super().ConnectToContainer(self.container_id)

    def Execute(self) -> Union[None, str]:
        try:
            return self.container.exec_run(
                'ipsec trafficstatus'
                )[1].decode('utf-8')
#            for match in regex_ike.finditer(docker_output):
#                for timestamp in match.group('start_time'):
#                    datetime.utcfromtimestamp(int(timestamp))

        except errors.APIError:
            print('Error in docker. Can\'t execute command')
            return None

    def represent_results(self: str) -> tabulate:
        try:
            regex_customer_type = re.compile(
                r'.* #[\d]+: (?P<cust_type>\".*\").*'
            )
            regex_ike = re.compile(
                r".* #[\d]+: .*] (?P<ext_ip>[\d.]+), .*,"
                r" add_time=(?P<start_time>\d+),"
                r" inBytes=(?P<ingress_bytes>\d+),"
                r" outBytes=(?P<egress_bytes>\d+),"
                r" .*"
                r" id='(?P<username>.*),"
                r" lease=(?P<int_ip>[\d.]+/\d+)"
            )
            # regex_xauth = re.compile(
            #     r".* #[\d]+: .*] (?P<ext_ip>[\d.]+),"
            #     r" username=(?P<username>.*), .*,"
            #     r" add_time=(?P<start_time>\d+),"
            #     r" inBytes=(?P<ingress_bytes>\d+),"
            #     r" outBytes=(?P<egress_bytes>\d+),"
            #     r" lease=(?P<int_ip>[\d.]+\/\d+)"
            # )
            for match in regex_customer_type.finditer(
                    self.Execute()
            ):
                customers_types = match.groups()
            for each in customers_types:
                # if 'ike' in each:
                ike_customers = []
                for match in regex_ike.finditer(self.Execute()):
                    ike_customers.append(
                        [
                            match.group('ext_ip'),
                            datetime.fromtimestamp(
                                int(match.group('start_time')), timezone.utc
                            ).strftime('%d.%m.%Y %H:%M:%S'),
                            match.group('ingress_bytes'),
                            match.group('egress_bytes'),
                            match.group('username'),
                            match.group('int_ip')
                        ]
                    )
                return tabulate(
                    ike_customers,
                    headers=[
                        'Ext. IP',
                        'Start Time, UTC',
                        'inBytes',
                        'outBytes',
                        'Username',
                        'Int. IP'
                    ]
                )
                # else:
                #    xauth_customers = [
                #        match.groups() for match in regex_xauth.finditer(
                #            self.Execute()
                #        )
                #    ]
                #    return tabulate(
                #        xauth_customers,
                #        headers=[
                #            'Ext. IP',
                #            'Username',
                #            'Start Time',
                #            'inBytes',
                #            'outBytes',
                #            'Int. IP'
                #        ]
                #    )
        except UnboundLocalError:
            return 'You have no any customers on your server'
