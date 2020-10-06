from django.contrib import admin

# Register your models here.
from questions.models import Question, QuestionOption, CustomerAnswers

admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(CustomerAnswers)
