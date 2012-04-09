from bep.stories.models import story
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django import forms
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
from django.utils.translation import string_concat
from bep.stories.models import story,count,audio_story
import wave
import struct

class UploadAudio(forms.Form):
    audio_file  = forms.FileField()
    log_file = forms.FileField()
    

def effects(request):
	t=get_template('effects.html')
   
	return HttpResponse(t)

def recording(request):
        t=get_template('recording.html')
        html=t.render(Context({}))
        return HttpResponse(html)
        
def edit(request):
	t=get_template('edit.html')
	return HttpResponse(t)	

def st(request,a):
	if request.method == 'GET':
		story_list = story.objects.filter(title=a)
		fname = story_list[0].file_name
		fid = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_text/'+fname, 'rb+')
		temp = fid.read()
		fid.close()
		c = {'temp_title':a,'temp':temp}
		return render_to_response('story.html',c)
	else:
		return render_to_response('tp.html')

def search_story(request):
	if request.method == 'POST':
		a=request.POST['search2']
		story_list = story.objects.filter(title=a)
		fname = story_list[0].file_name
		fid = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_text/'+fname, 'rb+')
		temp = fid.read()
		fid.close()
		c = {'temp_title':a,'temp':temp}
		return render_to_response('story.html',c)
	else:
		return render_to_response('tp.html')
		
	
def record(request):
		c = {'status1':'hidden'}
		c.update(csrf(request))
		return render_to_response('record.html',c)
		
def rec_search(request):
	if request.method == 'POST':
		a=request.POST['rec']
		try:
			story_list = story.objects.filter(title=a)
			fname = story_list[0].file_name
			#c={'stauts1':'show'}
			form = UploadAudio()
			c = {'form':form,'status1':'show','a3':a}
		except:
			c={'status1':'hidden'}
		
		c.update(csrf(request))
		return render_to_response('record.html',c)
	else:
		return render_to_response('tp.html')
		
def aud(request):
	if request.method == 'POST':
		de=request.POST['story_title']
		form = UploadAudio(request.POST,request.FILES)
		
		if form.is_valid():
			print 'entered if'
			handle_uploaded_file(request.FILES['log_file'],request.FILES['audio_file'],request.user,de)
			print 'inside if'
	return HttpResponseRedirect('/profile/')
	
	
def handle_uploaded_file(f,g,h,i)	:
	story_list = story.objects.filter(title=i)
	fname = story_list[0].file_name
	c = count.objects.filter(title=i)
	qw = c[0].counter
	count.objects.filter(title=i).update(counter=qw+1)
	
	s = string_concat(fname,"_",qw,".log")
	destination = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_log/'+unicode(s), 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()
	s = string_concat(fname,"_",qw)
	handle_uploaded_file2(f,g,h,i,s)
	
def handle_uploaded_file2(f,g,h,i,s):
	s1 = string_concat(s,".wav")
	destination = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_audio/'+unicode(s1), 'wb+')
	for chunk in g.chunks():
		destination.write(chunk)
	destination.close()
	
	s1 = string_concat(s,".wav")	
	b = audio_story(title=i,date_submission=datetime.now(),user_submit=h,file_name=unicode(s1))
	b.save();
    
def add_effects(request,a):
	story_list = story.objects.filter(title=a)
	fname = story_list[0].file_name
	fid = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_text/'+fname, 'rb+')
	temp = fid.read()
	fid.close()
	
	frnd_list = audio_story.objects.filter(title=a)
	
	c = {'temp_title':a,'temp':temp,'frnd_list':frnd_list,'status':'false'}
	c.update(csrf(request))
	return render_to_response('add_effects.html',c)			

