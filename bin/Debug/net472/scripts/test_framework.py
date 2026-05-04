from typing import List, Callable, Dict, Union
from colorama import Fore, init

init(autoreset=True)

TEST_REGISTRY = {}

def register_test(name: str):
    def decorator(func: Callable):
        if name in TEST_REGISTRY:
            print(Fore.YELLOW + f"Предупреждение: тест '{name}' перезаписан")
        TEST_REGISTRY[name] = func
        return func
    return decorator

def list_tests():
    print(Fore.CYAN + "\nДоступные тесты:")
    for name in sorted(TEST_REGISTRY.keys()):
        print(Fore.GREEN + f"  {name}")

def run_tests(test_names: Union[str, List[str]]) -> Union[List[str], Dict[str, Union[List[str], dict]]]:
    """Запускает тесты и возвращает команды (SSH) или настройки (SNMP)"""
    if isinstance(test_names, str):
        test_names = [test_names]
    
    if len(test_names) == 1:
        name = test_names[0]
        
        if name not in TEST_REGISTRY:
            print(Fore.RED + f"Тест '{name}' не найден!")
            return []
            
        print(Fore.CYAN + f"\nЗапуск теста -> {name}")
        commands = TEST_REGISTRY[name]()
        
        if isinstance(commands, dict):
            return commands
        else:
            all_commands = ["# Автотест начат"]
            all_commands.extend(commands)
            all_commands.append("# Автотест завершён")
            return all_commands

    else:
        result = {}
        
        for name in test_names:
            if name not in TEST_REGISTRY:
                print(Fore.RED + f"Тест '{name}' не найден!")
                continue
                
            print(Fore.CYAN + f"\nЗапуск теста -> {name}")
            commands = TEST_REGISTRY[name]()
            
            if isinstance(commands, dict):
                result[name] = commands
            else:
                test_cmds = ["# Автотест начат"]
                test_cmds.extend(commands)
                test_cmds.append("# Автотест завершён")
                result[name] = test_cmds
                
        return result