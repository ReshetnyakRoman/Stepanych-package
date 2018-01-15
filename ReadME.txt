
sudo netstat -plntu - проверка запущенных демонов, на каких портах они слушают и на каких ip

запусл nginx в ручную
sudo nginx -t проверка конфиг файла
sudo nginx запуск
sudo nginx -s stop  - остановка

Добавление ползльзователя для почты:
$ sudo useradd -m john -s /sbin/nologin
$ sudo passwd john

Управление службами systemctl:
sudo systemctl start nginx / mysql / flask-uwsgi / postfix / dovecot
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl status nginx
systemctl halt – останавливает систему
systemctl poweroff – выключает систему
systemctl reboot – перезагружает систему

=======Добавление сервиса в автозагрузку======
Find out the name of service’s script from /etc/init.d/ directory e.g. mysqld or httpd
Add it to chkconfig
sudo /sbin/chkconfig --add mysqld
Make sure it is in the chkconfig.
sudo /sbin/chkconfig --list mysqld
Set it to autostart
sudo /sbin/chkconfig mysqld on

sudo /sbin/chkconfig mysqld off  - выключение сервиса из автозагрузки (аналогичная команда systemctl disable httpd)
sudo /sbin/chkconfig mysqld on  - включение сервиса в атозагрузку  (аналогичная команда sudo systemctl enable nginx)
==================================

Для зауска службы в автозагрузке, нужно сздать служебный файл по адресу /usr/lib/systemd/system/
Файл запуска службы nginx выглядит так (/usr/lib/systemd/system/nginx.service):

[Unit]
Description=The nginx HTTP and reverse proxy server
#After=network.target remote-fs.target nss-lookup.target
After=network-online.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
PIDFile=/var/run/nginx.pid
# Nginx will fail to start if /run/nginx.pid already exists but has the wrong
# SELinux context. This might happen when running `nginx -t` from the cmdline.
# https://bugzilla.redhat.com/show_bug.cgi?id=1268621
ExecStartPre=/usr/bin/rm -f /run/nginx.pid
ExecStartPre=/usr/bin/sleep 20
ExecStartPre=/usr/sbin/nginx -t
ExecStart=/usr/sbin/nginx
ExecReload=/bin/kill -s HUP $MAINPID
KillSignal=SIGQUIT
TimeoutStopSec=5
KillMode=process
PrivateTmp=false

[Install]
WantedBy=multi-user.target


Файл запуска службы uwsgi выглядит так (/usr/lib/systemd/system/flask-uwsgi.service):

[Unit]
Description=uWSGI instance to serve flask-uwsgi project
After=network.target

[Service]
User=nginx
Group=nginx
WorkingDirectory=/home/flask
Environment="PATH=/home/flask/venv-pyth3/bin"
ExecStart=/home/flask/venv-pyth3/bin/uwsgi --ini uwsgi.ini

[Install]
WantedBy=multi-user.target


Файл запуска службы uwsgi /usr/lib/systemd/system/mysqld.service:

==================================



запуск mysql server:

sudo systemctl start mysqld

проверка статуса запущенного демона mysqld:

sudo systemctl status mysqld

sudo systemctl disable mysqld - отменяет автозапуск при перезагрузке

mysqladmin -u root -p version - информация об установленной версии

Команды:

поиск sudo find / -name mysql
ищем адрес:
/usr/local/mysql-5.7.20-macos10.12-x86_64/bin/mysql

Добавляем в .bash_profile ссылку на .bachrc
source $HOME/.bashrc


Прописываем в .bashrc
PATH=${PATH}:/usr/local/mysql-5.7.20-macos10.12-x86_64/bin/
export PATH

коннектимся к сервер (# mysql –u user_name –p user_password или # mysql -hхост -u user_name -puser_password или mysql -uusername -ppassword -hlocalhost)
$ mysql -u root -p;

Частые команды:

Задание пароля
mysql> UPDATE user SET Password=PASSWORD ('НОВЫЙ_ПАРОЛЬ') WHERE user='root';

Новая база данных
mysql> CREATE DATABASE ИМЯ_БАЗЫ CHARACTER SET utf8 COLLATE utf8_general_ci; (mytestdb)

Создание нового пользователя.
mysql> create user 'stepanich'@'localhost' identified by 'Stepanich_competition2001';

Предоставление пользователю доступа к базе данных
mysql> GRANT ALL PRIVILEGES ON Stepanich.* to 'stepanich'@'localhost';

Вступление в силу новых полномочий:
mysql> FLUSH PRIVILEGES;
Создание пльзователя с провами для доступа к базе данных


mysql> GRANT ALL PRIVILEGES ON mytestdb.* TO 'stepanych'@'localhost' IDENTIFIED BY 'stepanych';

Список баз данных
mysql> SHOW DATABASES;

полная информация о созданной таблице!
mysql> SHOW CREATE TABLE name_db 

Переключение между базами (выбор конкретной базы)
mysql> use new_db;

вывести список таблиц в MySQL, для выбранной базы
mysql> show tables;

вывести данные по таблице:
mysql> describe table_name;

удалить базу данных в MySQL
mysql> DROP DATABASE db_name;

сделать дамп базы в MySQL
$ mysqldump --user=user_name --password=user_password db_name > /path_to_dump/dump.sql;

Как залить данные из дампа в MySQL
$ mysql -u user_name -puser_password -f db_name < /path_to_dump/dump.sql

скопировать данные из одной таблицы в другую в MySQL
mysql> INSERT INTO `table_one` (id, parent_id, text) SELECT id, parent_id, option FROM `table_two`;

Показать данные о кодировке таблице 
mysql> show create table tablename;

Поменять кодировку таблицы
mysql> alter table `tablename` charset "utf8";

mysql>show processlist;
mysql>kill process_id;

Отображение русских букв 
SET NAMES utf8; - чаще для линуксовых консолей
SET NAMES cp866; - для cmd windows









