# OpenCMDB项目介绍

    OpenCMDB是一个完全开源的CMDB管理系统，遵循DevOps理念，立足于ITSM构建自动化运维的基石。
	这是一个完全社区性质的项目，欢迎熟悉Python、VUE.js、Django的朋友们参与，共同推进！

## 项目成员：
    Product Owner：赵班长
	Scrum Team：
	前端：欢迎参与
	后端：周伟
	
## 开发环境：

	  - Python-3.5.2
	  - Django-1.10.4
	  - MongoDB
	  - MySQL


# 环境部署

## MongoDB部署（在OpenCMDB中，MongoDB用于存放CI模型和相关数据）：


	[root@linux-node3 ~]# yum install -y mongodb-server mongodb npm
	[root@linux-node3 ~]# systemctl start mongod
	[root@linux-node3 ~]# systemctl enable mongod
	> use cmdb
		switched to db cmdb
	> db.addUser("cmdb", "cmdb");
	


## MySQL 部署（在OpenCMDB中，MySQL用于存放CMDB管理相关数据）：

	[root@linux-node3 ~]# systemctl start mariadb
	[root@linux-node3 ~]# systemctl enable mariadb
	MariaDB [(none)]> create database cmdb character set utf8 collate utf8_bin;
	MariaDB [(none)]> grant all on cmdb.* to cmdb@localhost identified by 'cmdb';
	MariaDB [(none)]> grant all on cmdb.* to cmdb@'%' identified by 'cmdb';


## Nginx部署
	
	[root@linux-node3 ~]# yum install -y nginx
     [root@linux-node3 ~]# cd /etc/nginx/default.d/

	

## Python 3.5.2安装：

	[root@linux-node3 ~]# yum install -y gcc glibc make openssl-devel mariadb-devel
	[root@linux-node3 ~]# cd /usr/local/src/
	[root@linux-node3 src]# wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
	[root@linux-node3 src]# tar zxf Python-3.5.2.tgz && cd Python-3.5.2
	[root@linux-node3 Python-3.5.2]# ./configure --prefix=/usr/local/python-3.5.2
	[root@linux-node3 Python-3.5.2]# make && make install


## Python 虚拟环境部署：


	[root@linux-node3 ~]# /usr/local/python-3.5.2/bin/pyvenv /opt/cmdb_runtime
	[root@linux-node3 ~]# cd /opt/cmdb_runtime/
	[root@linux-node3 ~]# git clone git@github.com:unixhot/opencmdb.git
	[root@linux-node3 cmdb_runtime]# source bin/activate
	(cmdb_runtime) [root@linux-node3 cmdb_runtime]# pip install -r cmdb/requirements.txt 

	
## 配置文件变更：

	(cmdb_runtime) [root@linux-node3 cmdb_runtime]# vim cmdb/CMDB/settings.py
		ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.56.13']
		mongodb_url=config('MONGODB_URL', '192.168.56.13')
		MONGODB_DATABASES = {
			"default": {
				"name": 'mongotest',
				"host": mongodb_url,
				# "host": '127.0.0.1',        
				"password": 'mongotest',
				"username": 'mongotest',
				"tz_aware": True,  # if you using timezones in django (USE_TZ = True)
			}
			
	(cmdb_runtime) [root@linux-node3 cmdb]# python manage.py migrate

