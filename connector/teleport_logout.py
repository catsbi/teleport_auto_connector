import subprocess
import os
from teleport_properties import properties as prop

def execute_database_logout():
    current_os = os.name  # 'posix' for Unix-like systems, 'nt' for Windows

    commands = [
        "tsh db logout jobflex-b2b-dv",
        "tsh db logout jobflex-b2b-st",
        "tsh db logout jobflex-b2b-st2",
        "tsh db logout ats-llm-dv"
    ]

    # Kill processes by port based on the OS
    if current_os == 'posix':  # Unix-like systems (Linux, macOS)
        commands += [
            f"kill -9 $(lsof -t -i :{prop['DV_PORT']})",
            f"kill -9 $(lsof -t -i :{prop['ST_PORT']})",
            f"kill -9 $(lsof -t -i :{prop['QA_PORT']})",
            f"kill -9 $(lsof -t -i :{prop['RETENTION_DV_PORT']})"
        ]
    elif current_os == 'nt':  # Windows
        commands += [
            f"netstat -ano | findstr :{prop['DV_PORT']} | for /f \"tokens=5\" %a in ('findstr :{prop['DV_PORT']}') do taskkill /PID %a /F",
            f"netstat -ano | findstr :{prop['ST_PORT']} | for /f \"tokens=5\" %a in ('findstr :{prop['ST_PORT']}') do taskkill /PID %a /F",
            f"netstat -ano | findstr :{prop['QA_PORT']} | for /f \"tokens=5\" %a in ('findstr :{prop['QA_PORT']}') do taskkill /PID %a /F",
            f"netstat -ano | findstr :{prop['RETENTION_DV_PORT']} | for /f \"tokens=5\" %a in ('findstr :{prop['RETENTION_DV_PORT']}') do taskkill /PID %a /F"
        ]

    # Add the final logout command
    commands.append("tsh logout")

    # Execute commands
    for command in commands:
        subprocess.run(command, shell=True)
        print(f"Executed: {command}")

def main():
    execute_database_logout()

if __name__ == "__main__":
    main()
