import json
import os

properties_path = "your properties path"

with open(properties_path, 'r') as file:
    # JSON 파일을 읽어서 Python 객체로 변환
    properties = json.load(file)