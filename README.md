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

 *Logurile vor fi transmise si stocate intr-un server, simulat in Vmware pe o distributie de linux mint.
 
 *Am instalat Vmware impreuna cu distributia de linux, am configurat modul bridge intrucat permite accesul direct prin ssh folosind adresa IP din reteaua locala.

 Actualizarea listei de pachete

sudo apt-get update

 Instalarea serverul SSH

sudo apt-get install openssh-server

 Pornirea si activarea serviciul SSH

sudo systemctl enable ssh

sudo systemctl start ssh

 Verificarea starii serviciului SSH

sudo systemctl status ssh

 Obtinerea adresei ip si conectarea la masina virtuala prin SSH

ssh mint@192.168.1.100

Configurarea transferului fara parola prin generarea cheii pe gazda si copierea cheii pe masina

ssh-keygen -t rsa -b 2048

ssh-copy-id mint@192.168.1.100

 Am probat transferul fisierelor intre dispozitivul pe care se monitorizeaza directorul si masina ce simuleaza serverul.

 Urmeaza analiza logurilor din server si implementarea unor mecanisme de alertare.

UPDATE:
Dupa ce distributia de linux a fost corupta, am reinstalat aceeasi distributie de mint nativ si inca o distributie de mint in virtualbox pentru a simula un server la care ma conectez prin ssh (Masina virtuala este de asemenea in modul Bridged).

De data aceasta am intampinat probleme la partea de conectare fara parola, deoarece nu stiam parola default de la mint pentru conectarea prin ssh (nu merge cu enter, mint sau alte variante).

Pentru a solutiona problema, am creat un nou utilizator, caruia i-am setat o parola si m-am conectat cu parola.

----------Ziua 5----------

Am creat un script pentru transmiterea fisierelor de log catre server, unde vor fi analizate. 

Am folosit sshpass pentru a furniza parola necesarea pentru autentificare direct in linia de comanda, pentru a simplifica automatizarea.

ex rulare: sshpass -p "parola" ssh utilizator@server

OBS: Din punct de vedere al securitatii, sshpass este o unealta intr-o oarecare masura nesigura, intrucat contine in cadrul scriptului parola in clar, dar vom face obfuscation pe cod la finalul proiectului.

Vom folosi rsync pentru a optimiza transferul de fisiere, transferand doar modificarile fisierelor, in locul fisierelor complete.

----------Ziua 6----------


Configurare ELK pentru analiza logurilor

curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch |sudo gpg --dearmor -o /usr/share/keyrings/elastic.gpg


echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list

sudo apt install elasticsearch

sudo nano /etc/elasticsearch/elasticsearch.yml

. . .
# ---------------------------------- Network -----------------------------------
#
# Set the bind address to a specific IP (IPv4 or IPv6):
#
network.host: localhost
. . .

sudo systemctl start elasticsearch

sudo systemctl enable elasticsearch

curl -X GET "localhost:9200"

output:
{
  "name" : "dragos",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "1aQA58noTWCnRcWyW2xWwg",
  "version" : {
    "number" : "7.17.22",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "38e9ca2e81304a821c50862dafab089ca863944b",
    "build_date" : "2024-06-06T07:35:17.876121680Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.3",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

sudo apt install kibana

sudo systemctl enable kibana

sudo systemctl start kibana

echo "kibanaadmin:`openssl passwd -apr1`" | sudo tee -a /etc/nginx/htpasswd.users

 /etc/nginx/htpasswd.users
tee: /etc/nginx/htpasswd.users: No such file or directory
Password: 
Verifying - Password: 
kibanaadmin:$apr1$k5clgpfa$LSjw9zInUjvBnP4bmNtn20


sudo apt install logstash

sudo nano /etc/logstash/conf.d/02-beats-input.conf

input {
  beats {
    port => 5044
  }
}

sudo nano /etc/logstash/conf.d/30-elasticsearch-output.conf


output {
  if [@metadata][pipeline] {
	elasticsearch {
  	hosts => ["localhost:9200"]
  	manage_template => false
  	index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
  	pipeline => "%{[@metadata][pipeline]}"
	}
  } else {
	elasticsearch {
  	hosts => ["localhost:9200"]
  	manage_template => false
  	index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
	}
  }
}

sudo systemctl start logstash

sudo systemctl enable logstash


Am adaugat in crontab toate scripturile

@reboot /bin/bash /home/dragos/Desktop/Practica/File_Monitoring/scripts/file_monitor.sh
@reboot /bin/bash /home/dragos/Desktop/Practica/File_Monitoring/scripts/log_user_commands.sh
@reboot /bin/bash /home/dragos/Desktop/Practica/File_Monitoring/scripts/monitor_acls.sh
@reboot /bin/bash /home/dragos/Desktop/Practica/File_Monitoring/scripts/monitor_capabilities.sh





