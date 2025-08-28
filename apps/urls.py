from django.urls import path



from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('components/',components,name='components'),
    path('contact/',contact,name='contact'),
    path('work/',work,name='work'),
    path('works/',works,name='works'),
    path('about/',about,name='about'),
    path('secretpage/',secretpage,name='secret page'),
    path('balloon/',balloon,name='secret page ballon'),
    path('yutuq/<int:id>/', yutuq_detail, name='yutuq_detail'),
]
