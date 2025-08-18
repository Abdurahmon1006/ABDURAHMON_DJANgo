from django.urls import path
from apps.views import *

from ABDURAHMON_DJANgo.apps.views import *

urlpatterns = [
    path('', home, name='index'),
    path('components/',components,name='components'),
    path('contact/',contact,name='contact'),
    path('work/',work,name='work'),
    path('works/',works,name='works'),
    path('about/',about,name='about'),
    path('secretpage/',secretpage,name='secret'),
    path('yutuq/<int:id>/', yutuq_detail, name='yutuq_detail'),
]
