from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('blog:post_list'))


def register_view(request):
	register_status = False
	if request.method  == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			authenticated_user = authenticate(
				username=new_user.username,
				password=request.POST['password1'])
			login(request, authenticated_user)
			return HttpResponseRedirect(reverse('blog:post_list'))
			register_status = True
	else:
		form = UserCreationForm()
	return render(request, 'users/register1.html',
		{'register_status': register_status,
		'form': form})
