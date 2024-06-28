    import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import re

# Configurarea email-ului
def send_alert_email(subject, body):
    from_email = 'dragos.cojocaru@mta.ro'  # Inlocuieste cu email-ul tau
    to_email = 'dragoscojocaru6@gmail.com'
    password = 'Password!'  # Inlocuieste cu parola ta

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email trimis cu succes!")
    except Exception as e:
        print(f"Eroare la trimiterea email-ului: {e}")

# Functia de monitorizare a log-urilor
def monitor_logs(log_files):
    # Expresii regulate pentru a detecta evenimentele suspecte
    acl_pattern = re.compile(r'ACL event: .* ATTRIB')
    capability_pattern = re.compile(r'cap_\w+=eip')
    file_event_pattern = re.compile(r'CREATED|DELETED|MODIFIED|ATTRIBUTE_CHANGED')

    file_handles = {log_file: open(log_file, 'r') for log_file in log_files}

    # Mutam cursorul la sfarsitul fisierelor
    for log_file, handle in file_handles.items():
        handle.seek(0, 2)

    try:
        while True:
            for log_file, handle in file_handles.items():
                line = handle.readline()
                if not line:
                    continue

                if acl_pattern.search(line) or capability_pattern.search(line) or file_event_pattern.search(line):
                    print(f"Activitate suspecta detectata in {log_file}: {line.strip()}")
                    send_alert_email("Alerta: Activitate suspecta detectata", f"{log_file}: {line.strip()}")
            time.sleep(1)
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

