#coding=utf-8

#import threading
#
#class Deploy(threading.Thread):
#    def __init__(self, thread_count, before_command = None, deploy_command, after_command = None):
#        self.thread_count = thread_count
#        self.before_command = before_command
#        self.deploy_command = deploy_command
#        self.after_command = after_command

import threading
import time

class MyThread(threading.Thread):
    def run(self):
        global num
        time.sleep(1)
        if mutex.acquire(1):
            num = num+1
            msg = self.name+' set num to '+str(num)
            print msg
            mutex.release()
            
num = 0
mutex = threading.Lock()

def test():
    for i in range(5):
        t = MyThread()
#        t.setDaemon(True)
        t.start()
#        t.join()
        if i == 4:
            t.join()
        
    
if __name__ == '__main__':
    test()
    print 'threading.activeCount()'



#x =  {'addition_args': '', 
#      'target_dir': '/app/wepapps/hike/', 
#      'threads': '3', 'temporary_dir': '', 
#      'source_dir': '/app/wepapps/hike/', 
#      'name': 'hike_pre_deploy', 
#      'is_backup': '0', 
#      'target_type': '2', 
#      'after_operations': '', 
#      'hosts': '[]', 
#      'login_user': '', 
#      'exclude_files': ''
#      }
#
#print x

#from hashlib import md5
#
#def md5_file(name):
#    m = md5()
#    with open(name, 'rb') as a_file:
#        m.update(a_file.read())
#    return m.hexdigest()
#
#
#print len(md5_file('/home/leal/workspace/ommp/manage.py'))

#import os
#
#
#x = '/home/leal/hike//'
#
#print os.path.abspath(os.path.join(x, 'a.txt'))

#hosts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13,14,15,16,17,18]
#
#
#threads = 20
#host_count = len(hosts)
#
#host_count_per_thread = host_count / threads
#
#threads = host_count if threads > host_count else threads
#host_count_per_thread = host_count / threads
##threads = threads + 1 if host_count % threads != 0 else threads
#
#t = []
#
#for i in range(0, threads):
#    t.append(hosts[0:host_count_per_thread])
#    del hosts[0:host_count_per_thread]
#    
#for i in range(0, len(hosts)):
#    t[i].append(hosts[i])
#    
#    
#print t
    
#import os
#
#print os.path.basename(os.path.abspath('/home/leal/'))






