def frnde(request,a):
		init = int(request.POST['text1'])
		final = int(request.POST['text2'])
		opt = request.POST['group1']
	
		story_list = audio_story.objects.filter(title=a,user_submit=opt)
		fname = story_list[0].file_name
		story_list1 = audio_story.objects.filter(title=a,user_submit=request.user)
		fname1 = story_list1[0].file_name
		aud_frnd = wave.open('/home/mayank/Desktop/bep/bep/bep_users/static/story_audio/'+fname,'rb')
		aud_me = wave.open('/home/mayank/Desktop/bep/bep/bep_users/static/story_audio/'+fname1,'rb')
		
		num_channels_me = aud_me.getnchannels()
		sample_rate_me = aud_me.getframerate()
		sample_width_me = aud_me.getsampwidth()
		num_frames_me = aud_me.getnframes()
		
		num_channels_frnd = aud_frnd.getnchannels()
		sample_rate_frnd = aud_frnd.getframerate()
		sample_width_frnd = aud_frnd.getsampwidth()
		num_frames_frnd = aud_frnd.getnframes()
			
		#open log file and get sample numbers
		l = len(fname)
		fnamet=fname[0:l-4]+".log"
		log_frnd = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_log/'+fnamet,'rb')
		l = len(fname1)
		fname1t=fname1[0:l-4]+".log"
		log_me = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_log/'+fname1t,'rb')
		
		#init=2
		#final=3
		
		under1 = log_frnd.read()
		count = 0
		j=0;
		
		found = []
		found.append(0)
		
		for x in range(0,len(under1)):
			if under1[x] == '_':
				found.append(x)
			
		if init==1:
			first1 = found[init-1]+1
			first2 = found[init]-1
			start_from_frnd = 1	
		else:
			first1 = found[init-1]+1
			first2 = found[init]-1
			start_from_frnd = int(under1[first1:first2+1])
		last1 = found[final]+1
		last2 = found[final+1]-1
		end_to_frnd = int(under1[last1:last2+1])	
		
		under1 = log_me.read()
		count = 0
		j=0;
		
		found = []
		found.append(0)
		
		for x in range(0,len(under1)):
			if under1[x] == '_':
				found.append(x)
			
		if init==1:
			first1 = found[init-1]+1
			first2 = found[init]-1
			start_from_me = 1	
		else:
			first1 = found[init-1]+1
			first2 = found[init]-1
			start_from_me = int(under1[first1:first2+1])
		last1 = found[final]+1
		last2 = found[final+1]-1
		end_to_me = int(under1[last1:last2+1])
		
		#	main OPERATION
		before = aud_me.readframes(start_from_me)
		waya_frnd = aud_frnd.readframes(start_from_frnd)
		waya_me = aud_me.readframes(end_to_me-start_from_me)
		frnd_part = aud_frnd.readframes(end_to_frnd-start_from_frnd)
		after = aud_me.readframes(num_frames_me-end_to_me)
		
		aud_me.close()
		aud_frnd.close()
		
		fi = ""
		fi = before+frnd_part+after
		
		p = wave.open('/home/mayank/Desktop/bep/bep/bep_users/static/story_audio/'+"temp_frnd.wav",'wb')
		p.setnchannels(2)
		p.setsampwidth(sample_width_me)
		p.setframerate(44100)
		p.writeframes(fi)
		p.close()
		return HttpResponseRedirect('/profile/')
		
		
