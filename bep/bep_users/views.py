from django import forms
from django.contrib.auth import authenticate,login,logout
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.utils.translation import string_concat
from django.contrib.auth.models import User
from django.template import Context,RequestContext
from bep.stories.models import story,audio_story,count
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.db import models

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class clog(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))

class register1(forms.Form):
	name = forms.CharField(max_length=40)
	user_name = forms.CharField(max_length=30) 
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))
	confirm_pwd = forms.CharField(widget=forms.PasswordInput(render_value=False))
	email_id = forms.EmailField()

def home(request):
	count=1
	if request.method == 'POST':
		form = clog(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username,password=password)
			
			if user is not None:
				login(request,user)
				return HttpResponseRedirect('/profile/')
			else:
				count=2
				#return HttpResponseRedirect('/home/')
	else:
		form = clog()
	all_entries = story.objects.all().order_by("-date_submission")[:4]
	c = {'form':form,'stories':all_entries,'count':count}
	c.update(csrf(request))
	print count
	return render_to_response('home.html',c)
''''
def profile(request):
	t=get_template('profile.html')
	all_entries = story.objects.filter(user_submit=request.user)
	html=t.render(Context({"person_name":request.user,"stories":all_entries}))
	return HttpResponse(html)
'''

def profile(request):
	
	#print request.GET['kunu']
  if request.user.is_authenticated():
	if request.method == 'POST':
		
		form = UploadFileForm(request.POST,request.FILES)
		print form.errors
		if form.is_valid():
			
			title1 = form.cleaned_data['title']
				
			
			handle_uploaded_file(request.FILES['file'],request.user,title1)
			return HttpResponseRedirect('/profile/')
	else:
		
		form = UploadFileForm()
	t=get_template('profile.html')
	
	all_entries = story.objects.filter(user_submit=request.user)
	all_entries1 = story.objects.all().order_by("-date_submission")
	stories_you = audio_story.objects.filter(user_submit=request.user)

	
	c = {"person_name":request.user,"stories":all_entries,'form':form,"stories_all":all_entries1,"stories_you":stories_you}
	#html=t.render(Context())
	c.update(csrf(request))
	#return HttpResponse(html)
	return render_to_response('profile.html',c)
  else:
	return HttpResponseRedirect('/home/')

	
def handle_uploaded_file(f,g,h):
    s = string_concat(datetime.now(),g)	
    destination = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_text/'+unicode(s), 'wb')
    for chunk in f.chunks():
		destination.write(chunk)
    destination.close()
    destination = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_text/'+unicode(s), 'rb')
    temp_file = destination.read()
    destination.close()
    count1 = 0
    whole_file = "<1>"+ temp_file
    count1=whole_file.count(".")
    for i in range(2,count1+2):
		whole_file1 = whole_file.replace(".","<"+str(i)+">",1)
		whole_file = whole_file1
    destination = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_text/'+unicode(s), 'wb')
    destination.write(str(whole_file))
    destination.close()	
    b = story(title=h,date_submission=datetime.now(),user_submit=g,last_modify=datetime.now(),file_name=unicode(s))
    b.save()
    b1 = count(title=h,counter=0)
    b1.save();

def register(request):
	if request.method == 'POST':
		form = register1(request.POST)
		
		if form.is_valid():
			name = form.cleaned_data['name']
			user_name = form.cleaned_data['user_name']
			password = form.cleaned_data['password']
			confirm_pwd = form.cleaned_data['confirm_pwd']
			email_id = form.cleaned_data['email_id']
			user = User.objects.create_user(user_name,email_id,password)
			user.save()	
			return HttpResponseRedirect('/home/')
	else:
		form = register1()
	c = {'form':form}
	c.update(csrf(request))
	return render_to_response('register.html',c)

def logout1(request):
	logout(request)
	return HttpResponseRedirect('/home/')

def success(request):
	t=get_template('success.html')
	html=t.render(Context({}))
	return HttpResponse(html)

def contactus(request):
	t=get_template('contactus.html')
	html=t.render(Context())
	return HttpResponse(html)

def feedback(request):
	
	a=request.GET['Message']
	fid = open("feedback.txt", 'a+')
	s = "USER:" +str(request.user) 
	fid.write('\n');
	fid.write(s)
	fid.write('\n');
	s = "MESSAGE:"
	fid.write(s);
	fid.write(a);
	fid.close();
		
	t=get_template('contactus.html')
	html=t.render(Context())
	return HttpResponse(html)
	
def listen(request):
	title1=request.POST['search3']
	all_entries = story.objects.filter(title=title1)
	fname = all_entries[0].file_name
	fid = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_text/'+fname, 'rb+')
	temp = fid.read()
	fid.close()
	all_entries = audio_story.objects.filter(title=title1)
	name = all_entries[0].file_name
	c = {'title1':title1,'data':temp,'name':name,}
	return render_to_response('listen.html',c)		

    

	
