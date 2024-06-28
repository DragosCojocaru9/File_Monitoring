#!/bin/bash

# Setarea parametrilor pentru conexiunea SSH
remote_user="dragos"
remote_host="192.168.88.140"
remote_password="mint"

# Directorul de unde trimitem fisierele de log
local_logs_dir="/home/dragos/Desktop/Practica/File_Monitoring/logs"

# Comanda pentru a trimite fisierele
sshpass -p "$remote_password" rsync -avz -e "ssh -o StrictHostKeyChecking=no" "$local_logs_dir/" "$remote_user@$remote_host:~/"

# Verificare status
if [ $? -eq 0 ]; then
    echo "Fisierele au fost trimise cu succes la serverul $remote_host."
else
    echo "A intervenit o eroare in timpul transferului fisierelor."
fi