def adde(request,a):
		init = int(request.POST['text1'])
		final = int(request.POST['text2'])
		
		#init=2
		#final=3
		#opt1 = request.POST['group1']
	
		story_list = story.objects.filter(title=a)
		fname = story_list[0].file_name
		#print fname
		
		
		slist = audio_story.objects.filter(title=a)
		fname_a = slist[0].file_name
		l = len(fname_a)
		fname1=fname_a[0:l-4]+".log"
		log = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_log/'+fname1,'rb+')
		
		
		under = log.read()
		count = 0
		j=0;
		
		found = []
		
		
		for x in range(0,len(under)):
			if under[x] == '_':
				found.append(x)
		print found		
	
		if init==1:
			start_from = 1	
		else:
			first1 = found[init-2]+1
			first2 = found[init-1]-1
			start_from = int(under[first1:first2+1])
		last1 = found[final-2]+1
		last2 = found[final-1]-1
		end_to = int(under[last1:last2+1])	
		print start_from
		print end_to	
		
		
		stream = wave.open('/home/mayank/Desktop/bep/bep/bep_users/static/story_audio/'+fname_a,"rb")
		num_channels = stream.getnchannels()
		sample_rate = stream.getframerate()
		sample_width = stream.getsampwidth()
		num_frames = stream.getnframes()
		total_samples = (end_to-start_from+1) * num_channels

						
		choice = request.POST['group1']				
		stream1 = wave.open('/home/mayank/Desktop/bep/bep/bep_users/static/story_audio/effects/'+choice,"rb")
		num_channels1 = stream1.getnchannels()
		sample_rate1 = stream1.getframerate()
		sample_width1 = stream1.getsampwidth()
		num_frames1 = stream1.getnframes()
		
		before = stream.readframes(start_from)
		raw_data = stream.readframes( end_to-start_from+1 ) # Returns byte data
		after = stream.readframes(num_frames-end_to)
		stream.close()		
	
		if sample_width == 1:
				fmt = "%iB" % total_samples # read unsigned chars
		elif sample_width == 2:
			fmt = "%ih" % total_samples # read signed 2 byte shorts
		else:
			raise ValueError("Only supports 8 and 16 bit audio formats.")
		integer_data = struct.unpack(fmt, raw_data)
		del raw_data # Keep memory tidy (who knows how big it might be)
		channels = [ [] for time in range(num_channels) ]
		for index, value in enumerate(integer_data):
			bucket = index % num_channels
			channels[bucket].append(value)
				
		if total_samples < num_frames1*num_channels1:			
			raw_data1 = ""
			
			raw_data1 = stream1.readframes( end_to-start_from+1 ) # Returns byte data
			#stream1.close()
			total_samples1 = (end_to-start_from+1) * num_channels1

			if sample_width1 == 1:
				fmt1 = "%iB" % total_samples1 # read unsigned chars
			elif sample_width1 == 2:
				fmt1 = "%ih" % total_samples1 # read signed 2 byte shorts
			else:		
				raise ValueError("Only supports 8 and 16 bit audio formats.")

			
			integer_data1 = struct.unpack(fmt1, raw_data1)
			del raw_data1 # Keep memory tidy (who knows how big it might be)
			channels1 = [ [] for time in range(num_channels1) ]
		
			for index1, value1 in enumerate(integer_data1):
				bucket1 = index1 % num_channels1
				channels1[bucket1].append(value1)

			tot_sapl = 2 ;    

			if sample_width1 == 1:
				fmt1 = "%iB" % 2 # read unsigned chars
			elif sample_width1 == 2:
				fmt1 = "%ih" % 2 # read signed 2 byte shorts
			else:
				raise ValueError("Only supports 8 and 16 bit audio formats.")
			
			b=""
		
			print num_frames
			print num_frames1	
		
			for i in range(0,end_to-start_from+1):
				channels1[0][i] = int(round((channels[0][i]+channels1[0][i])-(channels[0][i]*channels1[0][i])/32767 ))
				channels1[1][i] = int(round((channels[1][i]+channels1[1][i])-(channels[1][i]*channels1[1][i])/32767 ))
				a1=struct.pack(fmt1,channels1[0][i],channels1[1][i])
				b=b+a1

			fi =""
			fi = before+b+after
		
		
			#slist = audio_story.objects.filter(title=a,user_submit='kunal')
		else:
			total_samples1 = (end_to-start_from+1) * num_channels1
			#needed = total_samples1
			needed = end_to - start_from + 1
		#	if num_frames1 >= needed:
		#		raw_data1 = stream1.readframes( end_to-start_from+1 ) # Returns byte data
		#	else:
			raw_data1=""
			while needed > 0:
				if num_frames1 > needed:
					temp_data1 = stream1.readframes(needed)
					raw_data1 = raw_data1 + temp_data1
					needed = needed - num_frames1
				else:
					temp_data1 = stream1.readframes(num_frames1)
					raw_data1 = raw_data1 + temp_data1
					needed = needed - num_frames1
						
			print "total_sample1"
			print total_samples1
			if sample_width1 == 1:
				fmt1 = "%iB" % total_samples1 # read unsigned chars
			elif sample_width1 == 2:
				fmt1 = "%ih" % total_samples1 # read signed 2 byte shorts
			else:		
				raise ValueError("Only supports 8 and 16 bit audio formats.")

			
			integer_data1 = struct.unpack(fmt1, raw_data1)
			del raw_data1 # Keep memory tidy (who knows how big it might be)
			channels1 = [ [] for time in range(num_channels1) ]
		
			for index1, value1 in enumerate(integer_data1):
				bucket1 = index1 % num_channels1
				channels1[bucket1].append(value1)

			tot_sapl = 2 ;    

			if sample_width1 == 1:
				fmt1 = "%iB" % 2 # read unsigned chars
			elif sample_width1 == 2:
				fmt1 = "%ih" % 2 # read signed 2 byte shorts
			else:
				raise ValueError("Only supports 8 and 16 bit audio formats.")
			
			b=""
		
			print num_frames
			print num_frames1	
		
			for i in range(0,end_to-start_from+1):
				channels1[0][i] = int(round((channels[0][i]+channels1[0][i])-(channels[0][i]*channels1[0][i])/32767 ))
				channels1[1][i] = int(round((channels[1][i]+channels1[1][i])-(channels[1][i]*channels1[1][i])/32767 ))
				a1=struct.pack(fmt1,channels1[0][i],channels1[1][i])
				b=b+a1

			fi =""
			fi = before+b+after

		p = wave.open('/home/mayank/Desktop/bep/bep/bep_users/static/story_audio/'+"temp.wav",'wb')
		p.setnchannels(2)
		p.setsampwidth(sample_width)
		p.setframerate(44100)
		p.writeframes(fi)
		p.close()
		
		story_list = story.objects.filter(title=a)
		fname = story_list[0].file_name
		fid = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_text/'+fname, 'rb+')
		temp = fid.read()
		fid.close()
	
		frnd_list = audio_story.objects.filter(title=a)
	
		c = {'temp_title':a,'temp':temp,'frnd_list':frnd_list,'status':'true'}
		c.update(csrf(request))
		return render_to_response('add_effects.html',c)	
		

def cchanges(request,a):
	slist = audio_story.objects.filter(title=a)
	fname_a = slist[0].file_name
	stream = wave.open('/home/mayank/Desktop/bep/bep/bep_users/static/story_audio/temp.wav',"rb")
	num_channels = stream.getnchannels()
	sample_rate = stream.getframerate()
	sample_width = stream.getsampwidth()
	num_frames = stream.getnframes()
	t = stream.readframes(num_frames)
	stream.close()
	
	p = wave.open('/home/mayank/Desktop/bep/bep/bep_users/static/story_audio/'+fname_a,"wb")
	p.setnchannels(2)
	p.setsampwidth(sample_width)
	p.setframerate(44100)
	p.writeframes(t)
	p.close()
	
	story_list = story.objects.filter(title=a)
	fname = story_list[0].file_name
	fid = open('/home/mayank/Desktop/bep/bep/bep_users/static/story_text/'+fname, 'rb+')
	temp = fid.read()
	fid.close()
	frnd_list = audio_story.objects.filter(title=a)
	c = {'temp_title':a,'temp':temp,'frnd_list':frnd_list,'status':'false'}
	c.update(csrf(request))
	return render_to_response('add_effects.html',c)	
	
	
	
	
	
