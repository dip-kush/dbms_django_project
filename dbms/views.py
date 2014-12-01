from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.forms import ModelForm
from models import User,Topic,Institute
from papers.models import Paper
import datetime, sys
import string,random
import json
from one import printit

from django.conf import settings

def id_generator(size=20, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def int_generate(size=7, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'proffesion', 'cur_university', 'sex', 'country', 'location') 


def lnch(request):
    printit()
    cookie_value = id_generator()
    response = render(request, 'main.html')    
    response.set_cookie('id', cookie_value)
    return response

def logout(request):
    u=get_user(request)
    u.rand=id_generator()
    u.save()
    cookie_value = id_generator()
    response = render(request, 'main.html')    
    response.set_cookie('id', cookie_value)
    return response

    
'''
def signup(request):
    if request.method == 'POST':
        #form = SignupForm(request.POST)
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        try:
            pwd = request.POST['pass']
        except:
            pwd = ''    
        proffesion = request.POST['proffesion']
        cur_university = request.POST['cur_university']
        sex = request.POST['sex']
        country = request.POST['country']
        location = request.POST['location']
        p = User(first_name=fname,last_name=lname,email=email,username=username,password=pwd,proffesion=proffesion,cur_university=cur_university,sex=sex,country=country,location=location)
        p.save()
        return render(request, 'thanks.html')
'''
def signup(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        try:
            pwd = request.POST['pass']
        except:
            pwd = ''    
        proffesion = request.POST['proffesion']
        cur_university = request.POST['cur_university']
        sex = request.POST['sex']
        country = request.POST['country']
        location = request.POST['location']
        data = {'first_name': fname, 'last_name': lname, 'email': email, 'username': username, 'password': pwd, 'proffesion': proffesion, 'cur_university': cur_university, 'sex': sex, 'country': country, 'location': location} 
        form = SignupForm(data)
        if form.is_valid:
            if User.objects.filter(username = username).exists():
                return render(request, 'error.html', {'error': 'username already exists'})
            form.save()
            return render(request, 'thanks.html',{'message': 'You are successfully registerd. Go to login page'})
        else:
            return HttpResponse(form.errors)
    return render(request, 'main.html')
            
def get_session_cookie(request):
    if request.COOKIES.has_key('id'):
        value = request.COOKIES('id')
        return value
    

def get_paper_list(cookie_data):
    result = User.objects.get(rand=cookie_data)
    paper_data = Paper.objects.filter(user=result)
    paper_list = []
    if paper_data:
        for data in paper_data:
            #paper_list.append(data.title)
            paper_list.append({'title': data.title, 'link': data.id})
    return paper_list

def pfilter():
    pass




def filterpaper(request):
    p=[]
    paper_list=[]
    if request.method=='POST':
        sub = request.POST['subject']
        pap = Paper.objects.filter(tags=sub)
        t = get_all_topic()
        for i in pap:
            print p.append(i.id)
            paper = Paper.objects.get(id=i.id)
            paper_list.append({'title': paper.title, 'link': paper.id})
    return render(request, 'all.html', {'paper_list': paper_list,'topics':t})

    




def get_paper_list_from_user(result):
    #result = User.objects.get(rand=cookie_data)
    paper_data = Paper.objects.filter(user=result)
    paper_list = []
    if paper_data:
        for data in paper_data:
            #paper_list.append(data.title)
            paper_list.append({'title': data.title, 'link': data.id})
    return paper_list


def get_all_papers(request):
    print settings.MEDIA_ROOT
    result = Paper.objects.all()
    paper_list = []
    if result:
        for paper in result:
            user = User.objects.get(id=paper.user_id)
            paper_list.append({'title': paper.title, 'link': paper.id, 'user': user.username})
        print paper_list
    return paper_list
    

               
def signin(request):
    results = {}
    print "everytime i come here print it"
    if request.method == 'POST':
        uname = request.POST['username'];
        pwd = request.POST['pass'];
        if User.objects.filter(username = uname).exists():
            try:
                results=User.objects.get(username=uname)
            except:
                print sys.exc_info()    
                   
            if pwd==results.password:
                cookie_data = request.COOKIES.get('id')
                print cookie_data
                results.rand = cookie_data
                results.save()
                paper_list = get_paper_list(cookie_data)
                return render(request,'profile.html',{'firstname': results.first_name, 'lastname': results.last_name, 'paper_list': paper_list});
            else: 
                error =  {'error': 'password or username do not match'}     
        else:
            error = {'error': 'username do not exist'}
    return render(request, 'error.html', error)


def check(request):
    if request.is_ajax():
        if request.method=='POST':
            uname = request.POST['username']
            print uname
            if User.objects.filter(username=uname).exists():
                print 'Raw Data: "%s"' % request.body
                msg = 1
            else:
                msg = 0
    return HttpResponse(json.dumps({'data': msg}))

def print_topic(request, cookie_data):
    topics = []
    result_set = User.objects.get(rand = cookie_data)
    result = User.objects.filter(rand = cookie_data)
    try:
        result_topic = result.values('interest_topic')
        print result_topic
        for item in result_topic:
            topics.append(Topic.objects.get(id=item['interest_topic']).subject)
    except: 
        topics.append("There are no topics")
    return (result_set, topics)

def get_all_topic():
    topics = [] 
    result = Topic.objects.all()
    for item in result:
        topics.append({'value': item.id, 'title': item.subject})
    return topics


def get_schooling(request):
    cookie_data = request.COOKIES.get('id')
    if User.objects.filter(rand = cookie_data).exists():
        result = User.objects.get(rand=cookie_data)
        result_set=Institute.objects.filter(user=result.id)
    return result_set
                



def edit_profile(request):
    #print request.GET['val']
    cookie_data = request.COOKIES.get('id')
    if User.objects.filter(rand = cookie_data).exists():
        (result1, result2) = print_topic(request,cookie_data)
        result3 = get_all_topic()
        result4 = get_schooling(request)
        print "this is ",result4
        result5 = get_schooling(request)
        print "this is the result set",result5
        return render(request, 'edit_profile.html',{'firstname': result1.first_name, 'lastname': result1.last_name, 'interest_topic': result2, 'topics': result3,'schools': result4,'school_del':result5 })
    else:    
        return render(request, '404.html')


def delete_topic(request):
    if request.method == 'POST':
        sub = request.POST['subject']
        t=Topic.objects.get(id=sub)
        #t.objects.get(interest_topic=t)
        u=get_user(request)
        u.interest_topic.remove(t)
    return render(request,'thanks.html',{'message': "Topic Deleted"})

def delete_school(request): 
    if request.method=='POST':
        s = request.POST['sch']
        t = Institute.objects.filter(id=s).delete()
    return render(request,'thanks.html',{'message': "School Deleted"})


def check_cookie_validity(request):
    try:
        cookie_data = request.COOKIES.get('id')
    except:
        return False
    if User.objects.filter(rand = cookie_data).exists():
        return True
    else:
        return False
        
def get_user(request):  
    cookie_data = request.COOKIES.get('id')
    if User.objects.filter(rand = cookie_data).exists():
        result = User.objects.get(rand=cookie_data)
    return result

def add_topic(request):
    if check_cookie_validity(request):
        if request.method == 'POST':
            topic = request.POST['subject']
            print topic
            cookie_data = request.COOKIES.get('id')
            result = User.objects.get(rand=cookie_data)
            result.interest_topic.add(int(topic))
            return render(request, 'thanks.html', {'message': 'Topic has been added'})   
            #result = User.objects.get(rand=cookie_data)
            #(result1, result2) = print_topic(request,cookie_data)
            #result3 = get_all_topic()
            #return render(request, 'edit_profile.html',{'firstname': result1.first_name, 'lastname': result1.last_name, 'interest_topic': result2,'topics': result3})
            #result_topic = result.values('interest_topic')[0]
            #return render(request, 'edit_profile.html')
    else:
        return render(request, '404.html')


def view_all_papers(request):
    paper_list = get_all_papers(request)
    t = get_all_topic()
    if check_cookie_validity(request):
        return render(request, 'all.html', {'paper_list': paper_list,'topics':t})
    else:
        return render(request, 'ws_all.html',{'paper_list': paper_list})

def addschool(request):
    if request.method=='POST':  
        skl=request.POST['school_name']
        sd=request.POST['st_date']
        ed=request.POST['end_date']
        deg=request.POST['degree_at']
        u=get_user(request) 
        data=Institute(user=u,school_name=skl,start_time=sd,end_time=ed,degree=deg)
        data.save()
        return render(request,'thanks.html',{'message':'Schooling details has been saved'})

def welcome(request):
    cookie_data=request.COOKIES.get('id')    
    u = get_user(request)
    papers = get_paper_list_from_user(u)
    top = print_topic(request,cookie_data)
    top = top[1]
    return render(request,'welcome.html', {'user': u, 'interest_topic': top,'paper_list':papers})
