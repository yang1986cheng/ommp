from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'ommp.views.index'),
                       url(r'^deployment/side/$', 'ommp.views.side'),
                       url(r'^deployment/welcome/$', 'ommp.views.welcome'),
                       url(r'^deployment/deploy-php/$', 'ommp.views.deploy'),
                       url(r'^deployment/$', 'ommp.views.deploy_index'),
                       url(r'^functions/logs/$', 'ommp.views.view_logs'),
                       url(r'^resource/idc/$', 'ommp.resources.views.list_idc'),
                       url(r'^resource/add-idc/$', 'ommp.resources.views.add_idc'),
                       url(r'resource/idc-detail/$', 'ommp.resources.views.get_idc_detail'),
    # Examples:
    # url(r'^$', 'hike.views.home', name='home'),
    # url(r'^hike/', include('hike.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
