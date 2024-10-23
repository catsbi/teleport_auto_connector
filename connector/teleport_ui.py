# -*- coding: utf-8 -*-
 
import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import platform
import teleport_login
import teleport_logout
 
def execute_process():
    teleport_login.main()


def terminate_process():
    teleport_logout.main()

def open_file_in_default_editor(filename):
 # 현재 스크립트의 디렉토리 경로
    script_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 스크립트 파일의 절대 경로
    file_path = os.path.join(script_dir, filename)  # 파일의 절대 경로 생성

    # 현재 시스템의 플랫폼을 확인
    system_platform = platform.system() 
    
    if system_platform == 'Windows':
        # Windows에서 기본 프로그램으로 파일 열기
        os.startfile(file_path)
    elif system_platform == 'Darwin':  
        # macOS에서 기본 프로그램으로 파일 열기
        subprocess.run(['open', file_path])
    else:
        print("이 코드는 Windows와 macOS에서만 작동합니다.")  

def on_window_close():
     root.destroy()


# GUI 생성
root = tk.Tk()
root.geometry("300x100")
root.title("Teleport Executor")
 
# 실행 버튼
submit_button = tk.Button(root, width=26, text="Execute", command=execute_process)
submit_button.pack(pady=10)
 
# 종료 버튼
submit_button = tk.Button(root, width=26, text="Terminate", command=terminate_process)
submit_button.pack(pady=10)

# 종료 시점에도 logout 처리
root.protocol("WM_DELETE_WINDOW", on_window_close)
 
# 실행 즉시 properties 파일 오픈될 수 있도록 설정
root.after(500, open_file_in_default_editor("teleport_properties.py"))

# GUI 실행
root.mainloop()