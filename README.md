Требования для установки приложения Stepanych (описана установка на CentOS7)
На сервере должны быть усановлены:
-База данных MySQL(recomended) или SQLight (помощь по работе c MySQL в файле MySQL tips.txt)
-виртуальное окружение с установленным python 3.6 и pip (инструкция по установке и настройке в файле python_venv_uwsgi.txt)
-application server UWSGI (инструкция по установке и настройке в файле python_venv_uwsgi.txt)
-web-server (например NGINX который взаимодействует с UWSGI по unix-socket. инстуркция по настройке Nginx в файле nginx configuration.txt)
-почтовый сервер, есле нужен почтовый ящик на домене stepanich.ru (не обязательно, можно настроить отправку писем и через gmail/mail.ru/yandex)
-информаци по настройке служб (запуск, остановка, добавление в автозагрузку и т.п. в файле system services setup (CentOS7).txt)
-установленный git
Открытые порты:
22 - ssh
25 - postfix (smtp port)
80 - nginx (http)
443 -  nginx (shttp)
993 - dovecot (pop3 port)
995 - dovecot (pop3 port)
3306 - mysql
110 - dovecot (pop3 port)
143 - dovecot (pop3 port)
587 - posfix (smpt submission port)

Установка:
в корневом каталоге проекта инициализируем новый репозиторий git и клонируем приложение с github.com:
$ git init
$ git clone https://github.com/ReshetnyakRoman/Stepanych-package

