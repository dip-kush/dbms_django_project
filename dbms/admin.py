from django.contrib import admin
from dbms.models import User,Topic
from papers.models import Paper

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Paper)
