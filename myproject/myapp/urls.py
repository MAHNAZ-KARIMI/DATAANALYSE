from django.urls import path

from . import views	

urlpatterns = [
    path('start', views.algoritm_to_zip, name='do_thing'),
    path('', views.index, name='index'),
    path('message', views.show_Message, name='message')

]