JENERAL_CONF = {'username' : 'ckt', 
                'password' : '123qwe',
                'port' : 22,
                }

WEBSITE_CONF = {'exclude' : ['.git', '.gitignore', 'config.py', 'fabfile.py', 'admin', 'hikeuc/admin.php',], 
            'hosts' : ['10.169.0.61', '10.169.0.63', '10.169.0.65', '10.169.0.66', 
                       '10.169.0.69', '10.169.0.70', '10.169.0.71', '10.169.0.72',
                       '10.169.0.75',],
            'resource' : '/app/webapps/hike',
            'target' : '/app/webapps/hike', 
            'verification' : 'admin',
            'script' : '/app/webapps/pre_deploy.sh',
            }

WEIXIN_CONF = {'exclude' : ['.git', '.gitignore', 'config.py', 'fabfile.py', ], 
               'hosts' : ['10.169.0.73', '10.169.0.74', '10.169.0.78',],
               'resource' : '/app/webapps/hike_weixin',
               'target' : '/app/webapps/hike_weixin', 
               'verification' : 'admin',
               'script' : '/app/webapps/pre_weixin.sh',
            }

ENWEB_CONF = {'exclude' : ['.git', '.gitignore', 'config.py', 'fabfile.py', 'admin', 'hikeuc/admin.php',], 
           'hosts' : ['10.169.0.67', '10.169.0.68',],
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
            'hosts' : ['10.169.0.201'],
            'resource' : '/app/webapps/hike_bbs_x3',
            'target' : '/app/webapps/hike_new', 
            'verification' : 'admin',
            'script' : '/app/webapps/pre_bbs.sh',
            }

MOBILE_CONF = {'exclude' : ['.git', '.gitignore', 'config.py', 'fabfile.py', 'admin', 'admin.php'], 
            'hosts' : ['10.169.0.64'],
            'resource' : '/app/webapps/hike_m',
            'target' : '/app/webapps/hike_m', 
            'verification' : 'admin',
            'script' : '/app/webapps/pre_mobile.sh',
            }