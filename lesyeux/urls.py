from django.conf.urls import url
from lesyeux import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^view/', views.neighborhoods, name='neighborhoods'),
    url(r'^(?P<neighborhood_slug>[\w\-]+)/$', views.show_neighborhood, name = 'show_neighborhood'),
    url(r'^create_neighborhood/', views.create_neighborhood, name='create_neighborhood'),          
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    
]