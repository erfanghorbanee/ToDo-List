from django.shortcuts import render, redirect
from .models import List
from .forms import ListForm
from django.contrib import messages
from django.http import HttpResponseRedirect

def home(request):
    if request.method == 'POST':
        form = ListForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            tasks = List.objects.all
            messages.success(request, ("Task Has Been Added To List!"))
            return render(request, 'home.html', {'tasks': tasks}) 

    else:
        tasks = List.objects.all
        return render(request, 'home.html', {'tasks': tasks}) 


def about(request):
    context = {'first_name': 'Alireza', 'last_name': 'Ghorbani'}
    return render(request, 'about.html', context)


def delete(request, list_id):
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
    
    


# password12345