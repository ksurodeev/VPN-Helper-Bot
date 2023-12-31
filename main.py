from check_status import Check_Status
from check_logs import Check_Logs
from trafficstatus import Traffic_Status

if __name__ == '__main__':
    check_status = Check_Status('ipsec-vpn-server')
    print('\n Status of your container is', check_status.Execute(), '\n')
    if check_status.Execute() != 'running':
        print('Your container is not in running status')  # here we need to LOG
    check_logs = Check_Logs('ipsec-vpn-server')
    check_logs.Execute()
    traffic_status = Traffic_Status('ipsec-vpn-server')
    print(traffic_status.represent_results())
