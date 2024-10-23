@echo off

REM 현재 배치 파일의 디렉토리 경로
SET SCRIPT_DIR=%~dp0

REM 스크립트와 같은 디렉토리에 있는 ui.py 실행
python "%SCRIPT_DIR%teleport_ui.py"
pause