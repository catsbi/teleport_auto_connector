import subprocess
import pyotp
import time
import os
import json
from teleport_properties import properties as prop
import teleport_logout as tlout

# 운영체제에 따라 pexpect 또는 wexpect를 동적으로 로드
if os.name == 'posix':  # Unix-like 시스템 (Linux, macOS)
    import pexpect as expect_lib
elif os.name == 'nt':  # Windows 시스템
    import wexpect as expect_lib

# Step 1: tsh login with OTP
def tsh_login():
    command = f"tsh login --proxy teleport.devops.midasin.com --user {prop['USER_ID']}" 
    child = expect_lib.spawn(command)
    
    # Expect for password prompt and send password
    # child.expect("Password:")
    child.sendline(prop['USER_PW'])
    
    # After password, expect OTP prompt and generate OTP
    # child.expect("Enter your OTP code:")
    otp_code = generate_otp()
    child.sendline(otp_code)
    
    # Wait until the process completes
    child.expect(expect_lib.EOF)
    print("Login complete")

# OTP 생성 함수
def generate_otp():
    totp = pyotp.TOTP(prop['OTP_SECRET_KEY'])
    otp_code = totp.now()
    print(f"Generated OTP: {otp_code}")
    return otp_code

# Step 3-5: tsh proxy db commands in background (daemon)
def execute_proxy_db_commands_as_daemon():
    commands = [
        "tsh proxy db --tunnel jobflex-b2b-dv --db-user developer --port "+ prop['DV_PORT'],
        "tsh proxy db --tunnel jobflex-b2b-st --db-user developer --port "+ prop['ST_PORT'],
        "tsh proxy db --tunnel jobflex-b2b-st2 --db-user developer --port "+ prop['QA_PORT']
    ]
    
    processes = []
    for command in commands:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        processes.append(process)
        print(f"Started as daemon: {command}")

def isUsedTsh(ports):
    try:
        # 현재 OS를 확인
        current_os = os.name  # 'posix' (Linux, macOS) or 'nt' (Windows)

        for port in ports:
            if current_os == 'posix':  # Unix-like 시스템(Linux, macOS)일 경우
                result = subprocess.run(['lsof', '-t', '-i', f':{port}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            elif current_os == 'nt':  # Windows일 경우
                # netstat로 해당 포트가 사용 중인지 확인
                result = subprocess.run(['netstat', '-ano', '|', 'findstr', f':{port}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.stdout != "":
                if current_os == 'posix':
                    process_ids = result.stdout.strip().split('\n')
                elif current_os == 'nt':
                    # netstat 출력에서 PID 추출
                    lines = result.stdout.strip().split('\n')
                    process_ids = [line.split()[-1] for line in lines if line]  # 마지막 값이 PID

                print(f"Processes running on port {port}: {process_ids}")
                return True

        return False
    except Exception as e:
        return f"An error occurred: {e}"


def main(continueCount):
    # Step 1: Check Teleport Used Status
    if(isUsedTsh([prop['DV_PORT'], prop['ST_PORT'], prop['QA_PORT']])) :
        if (continueCount <= 0) :
            print("The teleportation process is starting, and the remaining restart attempts have expired. Terminating the process.")
        
        continueCount-=1
        print(f"The teleportation process is already in progress. It will be terminated and restarted. (Remaining attempts: {continueCount})")
        tlout.execute_database_logout()
        main(continueCount)
        return

    # Step 1: Login with OTP
    tsh_login()

    # Step 3-5: Run proxy db commands in background
    execute_proxy_db_commands_as_daemon()

if __name__ == "__main__":
    main(3)
