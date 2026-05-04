from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd

data_manager = None

OID_NAMES = {
    "1.3.6.1.2.1.1.3.0": "Аптайм (sysUpTime)",
    "1.3.6.1.2.1.2.2.1.8.1": "Link Порт 1 (1=Up, 2=Down)",
    "1.3.6.1.2.1.2.2.1.8.2": "Link Порт 2 (1=Up, 2=Down)",
    "1.3.6.1.2.1.2.2.1.8.3": "Link Порт 3 (1=Up, 2=Down)",
    "1.3.6.1.2.1.2.2.1.8.4": "Link Порт 4 (1=Up, 2=Down)",
    "1.3.6.1.2.1.2.2.1.8.5": "Link Порт 5 (1=Up, 2=Down)",
    "1.3.6.1.2.1.2.2.1.8.6": "Link Порт 6 (1=Up, 2=Down)",
    "1.3.6.1.2.1.2.2.1.8.7": "Link Порт 7 (1=Up, 2=Down)",
    "1.3.6.1.2.1.2.2.1.8.8": "Link Порт 8 (1=Up, 2=Down)",
    "1.3.6.1.2.1.2.2.1.8.9": "Link Порт 9 (1=Up, 2=Down)",
    "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.1": "PoE Порт 1",
    "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.2": "PoE Порт 2",
    "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.3": "PoE Порт 3",
    "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.4": "PoE Порт 4",
    "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.5": "PoE Порт 5",
    "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.6": "PoE Порт 6",
    "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.7": "PoE Порт 7",
    "1.3.6.1.4.1.42019.3.2.2.5.1.1.2.8": "PoE Порт 8",
    "1.3.6.1.4.1.42019.3.2.2.5.1.1.3.2": "Что-то2",
    "1.3.6.1.4.1.42019.3.2.2": "Status PSW",
    "1.3.6.1.4.1.42019.3.2.2.1": "UPS status",
    "1.3.6.1.4.1.42019.3.2.2.2": "Input status"
}

def get_snmp_values(ip, community, oid_list, sheet_name="SNMP", test_index_start=1):
    current_index = test_index_start
    for oid_str in oid_list:
        human_name = OID_NAMES.get(oid_str, f"Неизвестный OID: {oid_str}")
        try:
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(community, mpModel=0), 
                UdpTransportTarget((ip, 161), timeout=2, retries=1),
                ContextData(),
                ObjectType(ObjectIdentity(oid_str))
            )

            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

            if errorIndication:
                result_text = f"Ошибка сети: {errorIndication}"
            elif errorStatus:
                result_text = f"Ошибка SNMP: {errorStatus.prettyPrint()}"
            else:
                result_text = " = ".join([x.prettyPrint() for x in varBinds])

            print(f"[SNMP] {human_name} -> {result_text}")
            
            if data_manager:
                status_text = "Ошибка" if "Ошибка" in result_text else "Успех"
                clean_value = result_text.split(" = ")[-1] if " = " in result_text else result_text

                data_manager.sync_add_result(
                    test_source=sheet_name,
                    command=f"GET {oid_str} ({human_name})", 
                    status=status_text,       
                    output=clean_value,
                    target_value="N/A"
                )
            
        except Exception as e:
            print(f"[SNMP] Критическая ошибка при запросе {oid_str}: {e}")
            if data_manager:
                data_manager.sync_add_result(
                    test_source=sheet_name,
                    command=f"GET {oid_str}",
                    status="Ошибка",
                    output=f"Исключение: {str(e)}",
                    target_value="N/A"
                )
            
        current_index += 1

    return current_index