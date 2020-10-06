from django.conf.urls import url

from questions import views

urlpatterns = [

    url(r'^get-questions/$', views.GetQuestions.as_view(), name='get_questions'),
]
