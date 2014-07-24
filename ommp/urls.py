from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'hike.views.index'),
                       url(r'^deployment/side/$', 'hike.views.side'),
                       url(r'^deployment/welcome/$', 'hike.views.welcome'),
                       url(r'^deployment/deploy-php/$', 'hike.views.deploy'),
                       url(r'^deployment/$', 'hike.views.deploy_index'),
                       url(r'^functions/logs/$', 'hike.views.view_logs'),
    # Examples:
    # url(r'^$', 'hike.views.home', name='home'),
    # url(r'^hike/', include('hike.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
