#!/bin/bash

# Directorul ce se doreste a fi monitorizat
DIR_TO_WATCH="/home/dragos/Desktop/Practica/File_Monitoring/monitorized_directory"

# Fisierul de log in care se vor inregistra modificarile
LOG_FILE="/home/dragos/Desktop/Practica/File_Monitoring/logs/file_changes.log"

declare -A moved_files

# Utilizarea inotifywait pentru monitorizarea modificarilor
inotifywait -m -r -e create -e delete -e modify -e move -e attrib --timefmt '%Y-%m-%d %H:%M:%S' --format '%T %w %f %e' "$DIR_TO_WATCH" | while read timestamp dir file event
do
  full_path="$dir$file"

  # Filtrarea fișierelor temporare
  if [[ "$file" != *".goutputstream-"* ]]; then
    if [[ "$event" == *"MOVED_FROM"* ]]; then
      moved_files["$file"]="$timestamp $full_path"
    elif [[ "$event" == *"MOVED_TO"* ]]; then
      src="${moved_files[$file]}"
      if [[ -n "$src" ]]; then
        echo "$src MOVED_TO $full_path" >> "$LOG_FILE"
        unset moved_files["$file"]
      else
        echo "$timestamp $full_path $event" >> "$LOG_FILE"
      fi
    elif [[ "$event" == *"CREATE"* ]]; then
      echo "$timestamp $full_path CREATED" >> "$LOG_FILE"
    elif [[ "$event" == *"DELETE"* ]]; then
      echo "$timestamp $full_path DELETED" >> "$LOG_FILE"
    elif [[ "$event" == *"MODIFY"* ]]; then
      echo "$timestamp $full_path MODIFIED" >> "$LOG_FILE"
    elif [[ "$event" == *"ATTRIB"* ]]; then
      echo "$timestamp $full_path ATTRIBUTE_CHANGED" >> "$LOG_FILE"
    else
      echo "$timestamp $full_path $event" >> "$LOG_FILE"
    fi
  fi
done

