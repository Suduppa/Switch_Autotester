import sys
import argparse
import time
from datetime import datetime
import os
import json
import asyncio
import tests_all
from test_framework import run_tests, TEST_REGISTRY
import ssh_sender
import snmp_sender
from data_manager import DataManager

async def wait_for_start_time(start_time_str):
    """Асинхронное ожидание времени запуска"""
    print(f"[*] Отложенный запуск активен. Ожидание времени {start_time_str}...")
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == start_time_str:
            print("[+] Время пришло! Начинаю тестирование.")
            break
        await asyncio.sleep(10)

def run_ssh_blocks(test_data, ip, user, password, sheet_name):
    """Синхронная обертка для прогона блока SSH (выполняется в отдельном потоке)"""
    test_index = 1
    for block in test_data:
        if isinstance(block, tuple):
            cmd_text, expected_val = block
            ssh_sender.send_command(ip, user, password, "Switch#", cmd_text, sheet_name, test_index, explicit_value=expected_val)
            test_index += 1
        elif isinstance(block, str):
            ssh_sender.send_command(ip, user, password, "Switch#", block, sheet_name, test_index)
            if not block.startswith("#"):
                test_index += 1

async def execute_test_suite(test_names, ip, user, password, community, repeats=1):
    dm = DataManager()
    await dm.start()

    ssh_sender.data_manager = dm
    snmp_sender.data_manager = dm
    
    commands_by_test = run_tests(test_names)
    
    if not isinstance(commands_by_test, dict):
        t_name = test_names[0] if isinstance(test_names, list) else test_names
        commands_by_test = {t_name: commands_by_test}
    elif "type" in commands_by_test:
        t_name = test_names[0] if isinstance(test_names, list) else test_names
        commands_by_test = {t_name: commands_by_test}

    try:
        for i in range(repeats):
            if repeats > 1:
                print(f"\n>>> ИТЕРАЦИЯ {i+1} из {repeats} <<<\n")
            
            tasks = []
            
            for test_name, test_data in commands_by_test.items():
                sheet_name = f"{test_name}_R{i+1}" if repeats > 1 else test_name
                
                # SNMP
                if isinstance(test_data, dict) and test_data.get("type") == "snmp_get":
                    oids = test_data.get("oids", [])
                    print(f"[Подготовка] SNMP тест: {test_name}")
                    tasks.append(asyncio.to_thread(snmp_sender.get_snmp_values, ip, community, oids, sheet_name, 1))
                    
                # SSH
                elif isinstance(test_data, list):
                    print(f"[Подготовка] SSH тест: {test_name}")
                    tasks.append(asyncio.to_thread(run_ssh_blocks, test_data, ip, user, password, sheet_name))
                else:
                    print(f"\n[Ошибка] Неизвестный формат данных для теста {test_name}")

            print("\nЗапуск тестов в параллельном асинхронном режиме...")
            await asyncio.gather(*tasks)

    except Exception as e:
        print(f"Критическая ошибка в цикле тестов: {e}")
    finally:
        await dm.stop()
        print("\n[УСПЕХ] Тестирование завершено! Данные сохранены в БД и Excel.")

async def async_main():
    """Асинхронная точка входа для подготовки параметров"""
    parser = argparse.ArgumentParser(description="Автотесты Tfortis")
    parser.add_argument("--ip", default="192.168.0.32")
    parser.add_argument("--user", default="admin")
    parser.add_argument("--psw", default="admin")
    parser.add_argument("--community", default="public")
    parser.add_argument("tests", nargs="*", help="Имена тестов")
    args, unknown = parser.parse_known_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'test_data.json')
    
    delay_active = False
    start_time = "00:00"
    repeats = 1

    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                delay_active = config.get("UseDelayedStart", False)
                start_time = config.get("StartTime", "00:00")
                repeats = int(config.get("RunCount", 1))
        except Exception as e:
            print(f"Ошибка чтения параметров запуска из JSON: {e}")

    if delay_active:
        await wait_for_start_time(start_time)

    test_to_run = args.tests if args.tests else ["user_config"]
    await execute_test_suite(test_to_run, args.ip, args.user, args.psw, args.community, repeats)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        for name in sorted(TEST_REGISTRY.keys()):
            print(name)
        sys.exit(0)
        
    asyncio.run(async_main())

if __name__ == "__main__":
    main()