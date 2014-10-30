from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
#                       url(r'^admin/', include(admin.site.urls)),
#                       url(r't/', 'ommp.views.test'),
                       url(r'^$', 'ommp.views.index'),
                       url(r'^management/side/$', 'ommp.views.side'),
                       url(r'^management/welcome/$', 'ommp.views.welcome'),
                       url(r'^management/$', 'ommp.views.deploy_index'),
                       
                       #about idcs
                       url(r'^resource/idc/$', 'ommp.resources.views.list_idc'),
                       url(r'^resource/add-idc/$', 'ommp.resources.views.add_idc'),
                       url(r'resource/idc-detail/$', 'ommp.resources.views.get_idc_detail'),
                       url(r'resource/del-idc/$', 'ommp.resources.views.del_idc'),
                       url(r'resource/update-idc/$', 'ommp.resources.views.update_idc_info'),
                       url(r'resource/get-idcs/$', 'ommp.resources.views.get_idcs'),
                       
                       #normal
                       url(r'resource/get-users/$', 'ommp.resources.views.get_users'),
                       url(r'accounts/login/$', login, {'template_name' : 'login.html', 'redirect_field_name' : '/management/'}),
                       
                       #about servers
                       url(r'resource/servers/$', 'ommp.resources.views.servers'),
                       url(r'resource/get-servers/$', 'ommp.resources.views.get_servers'),
                       url(r'resource/add-server/$', 'ommp.resources.views.add_server'),
                       url(r'resource/del-server/$', 'ommp.resources.views.del_server'),
                       url(r'resource/update-server/$', 'ommp.resources.views.update_server'),
                       
                       
                       
                       #about cabinets
                       url(r'resource/cabinets/$', 'ommp.resources.views.cabinets'),
                       url(r'resource/add-cab/$', 'ommp.resources.views.add_cabinet'),
                       url(r'resource/del-cab/$', 'ommp.resources.views.del_cabinet'),
                       url(r'resource/get-cabs/$', 'ommp.resources.views.get_cabinets'),
                       url(r'resource/update-cab/$', 'ommp.resources.views.update_cabinet'),
                       url(r'resource/usable/$', 'ommp.resources.views.get_usable'),
                       
                       #about ipaddr
                       url(r'resource/ipaddr/$', 'ommp.resources.views.ipaddr'),
                       url(r'resource/add-ips/$', 'ommp.resources.views.add_ips'),
                       url(r'resource/get-ips/$', 'ommp.resources.views.get_ips'),
                       url(r'resource/update-ip/$', 'ommp.resources.views.update_ip'),
                       url(r'resource/del-ip/$', 'ommp.resources.views.delete_ip'),
                       url(r'resource/add-ip-relation/$', 'ommp.resources.views.add_ip_relation'),
                       url(r'resource/get-ip-relation/$', 'ommp.resources.views.get_ip_relation'),
                       url(r'resource/del-ip-relation/$', 'ommp.resources.views.del_ip_relation'),
                       url(r'resource/update-ip-relation/$', 'ommp.resources.views.update_ip_relation'),
                       
                       #about project
                       url(r'project/list/$', 'ommp.projects.views.listpro'),
                       url(r'project/add-project/$', 'ommp.projects.views.add_project'),
                       url(r'project/list-projects/$', 'ommp.projects.views.list_projects'),
                       url(r'project/update-project/$', 'ommp.projects.views.update_project'),
                       url(r'project/del-project/$', 'ommp.projects.views.delete_project'),
                       url(r'project/add-pro-ip-relation/$', 'ommp.projects.views.add_pro_ip_relation'),
                       url(r'project/list-pro-ip-relations/$', 'ommp.projects.views.list_pro_ip_relations'),
                       url(r'project/del-pro-ip-relation/$', 'ommp.projects.views.del_pro_ip_relation'),
                       
                       #about salt
                       url(r'functions/exc-command/$', 'ommp.functions.views.exc_command'),
                       url(r'functions/exc-command-handler/$', 'ommp.functions.views.handler_command'),
                       
                       #about task
                       url(r'tasks/tasks/$', 'ommp.task.views.tasks'),
                       url(r'tasks/add-task/$', 'ommp.task.views.add_task'),
                       url(r'tasks/list-tasks/$', 'ommp.task.views.list_templates'),
                       url(r'tasks/add-tasks-to-list/$', 'ommp.task.views.add_task_to_list'),
                       url(r'tasks/update-task/$', 'ommp.task.views.update_task'),
                       url(r'tasks/delete-task/$', 'ommp.task.views.delete_task'),
                       url(r'tasks/in-process/$', 'ommp.task.views.in_process'),
                       url(r'tasks/task-in-process/$', 'ommp.task.views.task_in_process'),
                       
                       #about task controller
                       url(r'tasks/start-process/$', 'ommp.task.views.start_process'),
                       url(r'tasks/pause-process/$', 'ommp.task.views.pause_process'),
                       url(r'tasks/restart-process/$', 'ommp.task.views.restart_process'),
                       url(r'tasks/continue-process/$', 'ommp.task.views.continue_process'),
                       url(r'tasks/end-process/$', 'ommp.task.views.end_process'),
                       url(r'tasks/stop-process/$', 'ommp.task.views.stop_process'),
                       
                       

    # Examples:
    # url(r'^$', 'hike.views.home', name='home'),
    # url(r'^hike/', include('hike.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     
)
