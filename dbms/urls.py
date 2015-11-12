from django.conf.urls import patterns, include, url
from dbms.views import lnch,signup,signin,check,edit_profile,add_topic,view_all_papers,addschool,welcome,filterpaper,delete_topic,delete_school,logout
from papers.views import upload,viewer,add_comment,search
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dbms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',lnch),
    url(r'^signup/$',signup),
    url(r'^signin/$',signin),
    url(r'^check/$',check),
    url(r'^profile/$',edit_profile),
    url(r'^logout/$',logout),
    url(r'^add_topic', add_topic),
    url(r'^upload/',upload),
    url(r'^viewer/',viewer),
    url(r'^add_comment/',add_comment),
    url(r'^viewall',view_all_papers),
    url(r'^search',search),
    url(r'^addschool',addschool),
    url(r'^welcome',welcome),
    url(r'^filter',filterpaper),
    url(r'^delete_topic',delete_topic),
    url(r'^delete_school',delete_school),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
