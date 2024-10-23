# -*- coding: utf-8 -*-
 
import tkinter as tk
from tkinter import messagebox
import subprocess
 
# Bash 스크립트를 실행하는 함수
def run_bash_script():
    # 입력된 값을 가져옴
    print("hi")

# GUI 생성
root = tk.Tk()
root.geometry("300x100")
root.title("Teleport Executor")
 
# 실행 버튼
submit_button = tk.Button(root, width=30, text="Execute", command=run_bash_script)
submit_button.pack(pady=10)
 
# 종료 버튼
submit_button = tk.Button(root, width=30, text="Terminate", command=run_bash_script)
submit_button.pack(pady=10)
 
# GUI 실행
root.mainloop()