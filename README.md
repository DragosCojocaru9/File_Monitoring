# File_Monitoring
Monitorizare fisiere dintr-un director folosind inotify-tools

----------Ziua 1----------

  *Se vor monitoriza modificarile, adaugarea si stergerea fisierelor cu ajutorul inotify-tools, procesele, permisiunile si capabilitatile (ACL).
  
  *Conectarea la serverul in care se vor stoca logurile se va face prin ssh. 
  
  *Scripturile ce monitorizeaza actiunile utilizatorului vor rula odata cu pornirea sistemului de operare si vor fi setate prin crontab sa transmita date la un anumit interval de timp.
  
  *Analiza logurilor va fi realizata prin intermediul ElasticSearch, Logstash si Kabana.
  
---------Ziua 2----------

  *Vor fi implementate mecanisme de alertare cu ajutorul mail.
  
  *Pentru mentenanta, vom realiza un backup-uri periodice ale scripturilor, in cloud.
  
  *Configurarea mediului de lucru:
  
    -instalare/configurare inotify-tools (monitorizarea modificarilor fisierelor)
    
    -instalare/configurare ELK (ElasticSearch, Logstash, Kibana) (analiza logurilor)
    
    -instalare psacct (logarea comenzilor executate)
    
    -instalare mailutils (mecanism de alertare)
  
  
----------Ziua 3----------

 *Am adaugat directoarele logs, monitored_directory, scripts.
 
 *Scriptul 'file_monitor.sh' monitorizeaza un director specificat si toate subdirectoarele si fisierele pe care le contine, inregistrand modificarile in fisierul log 'file_changes.log' in urmatorul format:
 
2024-06-19 11:27:55/home/dragos/Desktop/practica/File_Monitoring/monitorized_directory/dsad CREATED

2024-06-19 11:27:55/home/dragos/Desktop/practica/File_Monitoring/monitorized_directory/dsad ATTRIBUTE_CHANGED

2024-06-19 11:27:55/home/dragos/Desktop/practica/File_Monitoring/monitorized_directory/dsad MODIFIED

 *Scriptul 'log_user_commands.sh' monitorizeaza modificarile care au log in directorul specificat si in toate subdirectoarele sale, inregistrand modificarile in fisierul de log 'user_commands.log'.

 *Sunt monitorizate diferite evenimente, precum crearea, stergerea, modificarea, mutarea si schimbarile de atribute ale fisierelor. Fiecare eveniment generat de inotifywait este citit si interpretat.

 *Sunt stocate detalii precum timestamp-ul, directorul, numele fisierului si tipul evenimentului. Scriptul exclude fisierele temporare generate de anumite aplicatii din inregistrarea modificarilor, astfel incat doar modificarile semnificative sunt inregistrate in log.

 *Scripturile au fost adaugate in crontab pentru a rula odata cu pornirea sistemului de operare.

 sudo nano /etc/rc.local
 
 /home/dragos/Desktop/practica/File_Monitoring/scripts/file_monitor.sh &
 /home/dragos/Desktop/practica/File_Monitoring/scripts/log_user_commands.sh &

----------Ziua 4----------

----------Ziua 5----------

----------Ziua 6----------
