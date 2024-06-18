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
----------Ziua 4----------
----------Ziua 5----------
----------Ziua 6----------
