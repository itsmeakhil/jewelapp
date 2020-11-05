from django.conf.urls import url

from agent import views

urlpatterns = [

    url(r'^get-agent/$', views.GetAgent.as_view(), name='get_customer'),
    url(r'^contact-status/$', views.GetContactStatus.as_view(), name='contact'),
    url(r'^phone-status/$', views.GetPhoneNumberStatus.as_view(), name='phone_number_status'),
    url(r'^agent-status/update/$', views.UpdateAgentStatus.as_view(), name='Update_status'),
    url(r'^agent-phone/status/update/$', views.UpdatePhoneNumberStatus.as_view(), name='update_phone_status'),
    url(r'^add-answer/$', views.AddQuestionAnswer.as_view(), name='add_answer'),
    url(r'^add-answer/remarks/$', views.AddQuestionRemarks.as_view(), name='add_answer_remarks'),
    url(r'^files/$', views.AddBulkAgents.as_view(), name='files'),
    url(r'^add-agent-remarks/$', views.AddAgentsRemarks.as_view(), name='agent_remarks'),
]
