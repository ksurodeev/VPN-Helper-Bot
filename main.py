from check_status import Check_Status
from check_logs import Check_Logs
from trafficstatus import Traffic_Status

if __name__ == '__main__':
    check_status = Check_Status('ipsec-vpn-server')
    check_status.Execute()
    if check_status != 'running':
        pass
    check_logs = Check_Logs('ipsec-vpn-server')
#   check_logs.Execute()
    traffic_status = Traffic_Status('ipsec-vpn-server')
    print(traffic_status.represent_results)
