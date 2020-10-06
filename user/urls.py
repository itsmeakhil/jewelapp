from django.conf.urls import url

from user import views

urlpatterns = [

    url(r'^logout/$', views.UserLogout.as_view(), name='users_logout'),
    url(r'^login/$', views.UserLogin.as_view(), name='user_login'),
    url(r'^v1/login/$', views.UserLoginV1.as_view(), name='user_login_v1'),

]
