from django.db import models

class Topic(models.Model):
    subject = models.CharField(max_length=20)

    def __unicode__(self):
        return self.subject



class User(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.CharField(max_length = 30)
    username = models.CharField(max_length = 15, unique=True)
    password = models.CharField(max_length = 40)
    proffesion = models.CharField(max_length = 20)
    cur_university = models.CharField(max_length = 30)
    sex = models.CharField(max_length=2)   
    country = models.CharField(max_length = 30)
    location = models.CharField(max_length = 30)
    rand = models.CharField(max_length=21, default='NONE')
    interest_topic = models.ManyToManyField(Topic, default = 'NONE')
    #institute = models.ManyToManyField(Institute, default='NONE')
    def __unicode__(self):
        return self.username
    
class Institute(models.Model):
    user = models.ForeignKey(User)
    school_name = models.CharField(max_length=30)
    start_time = models.CharField(max_length=30)
    end_time = models.CharField(max_length=30)
    degree = models.CharField(max_length=30)   

    def __unicode__(self):
        return self.school_name




