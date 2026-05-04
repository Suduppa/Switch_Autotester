import json
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_path = os.path.join(base_dir, 'test_data.json')

str_valid, str_invalid = [], []
ips_valid, ips_invalid = [], []
time_valid, time_invalid = [], []

if os.path.exists(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            str_valid = data.get("str_valid", [])
            str_invalid = data.get("str_invalid", [])
            ips_valid = data.get("ips_valid", [])
            ips_invalid = data.get("ips_invalid", [])
            time_valid = data.get("time_valid", [])
            time_invalid = data.get("time_invalid", [])
    except Exception as e:
        print(f"Ошибка чтения JSON: {e}")