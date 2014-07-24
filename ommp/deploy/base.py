#coding: utf-8
from StringIO import StringIO
import paramiko 
import setting as st
import os
import subprocess

class SshClient:
    "A wrapper of paramiko.SSHClient"
    TIMEOUT = 4

    def __init__(self, host, port, username, password, key=None, passphrase=None):
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key is not None:
            key = paramiko.RSAKey.from_private_key(StringIO(key), password=passphrase)
        self.client.connect(host, port, username=username, password=password, pkey=key, timeout=self.TIMEOUT)

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None
            
    def execute(self, command, sudo=False):
        feed_password = False
        if sudo and self.username != "root":
            command = "sudo -S -p '' %s" % command
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        return {'out': stdout.readlines(), 
                'err': stderr.readlines(),
                'retval': stdout.channel.recv_exit_status()}
        
def GetPostValve(request):
    val = {'project' : request.get('project', ''),
        'type' : request.get('type', ''),
        'resource' : request.get('resource', ''),
        'reason' : request.get('reason', ''),
        'people' : request.get('people', ''),
        }
    
    return val

def GetChannel(host, port, username, password):
    channel = SshClient(host = host, port = port, username = username, password = password)
    return channel

def CloseChannel(channel):
    return channel.close()

def GetCommand(type, conf, host = None):
    command = ''
    if type == 'pre-deploy':
        command = 'bash %s' % (conf['script'])
    elif type == 'official':
        exclude = '" --exclude "'.join(conf['exclude'])
        command = 'cd %s;' % (conf['resource'])
        command += 'rsync -azxl --delete --exclude "%s" ./ ' % (exclude)
        command += '%s@%s:%s' % (st.JENERAL_CONF['username'], host, conf['target'])
    
    return command

def do_deploy(conf, command):
    pass

def bash(channel, command):
    pass

def local(command):
    pipe = subprocess.PIPE
    p = subprocess.Popen('%s' % (command), stdout = pipe, stderr = pipe, shell = True)
    out, err = p.communicate()
    return out, err

def get_config(project):
    if project == 'website':                                            #HIKe_website
        conf = st.WEBSITE_CONF
    elif project == 'bbs':                                            #HIKe_bbs
        conf = st.BBS_CONF
    elif project == 'weixin':                                            #HIKe_website_mobile
        conf = st.WEIXIN_CONF
    elif project == 'media':                                            #HIKe_media
        conf = st.MEDIA_CONF
    elif project == 'enweb':                                              #HIKe_weisite_en
        conf = st.ENWEB_CONF
    elif project == 'cms':                                                #HIKe_CMS
        conf = st.CMS_CONF
    else: conf = None
    
    return conf

def GetGeneralInfo():
    info = st.JENERAL_CONF
    port, username, password = info['port'], info['username'], info['password']
    return port, username, password

def sudo(channel, command, sudo = True):
#    print 'execute command "sudo %s"' % (command)
    return channel.execute(command, sudo)


def format_output(output):
    return output.read().replace('\n', '<br />')

def write_deploy_log():
    pass


            

    
    






















    