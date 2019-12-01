from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm, UserEditForm
from .models import Profile
from cards.models import Meal
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            Profile.objects.create(user=new_user)
            # login user
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('analyzer:analyze')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    next_page = request.GET['next']
    if request.user.is_authenticated():
        return HttpResponseRedirect(next_page)
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request, username=cd['username'], password=cd['password'])
                if user is not None:
                    login(request, user)
                    if next_page:
                        return HttpResponseRedirect(next_page)
                    else:
                        return HttpResponseRedirect('/')
                else:
                    error_msg = 'Could not log in'
                    return render(request, "login", {'form': form, 'error_msg': error_msg})
            else:
                error_msg = "Invalid credentials"
                return render(request, "login", {'form': form, 'error_msg': error_msg})
        else:
            form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_meals(request):
    meals = Meal.objects.filter(author=request.user)
    #TODO add update forms
    return render(request, 'users/profile.html', {'meals': meals})

@login_required
def profile(request):
    meals = Meal.objects.filter(collectors=request.user)
    saved = Meal.objects.filter(author=request.user).count()
    collected = Meal.objects.filter(collectors=request.user).count()-saved
    paginator = Paginator(meals, 3)
    page = request.GET.get('page')
    try:
        meals = paginator.page(page)
    except PageNotAnInteger:
        meals = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        meals = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'users/user_list_ajax.html', {'meals': meals})
    return render(request, 'users/profile.html', {'meals': meals, 'collected': collected, 'saved':saved})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('/users/profile')
        else:
            messages.error(request, "Your profile could not be updated")
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'user_form': user_form})


class PasswordChange(PasswordChangeView):
    success_url = '/users/profile'
    template_name = 'users/password_change.html'







