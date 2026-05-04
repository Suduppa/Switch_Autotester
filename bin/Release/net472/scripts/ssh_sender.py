import paramiko
import time
import re
import traceback
from colorama import Fore, init

init(autoreset=True)

data_manager = None

def clean_output(raw, command, prompt_str):
    try:
        cleaned = raw.replace(command, "", 1)
        cleaned = cleaned.replace(prompt_str, "")
        cleaned = re.sub(r'^[\r\n]+', '', cleaned).strip()
        return cleaned
    except Exception as e:
        return raw

def extract_test_value(command):
    try:
        cmd_no_quotes = command.replace('"', ' ').replace("'", ' ')
        parts = cmd_no_quotes.split()
        keywords = ['config_type', 'description', 'host_name', 'location', 'company', 'notes', 'username', 'auth_pass', 'privacy_pass',
                    'user', 'password', 'host', 'to', 'name', 'ifname', 'progname', 'content', 'email_list',
                    'subject', 'server_list', 'user_name', 'ping', 'source']

        for i, part in enumerate(parts):
            if part in keywords and i + 1 < len(parts):
                return parts[i + 1]

        if len(parts) > 2:
            return parts[-1]
        return "N/A"
    except:
        return "N/A"

def determine_status(output, command=""):
    try:
        output_lower = output.lower()
        if any(word in output_lower for word in ["syntax error", "error", "failed", "invalid", "illegal", "cannot", "unknown"]):
            return "Ошибка"
        elif any(word in output_lower for word in ["success", "успех", "completed", "updated", "applied", "created", "info: no changes"]):
            return "Успех"
        elif "warning" in output_lower or "предупреждение" in output_lower:
            return "Предупреждение"
        elif not output.strip():
            return "Выполнено"
        else:
            success_patterns = [r'configuration\s+updated', r'command\s+executed', r'success', r'completed successfully']
            for pattern in success_patterns:
                if re.search(pattern, output_lower, re.IGNORECASE):
                    return "Успех"
            return "Выполнено"
    except:
        return "Не определен"

def print_result(text):
    try:
        text_l = text.lower()
        if any(x in text_l for x in ["syntax error", "error", "failed", "invalid", "illegal"]):
            print(Fore.RED + text)
        elif "warning:" in text_l or "предупреждение" in text_l:
            print(Fore.YELLOW + text)
        elif "success" in text_l or "успех" in text_l:
            print(Fore.GREEN + text)
        elif "info:" in text_l or "информация" in text_l:
            print(Fore.CYAN + text)
        else:
            print(Fore.WHITE + text)
        print(Fore.WHITE + "─" * 50)
    except:
        print(Fore.WHITE + text)
        print(Fore.WHITE + "─" * 50)

def read_until_prompt(shell, expected_prompt, timeout=12):
    end_time = time.time() + timeout
    output = ""
    while time.time() < end_time:
        if shell.recv_ready():
            chunk = shell.recv(4096).decode('utf-8', errors='ignore')
            output += chunk
            if expected_prompt in output:
                return output, False 
        time.sleep(0.1)
    return output, True

def send_command(ip, user,password, prompt_str, commands, test_name="SSH", test_index=1, explicit_value=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, username=user, password=password, timeout=15, look_for_keys=False, allow_agent=False)
        shell = client.invoke_shell()
        read_until_prompt(shell, prompt_str, timeout=10)

        cmd_list = commands if isinstance(commands, list) else [commands]

        for cmd in cmd_list:
            if cmd.startswith("#"):
                print(Fore.MAGENTA + cmd)
                if data_manager:
                    data_manager.sync_add_result(test_source=test_name, command=cmd, status="Комментарий", output="", target_value="N/A")
                continue
            
            if not cmd.strip():
                continue

            print(Fore.CYAN + f"→ {cmd}")
            
            shell.send(cmd + '\n')
            raw_output, is_timeout = read_until_prompt(shell, prompt_str, timeout=12)

            if is_timeout:
                output = "Таймаут выполнения команды"
                status = "Таймаут"
                print(Fore.RED + output)
            else:
                output = clean_output(raw_output, cmd, prompt_str)
                print_result(output)
                status = determine_status(output, cmd)

            test_val = explicit_value if explicit_value else extract_test_value(cmd)

            if data_manager:
                data_manager.sync_add_result(
                    test_source=test_name,
                    command=cmd,
                    status=status,
                    output=output[:1000],
                    target_value=test_val
                )

    except paramiko.AuthenticationException:
        error_msg = "Неверный логин или пароль"
        print(Fore.RED + error_msg)
        if data_manager:
            data_manager.sync_add_result(test_source=test_name, command="SSH Auth", status="Ошибка", output=error_msg, target_value="N/A")
    except Exception as e:
        error_msg = f"Ошибка выполнения: {str(e)}"
        print(Fore.RED + error_msg)
        if data_manager:
            data_manager.sync_add_result(test_source=test_name, command="SSH Connection", status="Критическая ошибка", output=error_msg, target_value="N/A")
    finally:
        client.close()