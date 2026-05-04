# SMTP
#@register_test("smtp_config") #done
#def test_smtp_config():
#    cmds = []
#    cmds.append(f"# smtp_config — валидные имена")
#    for val in str_valid:
#        cmds += [
#            f"services smtp config user {val} password not4test", #не указал host
#            f"services smtp config user not4test password {val}", #не указал host
#            f"services smtp config host {val}", #не указал юзера и пароль
#            f"services smtp config to {val}",
#
#        ]
#    cmds.append(f"# smtp_config — невалидные имена")
#    for val in str_invalid:
#        cmds += [
#            f"services smtp config user {val} password not4test", #не указал host
#            f"services smtp config user not4test password {val}", #не указал host
#            f"services smtp config host {val}", #не указал юзера и пароль
#            f"services smtp config to {val}"
#        ]
#    return cmds


# SNMP
#@register_test("snmp_config") # done #todo посмотреть что можно сделать с командами, тк в репорт записывается значение testvalue
#def test_snmp_config():
#    cmds = []
#    cmds.append("# snmp_config — валидные имена")
#    for val in str_valid:
#        cmds += [
#            f"services snmp config state enable version v3 enable username {val}",
#            #f"services snmp config state enable version v3 enable username {val} auth_type MD5 auth_pass not4test privacy_type DES privacy_pass not4test",
#            f"services snmp config state enable version v3 enable username not4test auth_type MD5 auth_pass {val} privacy_type DES privacy_pass not4test",
#            f"services snmp config state enable version v3 enable username not4test auth_type MD5 auth_pass not4test privacy_type DES privacy_pass {val}",
#            f"services snmp config state enable version v1 enable read_community {val}",
#            f"services snmp config state enable version v1 enable write_community {val}",
#        ]
#    cmds.append("# snmp_config — невалидные имена")
#    for val in str_invalid:
#        cmds += [
#            f"services snmp config state enable version v3 enable username {val}",
#            #f"services snmp config state enable version v3 enable username {val} auth_type MD5 auth_pass not4test privacy_type DES privacy_pass not4test",
#            f"services snmp config state enable version v3 enable username not4test auth_type MD5 auth_pass {val} privacy_type DES privacy_pass not4test",
#            f"services snmp config state enable version v3 enable username not4test auth_type MD5 auth_pass not4test privacy_type DES privacy_pass {val}",
#            f"services snmp config state enable version v1 enable read_community {val}",
#            f"services snmp config state enable version v1 enable write_community {val}",
#        ]
#    return cmds

#Новые тестики

from types import ClassMethodDescriptorType
from test_framework import register_test
from data.test_main import str_valid, str_invalid, ips_valid, ips_invalid, time_valid, time_invalid

# VLAN — имена
@register_test("ssh__UsIn__vlan__name__full")
def vlan_name_test():
    cmds = []
    for vid in range(1, 2):
        cmds.append(f"# VLAN {vid} — валидные имена")
        cmds += [(f"network vlan config vlanid {vid} name {v}", v) for v in str_valid]
        cmds.append(f"# VLAN {vid} — невалидные имена (ошибки ожидаемы)")
        cmds += [(f"network vlan config vlanid {vid} name {v}", v) for v in str_invalid]
    return cmds
    cmds.append("changes revert")

@register_test("ssh__UsIn__changes__revert")
def changes_revert_config_type():
    cmds = []
    cmds.append("# Сonfig_type — валидные имена")
    cmds += [(f"changes revert config_type {v}", v) for v in str_valid]
    cmds.append("# config_type — инвалидные имена")
    cmds += [(f"changes revert config_type {v}", v) for v in str_invalid]
    return cmds

# RADIUS
@register_test("ssh__UsIn__radius__config")
def test_radius_config():
    cmds = []
    cmds.append("# Radius_config — валидные имена")
    for val in str_valid:
        cmds += [
            (f"special radius config general ca_cert {val}", val),
            (f"special radius config general server_cert {val}", val),
            (f"special radius config general private_key {val}", val),
            (f"special radius config general shared_secret {val}", val),
        ]
    cmds.append(f"# Radius_config — невалидные имена")
    for val in str_invalid:
        cmds += [
            (f"special radius config general ca_cert {val}", val),
            (f"special radius config general server_cert {val}", val),
            (f"special radius config general private_key {val}", val),
            (f"special radius config general shared_secret {val}", val),
        ]
    return cmds

