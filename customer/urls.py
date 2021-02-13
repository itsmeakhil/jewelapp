from django.urls import path

from customer import views

urlpatterns = [

    path('customers/', views.Customer.as_view(), name='customer'),
    path('update-phone_number/<int:pk>/', views.UpdatePhoneNumber.as_view(), name='update phone number'),
    path('customer-details/<int:pk>/', views.CustomerDetails.as_view(), name='customer_details'),
    path('assign-customers/', views.AssignCustomers.as_view(), name='assign_customer'),
    path('get-customer-by-user/', views.GetCustomersByUser.as_view(), name='get_customer_by_user'),
    path('get-customer-by-user/<int:pk>/', views.GetCustomersByAssignedUser.as_view(), name='get_customer_by_user_id'),
    path('get-customer-list/', views.GetCustomersList.as_view(), name='get_customer_list'),
    path('customer-phone/status/update/', views.UpdatePhoneNumberStatus.as_view(), name='update_customer_phone_status'),
    path('customer-status/update/', views.UpdateCustomerStatus.as_view(), name='update_customer_status'),
    path('add-customer-remarks/', views.AddCustomerRemarks.as_view(), name='customer_remarks'),
    path('field-report/', views.FieldReportViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    }), name='field_report'),
    path('field-report-details/<int:pk>/', views.FieldReportViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    }), name='field_report_details'),
    path('get-customers/', views.GetCustomersWithFieldReport.as_view(), name='get_customer'),
    path('customer-details-with-report/<int:pk>/', views.GetCustomersWithFieldReportDetails.as_view(),
         name='customer_details_with_report'),
    path('customers/bulk-insert/', views.CustomerBulkInsert.as_view(), name='customer-insert'),

]
