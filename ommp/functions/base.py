#coding: utf-8
import setting as st
import threading


class WatchLogs(threading.Thread):
    def __init__(self, channel, wor, project, logfile, tempfile ):         #wor, write or read the temporary file
        self.channel = channel
        self.wor = wor
        self.project = project
        self.logfile = get_log_file_path(self.project, logfile)
        self.tempfile = tempfile
        
    def run(self):
        if self.wor == 'w':
            self.channel.execute("pkill tail; [ -f %s ] && rm -rf %s; tail -f %s >> %s" % (self.tempfile, self.tempfile, self.logfile, self.tempfile))
#            return "[ -f %s ] && rm -rf %s; tail -f %s >> %s" % (self.tempfile, self.tempfile, self.logfile, self.tempfile)
        elif self.wor == 'r':
            stdout = self.channel.execute("cat %s; > %s" % (self.tempfile, self.tempfile))
            return stdout['out']
#            return "cat %s; > %s" % (self.tempfile, self.tempfile)
        
    def stop(self):
        self.channel.execute("[ -f %s ] && rm -rf %s;" % (self.tempfile))
        self.channel.close()



def get_log_list(channel, project):
    pro_info = st.JAVA_PROJECTS[project]
    stdout = channel.execute('ls %s' % (pro_info['logs_dir']))
    return stdout['out']

def get_config(project):
    return st.JAVA_PROJECTS[project]

def get_connection_info():
    return st.CONNECTION_INFO

def get_log_content(channel, project, filename):
    file_path = get_log_file_path(project, filename)
    stdout = channel.execute('cat %s' % (file_path))
    return stdout['out']

def get_log_file_path(project, filename):
    pro_info = st.JAVA_PROJECTS[project]
    file_path = pro_info['logs_dir'] + "/" + filename
    return file_path