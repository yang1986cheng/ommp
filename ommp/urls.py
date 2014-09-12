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
                       url(r'^management/deploy-php/$', 'ommp.views.deploy'),
                       url(r'^management/$', 'ommp.views.deploy_index'),
                       url(r'^functions/logs/$', 'ommp.views.view_logs'),
                       
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

    # Examples:
    # url(r'^$', 'hike.views.home', name='home'),
    # url(r'^hike/', include('hike.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     
)