# SMTP
@register_test("ssh__UsIn__smtp__config")
def test_smtp_config():
    cmds = []
    cmds.append(f"# smtp_config — валидные имена")
    for val in str_valid:
        cmds += [
            (f"services smtp config user {val} password not4test", val),
            (f"services smtp config user not4test password {val}", val),
            (f"services smtp config host {val}", val),
            (f"services smtp config to {val}", val),
        ]
    cmds.append(f"# smtp_config — невалидные имена")
    for val in str_invalid:
        cmds += [
            (f"services smtp config user {val} password not4test", val),
            (f"services smtp config user not4test password {val}", val),
            (f"services smtp config host {val}", val),
            (f"services smtp config to {val}", val)
        ]
    return cmds

# SNMP
@register_test("ssh__UsIn__snmp__config")
def test_snmp_config():
    cmds = []
    cmds.append("# snmp_config — валидные имена")
    for val in str_valid:
        cmds += [
            (f"services snmp config state enable version v3 enable username {val}", val),
            (f"services snmp config state enable version v3 enable username not4test auth_type MD5 auth_pass {val} privacy_type DES privacy_pass not4test", val),
            (f"services snmp config state enable version v3 enable username not4test auth_type MD5 auth_pass not4test privacy_type DES privacy_pass {val}", val),
            (f"services snmp config state enable version v1 enable read_community {val}", val),
            (f"services snmp config state enable version v1 enable write_community {val}", val),
        ]
    cmds.append("# snmp_config — невалидные имена")
    for val in str_invalid:
        cmds += [
            (f"services snmp config state enable version v3 enable username {val}", val),
            (f"services snmp config state enable version v3 enable username not4test auth_type MD5 auth_pass {val} privacy_type DES privacy_pass not4test", val),
            (f"services snmp config state enable version v3 enable username not4test auth_type MD5 auth_pass not4test privacy_type DES privacy_pass {val}", val),
            (f"services snmp config state enable version v1 enable read_community {val}", val),
            (f"services snmp config state enable version v1 enable write_community {val}", val),
        ]
    return cmds

# SNTP
@register_test("ssh__UsIn__sntp__config")
def test_sntp_config():
    cmds = []
    cmds.append("# sntp_config — валидные имена")
    for val in str_valid:
        cmds += [(f"services sntp config add host_name {val}", val)]
        #f"services sntp config delete host_name {val}",
    cmds.append("# sntp_config — невалидные имена")
    for val in str_invalid:
        cmds += [(f"services sntp config add host_name {val}", val)]
        #f"services sntp config delete host_name {val}",
    return cmds
    cmds.append("changes revert")

# TFDM не проходят тесты
@register_test("ssh__UsIn__tfdm__config")
def test_tfdm_config():
    cmds = []
    cmds.append("# tfdm_config — валидные имена")
    for val in str_valid:
        cmds.append((f"special device_manager config ifname {val} state enable", val))
    cmds.append("# tfdm_config — невалидные имена")
    for val in str_invalid:
        cmds.append((f"special device_manager config if_name {val} state enable", val))
    return cmds

# mngt_vlan
@register_test("ssh__UsIn__mngt__vlan")
def test_mngt_vlan():
    cmds = []
    cmds.append("# mngt_vlan — валидные имена")
    for val in str_valid:
        cmds.append((f"network vlan config mngt_vlan action add ifname {val} vlan_id 1", val))
        cmds.append((f"network vlan config mngt_vlan action delete ifname {val}", val))
    cmds.append("# mngt_vlan — невалидные имена")
    for val in str_invalid:
        cmds.append((f"network vlan config mngt_vlan action add ifname {val} vlan_id 1", val))
        cmds.append((f"network vlan config mngt_vlan action delete ifname {val}", val))
    return cmds

# System description
@register_test("ssh__UsIn__system__description")
def test_system_description():
    cmds = []
    fields = [ "description", "host_name", "location", "company", "notes"]
    cmds.append("# System description — валидные имена")
    for field in fields:
        for val in str_valid:
            cmds.append((f"system description config {field} {val}", val))
    
    cmds.append("# System_description — невалидные имена")
    for field in fields:
        for val in str_invalid:
            cmds.append((f"system description config {field} {val}", val))
    return cmds