распаковываем все из каталога пакета в каталог прокта и удаляем пустой каталог 
$ mv Stepanych-package/* /home/flask
$ rm Stepanych-package/ -r

преименовываем файл config.py в config_dev.py а файл config_prod.py в config.py
$ mv config.py config_dev.py
$ mv config_prod.py config.py
преименовываем файл manage.py в manage_dev.py а файл manage_prod.py в manage.py
$ mv manage.py manage_dev.py
$ mv manage_prod.py manage.py

создаем error.log для uwsgi и присваеваем ему нужного пользователя
$sudo touch /home/flask/error.log
$sudo chown nginx:flask-uwsgi error.log

в файле для запуска uwsgi сервера проверяем путь к файлу manage.py на запуск приложения  
$ sudo nano uwsgi.ini
wsgi-file = /home/flask/manage.py

в файле manage.py при необходимости можно указать кокой конфиг загружать (proudction/testing/development)

в базе данных, пусть это будет MySQL создаем пользователя и базу данных для нашего приложения:
в примере база данных Stepanich_db, пользовател stepanich_mysql_user и пароль strong_password
mysql> GRANT ALL PRIVILEGES ON Stepanich_db.* TO 'stepanich_mysql_user'@'localhost' IDENTIFIED BY 'strong_password';

в файле config.py прописываем доступ к базам данных (созданного выше ползьователя и базу данных MySQL):
Пример того как должен выглядеть формат: (меяем строчку 50)
	class ProductionConfig(Config):
		SQLALCHEMY_DATABASE_URI = 'mysql://stepanich_mysql_user:strong_password@localhost/Stepanich_db?charset=utf8'

в том же файле находим и прописываем настройки для отправки email-ов, нужно указать почтовый сервер, логин и пароль пользователя.
	MAIL_SERVER = '102.23.234.21'
	MAIL_USE_TLS = True
	MAIL_PORT = 25
	MAIL_USERNAME = 'mail_user_name' # os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = 'mail_user_password' # os.environ.get('MAIL_PASSWORD')

Может бытль обычный gmail, например:
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_USE_TLS = True
	MAIL_PORT = 587
	MAIL_USERNAME = 'gmail_user@gmail.com' # os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = 'gmail_password' # os.environ.get('MAIL_PASSWORD')	



останавливаем сервер uwsgi если он запущен
$ sudo systemctl stop flask-uwsgi

устанавливаем пакет для взаимодействия mysql-python
$ sudo yum install python-devel mysql-devel

заходим в виртуальное окружение
$ source venv-pyth3/bin/activate

устанавливаем необходимые для работы преложения пакеты (это занимает несколько минут):
(venv-pyth3)$ pip install -r Stepanych/requirements/common.txt

запускаем приложение в энторпритаторе с консолью, что бы создать базы данных:
(venv-pyth3)$ python manage.py shell

в интерпритаторе даем команду для создания всех таблиц:
>>> db.create_all()
>>> exit ()

выходим из окружения:
(venv-pyth3)$ deactivate


Для наполнения базы данных есть два пути:
1) если мы ходтим востановить все данные их sql-backup файла то просто накатываем его на MySQL и все должно заработать (см. раздел Backup)
2) если мы хотим завести все с нуля с читой базой данных и без архивов про предыдущим соревнованиям то:
логинимся в mysql, что-бы добавить пользователя админа и типы прав, соревнования:
$ mysql -u stepanich_mysql_user -p

mysql> use Stepanich_bd;


mysql>insert into roles (role, permissions) values('admin',255);
mysql>insert into roles (role, permissions) values('guest',4);
mysql>insert into roles (role, permissions) values('user',3);

mysql>insert into competition (competitionName, competitionStatus, routesStatus) values ('Stepanych','closed','0');

mysql>insert into main (keyTeamCompetition, competition, email, teamName, confirmed, role, year1, year2) values('Stepanychadmin','Stepanych','admin_email@gmail.com','admin','True','admin', 1990, 1990); 

INSERT INTO setDescriptions (description, setNuber) values ('сет', 0);

!! После запуска сайта нужно будет изменить пароль пользователя admin --> нажать "Войти" и выбрать "забыли пароль"!!

========Запускаем сайт!======
запускаем службы (прежде чем их запустить нужно проверить что существуют соответствующие сервисные файлы см.ниже)
$ sudo systemctl start flask-uwsgi
$ sudo systemctl start nginx
$ sudo systemctl start mysqld
$ sudo systemctl start postfix
$ sudo systemctl start dovecot

проверяем статуч, что все они успешно запустились
$ sudo systemctl status flask-uwsgi
$ sudo systemctl status nginx
$ sudo systemctl status mysqld
$ sudo systemctl status postfix
$ sudo systemctl status dovecot

если статус выдал ошибку, ее полностью можно посмотреть в журнал:
$sudo journalctl -u service-name.service  - весь журнал 
$sudo journalctl -u service-name.service -b - последняя загрузка

добавляем службы в автозагрузку
$ sudo systemctl enable flask-uwsgi
$ sudo systemctl enable nginx
$ sudo systemctl enable mysqld
$ sudo systemctl enable postfix
$ sudo systemctl enable dovecot



Что бы проверить что СИСТЕМНАЯ служба в автозагрузках, нужно что бы они присутствовала в катлоге /usr/lib/systemd/system/
Смотрим что там есть файлы:
nginx.service
mysqld.service
postfix.service - если используется местная почта.
dovecot.service - если используется местная почта.
dovecot.socket - если используется местная почта.

А наша самодельная служба находится в /etc/systemd/system :
flask-uwsgi.service




1) Файл nginx.service должен существовать и  быть таким:
$ sudo nano /usr/lib/systemd/system/nginx.service

------File start----
[Unit]
Description=The nginx HTTP and reverse proxy server
After=network.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
PIDFile=/var/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t -c /etc/nginx/nginx.conf
ExecStart=/usr/sbin/nginx -c /etc/nginx/nginx.conf
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
-------file end-----


2) файл flask-uwsgi.service должен существовать и  быть таким flask-uwsgi:
$ sudo nano /etc/systemd/system/flask-uwsgi.service


------File start----
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
-------file end-----

3) Файл postfix.service должен существовать и  быть таким:
$ sudo nano /usr/lib/systemd/system/postfix.service
------File start----
[Unit]
Description=Postfix Mail Transport Agent
After=syslog.target network.target
Conflicts=sendmail.service exim.service

[Service]
Type=forking
PIDFile=/var/spool/postfix/pid/master.pid
EnvironmentFile=-/etc/sysconfig/network
ExecStartPre=-/usr/libexec/postfix/aliasesdb
ExecStartPre=-/usr/libexec/postfix/chroot-update
ExecStart=/usr/sbin/postfix start
ExecReload=/usr/sbin/postfix reload
ExecStop=/usr/sbin/postfix stop

[Install]
WantedBy=multi-user.target

------File end----

4) Файл dovecot.service должен существовать и  быть таким:
$ sudo nano /usr/lib/systemd/system/dovecot.service
------File start----
[Unit]
Description=Dovecot IMAP/POP3 email server
After=local-fs.target network.target network-online.target

[Service]
Type=simple
ExecStartPre=/usr/libexec/dovecot/prestartscript
ExecStart=/usr/sbin/dovecot -F
ExecReload=/bin/kill -HUP $MAINPID
PrivateTmp=true
NonBlocking=yes

[Install]
WantedBy=multi-user.target
------File end----


5) Файл mysqld.service должен существовать и  быть таким:
$ sudo nano /usr/lib/systemd/system/mysqld.service
------File start----
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target

[Install]
WantedBy=multi-user.target

[Service]
User=mysql
Group=mysql

Type=forking

PIDFile=/var/run/mysqld/mysqld.pid

# Disable service start and stop timeout logic of systemd for mysqld service.
TimeoutSec=0

# Execute pre and post scripts as root
PermissionsStartOnly=true

# Needed to create system tables
ExecStartPre=/usr/bin/mysqld_pre_systemd

# Start main service
ExecStart=/usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid $MYSQLD_OPTS

# Use this to switch malloc implementation

ссылка на иконки
https://www.w3schools.com/icons/icons_reference.asp
EnvironmentFile=-/etc/sysconfig/mysql

# Sets open_files_limit
LimitNOFILE = 5000

Restart=on-failure

RestartPreventExitStatus=1

PrivateTmp=false
------File end----

======Логи=====
Логи пишутся в:
/home/flask/error.log   uwsgi server error log
/var/log/nginx/error.log


tail /home/flask/error.log
sudo tail /var/log/nginx/error.log

=====BackUP=====
MySQL backup 
в консоле вводим:
заходим в папку проекта:
$ cd /home/flask/
создаем backup file:
$ mysqldump -u stepanich -p  Stepanich -R -E --single-transaction --triggers >Stepanich_backup.sql
файл сохраняется в той же папке из которой вводилась команда.

здесь 
пользователь: stepanich
сохраняем базу данных Stepanich
-R for all routines
-E for all Events
--single-transaction - without locking the table i.e., without interrupting any connection(R/W)

Восстановление базы данных:
1) На целевой машине создается база данных с таким же именем:
mysql> GRANT ALL PRIVILEGES ON Stepanich.* TO 'stepanich_mysql_user'@'localhost' IDENTIFIED BY 'strong_password';

2) Загрузить файл в MySQL командой (при этом нужно быть в папке в которой находится файл):
$ mysql -u [uname] -p[pass] [db_to_restore] < [backupfile.sql]
в нашем случае:
$ mysql -u stepanich -p Stepanich < Stepanich_backup.sql

Если нужно создать базу данных которая уже существует то синтаксис команды следующий:
mysqlimport -u [uname] -p[pass] [dbname] [backupfile.sql]

Архивация папок img & doc
сжатие общий вид:
$ tar -jcvf archive_name.tar /path/to/directory_to_compress
разархивирование:
$ tar -xvf archive_name.tar

Наш случай добавления архива:
$ cd /home/flask/
$ tar -jcvf img_backup.tar /home/flask/Stepanych/img/
$ tar -jcvf doc_backup.tar /home/flask/Stepanych/doc/