from django.shortcuts import render

# Create your views here.
#add
from myapp.tools import *

from myapp.main import *
from django.views.static import serve 
from .models import FileData
from django.shortcuts import render
from django.http import HttpResponse

from django.template.loader import render_to_string
import os
import unittest
# from myapp.tests import HistogramTestCase #Where my unittest was defined

def algoritm_to_zip(request):

	csv_path = {"None":None}
	#print("**\n\n\n*", request.FILES)
	mode = 'csvselect'
	if 'myfile' in request.FILES:

		this_file = FileData.objects.create(tag="input", file=request.FILES['myfile'])
		csv_path["csvSelected"] = "files"+this_file.file.url
	elif request.POST.getlist('mysql'):
		mode = 'mysql'
	else:
		csvselected = request.POST['csvselected']
		csv_path["csvSelected"] = f'myapp/analysisfolder/EasyData/{csvselected}'

	do_algoritm(csv_path, mode)
    #
	file_obj = tozip(None,"myapp/analysisfolder/Luk_Virksomhed")

	this_file = FileData.objects.create(name="generated_files.zip",file=file_obj,tag="zip")

	zip_download = [this_file.file.url] #adress er files
	context = {'zip': zip_download}

	return render(request,'result.html',context)

def index(request):
	FileData.objects.all().delete()
	input_dir = "myapp/analysisfolder/EasyData/"
	file_list=os.listdir(input_dir)

	new_list = []
	for file in file_list:
		new_list += [
		{
		"name": file,
		"link": input_dir+file
		}]
	context = {'csvlist': new_list}

	return render(request,'index.html',context)

def show_Message(request):
	listString = []
	mess1= "CSV should have these columns:"
	listString.append(mess1)

	context = {'message':listString }
	return render(request,'message.html',context)