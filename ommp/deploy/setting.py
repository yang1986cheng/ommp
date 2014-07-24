#coding: utf-8
JENERAL_CONF = {'username' : 'ckt', 
                'password' : '123qwe',
                'port' : 22,
                }

WEBSITE_CONF = {'exclude' : ['.git', '.gitignore', 'config.py', 'fabfile.py', 'admin', 'hikeuc/admin.php',], 
            'hosts' : [],
            'resource' : '/app/webapps/hike',
            'target' : '/app/webapps/hike', 
            'verification' : 'admin',
            'script' : '/app/webapps/pre_deploy.sh',
            'static' : {'./js/' : '/app/webapps/media/js', 
                        './images/home/' : '/app/webapps/media/images/home', 
                        './style/' : '/app/webapps/media/style', 
                        './images/index/' : '/app/webapps/media/images/index',
                        }, 
            'static_host' : ['10.120.10.32',],
            }

WEIXIN_CONF = {'exclude' : ['.git', '.gitignore', 'config.py', 'fabfile.py', ], 
               'hosts' : [],
               'resource' : '/app/webapps/hike_weixin',
               'target' : '/app/webapps/hike_weixin', 
               'verification' : 'admin',
               'script' : '/app/webapps/pre_weixin.sh',
            }

ENWEB_CONF = {'exclude' : ['.git', '.gitignore', 'config.py', 'fabfile.py', 'admin', 'hikeuc/admin.php',], 
           'hosts' : [],
           'resource' : '/app/webapps/hike_en',
           'target' : '/app/webapps/hike_en', 
           'verification' : 'admin',
           'script' : '/app/webapps/pre_en.sh',
            }

CMS_CONF = {'exclude' : ['.git', '.gitignore', 'config.py', 'fabfile.py', 'admin', 'hikeuc/admin.php',], 
            'hosts' : [],
            'resource' : '/app/webapps/hike',
            'target' : '/app/webapps/hike', 
            'verification' : 'admin',
            'script' : '/app/webapps/pre_cms.sh',
            }

MEDIA_CONF = {'exclude' : ['.git', '.gitignore', 'config.py', 'fabfile.py', 'admin', 'hikeuc/admin.php',], 
              'hosts' : ['10.169.0.120',],
              'resource' : '/app/webapps/hike_media',
              'target' : '/app/webapps/hike_media', 
              'verification' : 'admin',
              'script' : '/app/webapps/pre_media.sh',
            }

BBS_CONF = {'exclude' : ['.git', '.gitignore', 'config.py', 'fabfile.py', 'data/attachment', 'data/attachment_local', 'data/diy', 'admin', 'admin.php'], 
            'hosts' : ['10.120.10.32', '10.120.10.36', ],
            'resource' : '/app/webapps/hike_bbs_x3',
            'target' : '/app/webapps/hike_new', 
            'verification' : 'admin',
            'script' : '/app/webapps/pre_bbs.sh',
            }
