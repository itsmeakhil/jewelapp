from django.conf.urls import url

from customer import views

urlpatterns = [

    url(r'^get-customer/$', views.GetCustomer.as_view(), name='get_customer'),
    url(r'^contact-status/$', views.GetContactStatus.as_view(), name='contact'),
    url(r'^status/update/$', views.UpdateCustomerStatus.as_view(), name='Update_status'),
    url(r'^add-answer/$', views.AddQuestionAnswer.as_view(), name='add_answer'),
]
