import requests
import os
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from .models import List
from .forms import ListForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

load_dotenv()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) 
def home(request):
	"""
	handles the creation and search of new todo through actions
	"""
	if request.method == 'POST':
		action = request.POST.get("action")
		item = request.POST.get("item")
		form = ListForm(request.POST)
		
		if action == "add":
			if form.is_valid():
				form.save()
				tasks = List.objects.all
				messages.success(request, ("Task Has Been Added To List!"))
				return render(request, 'home.html', {'tasks': tasks})
		elif action == "search":
			tasks = List.objects.filter(item__icontains=item)
			return render(request, 'search_results.html', {'tasks': tasks, 'query': item})

	else:
		tasks = List.objects.all
		return render(request, 'home.html', {'tasks': tasks}) 


def about(request):
    context = {'first_name': 'Alireza', 'last_name': 'Ghorbani'}
    return render(request, 'about.html', context)


def delete(request, list_id):
	"""
	delete a todo from todo list
	"""
	task = List.objects.get(pk=list_id)
	task.delete()
	messages.success(request, ("Task Has Been Deleted!"))
	return redirect('home')


def cross_off(request, list_id):
	task = List.objects.get(pk=list_id)
	task.completed = True
	task.save()
	return redirect('home')	

def uncross(request, list_id):
	task = List.objects.get(pk=list_id)
	task.completed = False
	task.save()
	return redirect('home')	


def edit(request, list_id):
	"""
	edit a todo, redirected to home when successful
	"""
	if request.method == 'POST':
		task = List.objects.get(pk=list_id)

		form = ListForm(request.POST or None, instance=task)
        
		if form.is_valid():
			form.save()
			messages.success(request, ('Task Has Been Edited!'))
			return redirect('home')

	else:
		task = List.objects.get(pk=list_id)
		return render(request, 'edit.html', {'task': task})
    

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register(request):
	"""
	register a new user, redirected to login if user is successfully registered.
	"""
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		
		if not username or not password or not email:
			return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
		
		if User.objects.filter(username=username).exists():
			return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
		
		user = User.objects.create_user(username=username, password=password, email=email)
		user.save()
		return redirect("login")
	return render(request, 'register.html')

@api_view(['GET', 'POST'])
@permission_classes([AllowAny]) 
def login_view(request):
	"""
	login to user account, if login successful then redirected to home
	"""
	if request.method == 'POST':
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
	return render(request, 'login.html')


def get_public_holiday(request):
	
	# this api provide country name in iso_3166 format --> https://calendarific.com/api-documentation
	# https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes

	country = request.GET.get("country")
	year = request.GET.get("year")
	api_key = os.getenv("CALENDER_API_KEY")

	url = f"https://calendarific.com/api/v2/holidays?&api_key={api_key}&country={country}&year={year}"

	try:
		response = requests.get(url=url)

		if response.status_code == 200:
			data = response.json()
			holidays = data.get("response", {}).get("holidays", [])
			return JsonResponse({"holidays": holidays})

		else:
			return JsonResponse({'error': 'Failed to fetch data from external API'}, status=response.status_code)
	except Exception as e:
		return JsonResponse({"error": f"Unexpcted error, refer documentation for more"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)