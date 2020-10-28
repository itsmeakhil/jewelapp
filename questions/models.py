from django.db import models

from agent.models import Agent
from company.models import Company
from user.models import User
from utils.basemanager import BaseManager
from utils.basemodel import BaseModel


class Question(BaseModel):
    content = models.CharField(max_length=500, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    objects = BaseManager()

    def __str__(self):
        return self.content


class QuestionOption(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_answer = models.BooleanField(default=False)

    objects = BaseManager()

    def __str__(self):
        return self.name


class AgentAnswers(BaseModel):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)

    objects = BaseManager()

    def __str__(self):
        return self.agent.name
