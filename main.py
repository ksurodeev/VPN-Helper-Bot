from check_status import Check_Status
from check_logs import Check_Logs

if __name__ == '__main__':
    container_id = 'ipsec-vpn-server'
    check_status = Check_Status(container_id)
    check_logs = Check_Logs(container_id)

    print (check_status, check_logs)