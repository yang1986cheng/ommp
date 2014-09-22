ommp
====
OMMP(Operation and maintenance management platform)
运维管理平台,集资源管理、项目部署、任务管理的集中管理平台
运行环境:
    python 2.7
    django 1.5.1
    mysql

使用方法:
    1:下载,git clone https://github.com/yang1986cheng/ommp.git
    2:修改ommp/ommp/settings.py
	DATABASE  = {} 项修改为相应值
    3:运行 python manage.py syncdb  初始化数据库
	初次安装会要求添加管理员帐号
    4:运行服务器,python manage.py runserver 0.0.0.0:8080
    5:至此配置完成,访问服务器+端口,如:192.168.0.100:8080