#!/bin/bash

# Directorul ce se dorește a fi monitorizat pentru ACL-uri
DIR_TO_WATCH="/home/dragos/Desktop/Practica/File_Monitoring/monitorized_directory"

# Fisierul de log în care se vor înregistra modificările de ACL
LOG_FILE="/home/dragos/Desktop/Practica/File_Monitoring/logs/acl_changes.log"

# Funcția pentru monitorizarea ACL-urilor
monitor_acl() {
  # Folosim inotifywait pentru a monitoriza schimbările ACL-urilor
  inotifywait -m -r -e attrib --timefmt '%Y-%m-%d %H:%M:%S' --format '%T %w %f %e' "$DIR_TO_WATCH" | while read timestamp dir file event
  do
    full_path="$dir$file"
    
    # Înregistram evenimentul în fișierul de log
    echo "[$timestamp] ACL event: $event on file: $full_path" >> "$LOG_FILE"
  done
}

# Pornim monitorizarea ACL-urilor în fundal
monitor_acl &

