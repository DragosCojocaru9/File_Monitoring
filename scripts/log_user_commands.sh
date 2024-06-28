#!/bin/bash
Directorul monitorizat si fisierul de log

MONITOR_DIR="/home/dragos/Desktop/Practica/File_Monitoring/monitorized_directory"
LOG_FILE="/home/dragos/Desktop/Practica/File_Monitoring/logs/user_commands.log"
Functia pentru a monitoriza comenzile executate in directorul monitorizat

monitor_commands() {
# Folosim inotifywait pentru a monitoriza modificarile in directorul monitorizat si in subdirectoarele sale
inotifywait -m -r -e create,modify,delete,move --timefmt '%Y-%m-%d %H:%M:%S' --format '%T %e %w%f' "$MONITOR_DIR" | while read timestamp event file; do
# Inregistram evenimentul in fisierul de log
echo "[$timestamp] Event: $event | File: $file" >> "$LOG_FILE"
done
}

monitor_commands &
