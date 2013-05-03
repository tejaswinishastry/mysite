from django.conf.urls import *
from blogs.views import *



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'auth.views.login_user'),   
    # below line for handling static content
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/tej/mysite/media'}),
    url(r'^blog/$', frontpage),
    url(r'^blog/(\d{4,4})/(\d{2,2})/([\w\-]+)/$', singlepost),
    url(r'^blog/(\d{4,4})/$', yearview),
    url(r'^blog/(\d{4,4})/(\d{2,2})/$', monthview),
    url(r'^blog/tag/([\w\-]+)/$', tagview),
    url(r'^blog/category/([\w\-]+)/$', categoryview),
    url(r'^$',frontpage),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
)


