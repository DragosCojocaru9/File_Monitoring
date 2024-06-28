#!/bin/bash

DIR_TO_WATCH="/home/dragos/Desktop/Practica/File_Monitoring/monitorized_directory"

LOG_FILE="/home/dragos/Desktop/Practica/File_Monitoring/logs/capabilities.log"

monitor_capabilities() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - Incepem monitorizarea capabilitatilor." >> "$LOG_FILE"
    while true; do

# Utilizam find pentru a gasi toate fisierele din directorul monitorizat si subdirectoarele sale
        find "$DIR_TO_WATCH" -type f -exec getcap {} + 2>/dev/null | while read -r line; do
            echo "$(date +"%Y-%m-%d %H:%M:%S") $line" >> "$LOG_FILE"
        done
        sleep 60  # Asteapta 60 de secunde inainte de a verifica din nou
    done
}

# Rulam functia de monitorizare in fundal
monitor_capabilities &