# System log
@register_test("ssh__UsIn__log__config")
def test_log_config():
    cmds = []
    cmds.append("# log_config — валидные имена")
    for val in str_valid:
        cmds += [
            (f"system log config filter add/edit name {val}", val),
            (f"system log config filter add/edit name not4test progname {val}", val),
            (f"system log config filter add/edit name not4test content {val}", val),
            (f"system log config action add/edit name {val}", val),
            #f"system log config action add/edit name not4test log_action send2server server_list {val}", ошибки кидает
            #f"system log config action add/edit name not4test log_action email email_list test_mail@test_mai.ru subject {val}", ошибки кидает
            (f"system log config rule add/edit name {val} filter not4test action Syslog", val),
        ]
    cmds.append("# log_config — невалидные имена")
    for val in str_invalid:
        cmds += [
            (f"system log config filter add/edit name {val}", val),
            (f"system log config filter add/edit name not4test progname {val}", val),
            (f"system log config filter add/edit name not4test content {val}", val),
            (f"system log config action add/edit name {val}", val),
            # f"system log config action add/edit name not4test log_action send2server server_list {val}", ошибки кидает
            # f"system log config action add/edit name not4test log_action email email_list test_mail@test_mai.ru subject {val}", ошибки кидает
            (f"system log config rule add/edit name {val} filter not4test action Syslog", val),
        ]
    return cmds

# Users
@register_test("ssh__UsIn__user__config")
def test_user_config():
    cmds = []
    cmds.append("# User_config — валидные имена")
    for val in str_valid:
        cmds.append((f"system user config add user_name {val} password not4test admin_rule full", val))

    cmds.append("# User_config — инвалидные имена")
    for val in str_invalid:
        cmds.append((f"system user config add username {val} password not4test admin_rule full", val))

    cmds.append("# Удаление созданных пользователей")
    for val in str_valid:
        cmds.append((f"system user config delete user_name {val}", val))
    for val in str_invalid:
        cmds.append((f"system user config delete user_name {val}", val))
    return cmds

# Tools
@register_test("ssh__UsIn__tools__ping")
def test_tools():
    cmds = []
    cmds.append("# Tools_config — валидные имена")
    for val in str_valid:
        cmds += [
            (f"tools ping {val}", val),
            (f"tools ping 192.168.0.1 source {val}", val),
        ]
    cmds.append("# Tools_config — невалидные имена")
    for val in str_invalid:
        cmds += [
            (f"tools ping {val}", val),
            (f"tools ping 192.168.0.1 source {val}", val),
        ]
    return cmds

# Autorestart
@register_test("ssh__UsIn__autorestart__test")
def test_autorestart():
    cmds = []
    cmds.append("#Autorestart - валидные значения")
    for val in time_valid:
        cmds += [
            f"",
        ]
    cmds.append("#Autorestart - невалидные значения")
    for val in time_invalid:
        cmds += [
            f"",
        ]

#SNMP
@register_test("snmp__check")
def snmp_check():
    oids = [
        "1.3.6.1.2.1.1.3.0", # sysUpTime
        "1.3.6.1.2.1.2.2.1.8.1",
        "1.3.6.1.2.1.2.2.1.8.2",
        "1.3.6.1.2.1.2.2.1.8.3",
        "1.3.6.1.2.1.2.2.1.8.4",
        "1.3.6.1.2.1.2.2.1.8.5",
        "1.3.6.1.2.1.2.2.1.8.6",
        "1.3.6.1.2.1.2.2.1.8.7",
        "1.3.6.1.2.1.2.2.1.8.8",
        "1.3.6.1.2.1.2.2.1.8.9",
        "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.1",
        "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.2",
        "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.3",
        "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.4",
        "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.5",
        "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.6",
        "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.7",
        "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.8",
        "1.3.6.1.4.1.42019.3.2.2.5.1.1.3.2",
        "1.3.6.1.4.1.42019.3.2.2", #status PSW
        "1.3.6.1.4.1.42019.3.2.2.1", #UPS status
        "1.3.6.1.4.1.42019.3.2.2.2" # Input status
    ]
    # Возвращаем специальный маркер и данные, чтобы run.py понял, что это SNMP, а не SSH
    return {"type": "snmp_get", "oids": oids}

