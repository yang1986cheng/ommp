ommp
====

OMMP(Operation and maintenance management platform)
集资源管理、任务管理、指令执行、文件同步等功能管理平台
运行环境: python 2.7 django 1.5.1 mysql saltstack

使用方法(开发版):
	1:下载,git clone https://github.com/yang1986cheng/ommp.git
	2:安装依赖库，pip install celery django-celery django-kombu xlrd
	3：安装saltstack--http://docs.saltstack.com/en/latest/topics/installation/index.html
	4:修改ommp/ommp/settings.py DATABASE = {} 项修改为相应值
	5:运行 python manage.py syncdb 初始化数据库 初次安装会要求添加管理员帐号
	6:运行服务器,python manage.py runserver 0.0.0.0:8080
	7:至此配置完成,访问服务器+端口,如:192.168.0.100:8080

说明:
    指令执行模块，是调用saltstack服务进行指令分发（所以需要saltstack支持）、后期有需要再开发独立于saltstack的指令执行功能