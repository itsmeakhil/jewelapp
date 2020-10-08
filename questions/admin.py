from django.contrib import admin

# Register your models here.
from questions.models import Question, QuestionOption, CustomerAnswers

admin.site.register(Question)


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    """
     Register the CustomerService class in django admin.
    """

    list_display = ('name', 'question', 'is_answer')
    search_fields = ('question', 'name',)
    ordering = ('question',)
    list_filter = ('question',)
    exclude = ['is_delete', 'is_active']


@admin.register(CustomerAnswers)
class CustomerAnswersAdmin(admin.ModelAdmin):
    """
     Register the CustomerAnswers class in django admin.
    """

    list_display = ('customer', 'question', 'option')
    search_fields = ('customer', 'question',)
    ordering = ('question',)
    list_filter = ('question', 'customer',)
    exclude = ['is_delete', 'is_active']
