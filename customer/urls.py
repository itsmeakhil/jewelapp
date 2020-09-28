from django.conf.urls import url

from customer import views

urlpatterns = [

    url(r'^get_customer/$', views.GetCustomer.as_view(), name='get_customer'),
    url(r'^status/update/$', views.UpdateCustomerStatus.as_view(), name='Update_status'),
]
