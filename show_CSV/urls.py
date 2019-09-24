from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('show_CSV/$', views.deal_post, name='deal_post'),
    # url(r'index/$', views.index, name='index'),
    # url(r'postTest/$', views.postTest, name='postTest'),
    url(r'deal_post/$', views.deal_post, name='deal_post'),
    # path('deal_post/', views.deal_post,name='deal_post'),
    # url(r'postTest/', views.postTest),
]