# Полный опрос статусов и конфигураций
@register_test("ssh__show__all__status")
def test_show_all_status():
    cmds = []
    
    cmds.append("# Запуск глобального опроса show-команд")
    cmds += [
        "network ipif show status arp",
        "network ipif show status fdb",
        "network ipif show status network",
        "network ipif show status packet",
        "network port show configuration",
        "network port show status",
        "network vlan show configuration all",
        #"network vlan show configuration vlan_id 1234",
        "services igmp show configuration",
        "services igmp show status",
        "services snmp show configuration",
        "services lldp show configuration",
        "services lldp show status local",
        "services lldp show status remote",
        "services lldp show status statistic",
        "services lldp show status interfaces",
        "services smtp show configuration",
        "services smtp show configuration password",
        "services smtp test",
        "services sntp show configuration",
        "services stp show configuration bridge",
        "services stp show configuration ports",
        "services stp show status ports",
        "services stp show status bridge",
        "special autorestart show configuration",
        "special autorestart show status",
        "special device_manager show configuration",
        "special io show configuration input",
        "special io show configuration output",
        "special io show status sfp 1",
        "special io show status sfp 2",
        "special io show status ups",
        "special io show status input",
        "special io show status output",
        "special poe show status",
        "special poe show status extended",
        "system log show configuration filter",
        "system log show configuration action",
        "system log show configuration rule",
        "system log show configuration all",
        "system syslog show configuration",
        "system user show configuration",
        "special radius show status client",
        "special radius show status",
        "special radius show configuration",
        "special radius show certificate"
    ]
    
    return cmds

# Управление пользователями CLI (Автоматизированная проверка прав)
@register_test("ssh__UsIn__user__management")
def test_user_management_cli():
    cmds = []
    
    cmds.append("#1. Создание пользователей (под admin)")
    cmds.append(("system user config add user_name test_full password 111 admin_rule full", "test_full"))
    cmds.append(("system user config add user_name test_user password 222 admin_rule read_only", "test_user"))
    
    #test_full
    cmds.append({
        "user": "test_full",
        "password": "111",
        "commands": [
            "# Подключение под test_full (Должно быть Успех)",
            "system user show configuration",             # Команда show
            "system user config add user_name test_add_admin password 333 admin_rule read_only"    # Команда config
        ]
    })

    #test_user
    cmds.append({
        "user": "test_user",
        "password": "222",
        "commands": [
            "# Подключение под test_user (show должен отрабоать)",
            "system user show configuration",             # Команда show (разрешена)
            "# Подключение под test_user (config должен выдать Ошибку)",
            "system user config add user_name test_add_user password 444 admin_rule read_only"    # Команда config (ЗАПРЕЩЕНА)
        ]
    })

    cmds.append("#2. Очистка системы (Снова под admin)")
    cmds.append(("system user config delete user_name test_full", "test_full"))
    cmds.append(("system user config delete user_name test_user", "test_user"))
    cmds.append("system user config add user_name test_add_admin password 333 admin_rule read_only") # Удаляем test_add_admin
        
    return cmds

@register_test("web__user__management")
def test_web_user_management():
    return {"type": "web"}

@register_test("web__availability")
def test_web_availability():
    return {"type": "web"}

@register_test("web__navigation")
def test_web_ui_errors():
    return {"type": "web"}

#@register_test("web__help")
#def test_web_help():
#    return {"type": "web"}

@register_test("web__translation")
def test_web_translation():
    return {"type": "web"}

# SNTP 
@register_test("ssh__sntp__config")
def test_sntp_cli_config():
    cmds = []
    cmds.append("#1. Включение SNTP (Часовой пояс +3, Москва)")
    cmds.append("services sntp config state enable")
    cmds.append("services sntp config timezone 3") 
    cmds.append("services sntp config add host_name www.ntp-servers.net")
    cmds.append("changes save")
    cmds.append(("services sntp show configuration", "VERIFY_TIME_+3"))

    cmds.append("#2. Возврат часового пояса на +5 (Екатеринбург)")
    cmds.append("services sntp config timezone 5")
    cmds.append("changes save")
    cmds.append(("services sntp show configuration", "VERIFY_TIME_+5"))

    cmds.append("#3.Очистка (удаление тестового сервера)")
    cmds.append("services sntp config delete host_name www.ntp-servers.net")
    cmds.append("changes save")

    return cmds

#Проверка сетевых настроек
@register_test("ssh__IP__static")
def test_ssh_ip_static():
    cmds = []
    cmds.append("network ipif show status network")


# Добавить тест: @register_test("имя")

