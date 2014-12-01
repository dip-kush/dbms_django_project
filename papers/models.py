from django.db import models
from dbms.models import User, Topic
import datetime
'''
class Author(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=40)
    email = models.EmailField()
    
    def Meta(self):
        return self.name
'''        

class Paper(models.Model):
    title = models.CharField(max_length=100,default=None)
    paper_file = models.FileField(upload_to='uploads')
    user = models.ForeignKey(User)
    tags = models.ManyToManyField(Topic, default='NONE')
    views = models.IntegerField(default=0)
    #authors = models.ManyToManyField(Author, default=None)
    #user_id = models.ForeignKey(User)
    #date_publish = models.CharField(max_length=12,default=None)
    
    def __unicode__(self):
        return self.title
    
    
class Comment(models.Model):
    user_id = models.ForeignKey(User)
    subject = models.CharField(max_length=100, default="no subject")
    content = models.CharField(max_length=200, default="no content")
    paper_id = models.ForeignKey(Paper)
    comment_time = models.DateTimeField('date_created', default=datetime.datetime.now())

    def __unicode__(self):
        return self.subject


class View(models.Model):
    user=models.ForeignKey(User)
    pap=models.ForeignKey(Paper)   

# Create your models here.
