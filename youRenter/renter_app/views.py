from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Ware
from .forms import WareForm, UserForm, ProfileForm, LoginForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout




def is_admin_group(user):
    return user.groups.filter(name='admin').exists()

def private_view(request):
    if is_admin_group(request.user):
        return render(request, 'private.html', {})        
    else:
        return HttpResponseRedirect(reverse('home'))


def index(request):
    item = Ware.objects.all()
    data={
        'item': item
    }
    return render(request,'index.html',data)


@login_required
def add(request):
    form = WareForm()
    if request.method == 'POST':
        form = WareForm(request.POST)
        if form.is_valid():
            ware = form.save(commit=False)
            if 'picture' in request.FILES:
                ware.picture = request.FILES['picture']
            ware.save()            
            print('save')
            messages.success(request, 'your item have been added succesfully')
            return HttpResponseRedirect(reverse('home'))
        else:
            print('form is not valid')

    data = {
        'form': form
    }
    return render(request,'add.html', data)





def detail(request, pk):
    ware = get_object_or_404(Ware, pk=pk)
    data = {
        'ware': ware
    }
    return render(request, 'detail.html', data)

  


class WareDelete(DeleteView):
    model = Ware
    success_url = reverse_lazy('home')
    template_name = 'delete.html'  


class WareCreate(CreateView):
    model = Ware
    fields = '__all__'
    template_name = 'ware_form.html'

class WareUpdate(UpdateView):
    model = Ware
    fields = '__all__'
    template_name = 'ware_form.html'     




@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.error(request, 'user is not active')
            else:
                messages.error(request, 'invalid username of password')
    
    data = {'form': form}
    return render(request, 'login.html', data)


def register(request):
    userForm = UserForm()
    profileForm = ProfileForm()

    if request.method == 'POST':
        userForm = UserForm(request.POST)
        profileForm = ProfileForm(request.POST)

        if userForm.is_valid() and profileForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = profileForm.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect(reverse('home'))

    data = { 'userForm': userForm, 'profileForm': profileForm}
    return render(request, 'register.html', data)



