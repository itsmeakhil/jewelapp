from django.conf.urls import url

from customer import views

urlpatterns = [

    # url(r'^get-agent/$', views.GetAgent.as_view(), name='get_customer'),
    url(r'^customer-phone/status/update/$', views.UpdatePhoneNumberStatus.as_view(), name='update_phone_status'),
    url(r'^add-customer-remarks/$', views.AddCustomerRemarks.as_view(), name='customer_remarks'),
    url(r'^add-customer/$', views.AddCustomer.as_view(), name='add_customer'),
]
