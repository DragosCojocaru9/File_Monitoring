import time
import re

# Functia de scriere a alertelor in fisierul de log si de afisare pe consola
def log_alert(alert_message):
    alert_log_file = '/home/dragos/Desktop/Practica/File_Monitoring/logs/alerts.log'
    with open(alert_log_file, 'a') as alert_file:
        alert_file.write(alert_message + '\n')
    print(alert_message)

# Functia de monitorizare a log-urilor
def monitor_logs(log_files):
    # Expresii regulate pentru a detecta activitatile suspecte
    executable_file_pattern = re.compile(r'cap_\w+=eip')
    delete_file_pattern = re.compile(r'DELETED')
    modify_permissions_pattern = re.compile(r'ATTRIBUTE_CHANGED')

    file_handles = {log_file: open(log_file, 'r') for log_file in log_files}

    try:
        while True:
            for log_file, handle in file_handles.items():
                lines = handle.readlines()
                for line in lines:
                    if (executable_file_pattern.search(line) or 
                        delete_file_pattern.search(line) or 
                        modify_permissions_pattern.search(line)):
                        alert_message = f"Alerta critica de securitate detectata in {log_file}: {line.strip()}"
                        log_alert(alert_message)
            print("Asteptam 2 minute...")  # Afiseaza mesaj de asteptare
            time.sleep(120)  # Asteapta 2 minute inainte de a verifica din nou
    except KeyboardInterrupt:
        print("Monitorizarea a fost oprita.")
    finally:
        for handle in file_handles.values():
            handle.close()

if __name__ == "__main__":
    log_directory = '/home/dragos/Desktop/Practica/File_Monitoring/logs'
    log_files = [
        f"{log_directory}/acl_changes.log",
        f"{log_directory}/capabilities.log",
        f"{log_directory}/file_changes.log",
        f"{log_directory}/user_commands.log"
    ]
    monitor_logs(log_files)

