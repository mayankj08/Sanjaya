from django.conf.urls.defaults import patterns, include, url
from bep.bep_users.views import home,profile,register,logout1,success,contactus,feedback,listen
from bep.stories.views import effects,edit,st,search_story,record,rec_search,aud,add_effects,adde,frnde,cchanges
from django.contrib import admin
from bep.stories.models import story
from bep.stories.views import recording
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bep.views.home', name='home'),
    # url(r'^bep/', include('bep.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
url(r'^admin/', include(admin.site.urls)),
(r'^home/$', home),
(r'^profile/$',profile),
(r'^profile/([a-zA-Z ]+[0-9]*)/$',st),
(r'^register/$',register),
(r'^logout1/$',logout1),
(r'^success/$',success),
(r'^recording/$',recording),
(r'^contactus/$',contactus),
(r'^feedback/$',feedback),
(r'^listen/$',listen),
(r'^aud/$',aud),
#(r'^st/',st),
(r'^search_story/$',search_story),	
#(r'^uploading/$',
#(r'^handle_uploaded_file/$',handle_uploaded_file),
(r'^effects/$',effects),
(r'^edit/',edit),
(r'^record/',record),
(r'^rec_search/',rec_search),
(r'^add_effects/([a-zA-Z ]+[0-9]*)/$',add_effects),
(r'^adde/([a-zA-Z ]+[0-9]*)/$',adde),
(r'^frnde/([a-zA-Z ]+[0-9]*)/$',frnde),
(r'^confirm_changes/([a-zA-Z ]+[0-9]*)/$',cchanges),

)
