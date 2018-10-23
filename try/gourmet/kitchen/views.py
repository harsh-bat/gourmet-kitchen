from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Everyone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import os
MEDIA_URL = '/media/'

def index(request):
    return render(request, "kitchen/index.html")

def loginview(request):
    if request.method == "POST":
        entered_email = request.POST.get('login_email')
        entered_password = request.POST.get('login_password')
        if User.objects.filter(username=entered_email).exists():
            pass
        elif  User.objects.filter(email=entered_email).exists():
            entered_email = User.objects.get(email=entered_email).username
        else:
            return render(request, "kitchen/index.html",{"clickSignup":True,"error_message_signup":"You don't have an account. You must sign up"})
        user = authenticate(username=entered_email, password=entered_password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(f'profile/{entered_email}')
        else:
            return render(request, "kitchen/index.html",{"clickLogin":True,"error_message_login":"Enter valid credentials"})
    else:
        return render(request, "kitchen/index.html",{"clickLogin":True,"error_message_login":"You must first Login"})


@login_required(login_url='/login')
def profile(request, usernameLink):
    current_user = request.user
    link_user=None
    if User.objects.filter(username=usernameLink).exists():
        link_user= User.objects.get(username=usernameLink)
    else:
        return HttpResponseRedirect(f'{current_user.username}')
    current_person = Everyone.objects.get(id=current_user)
    link_person = Everyone.objects.get(id=link_user)
    person=None
    is_self=True
    if current_user==link_user:
        person=current_person
        is_self=True
    else:
        person=link_person
        is_self=False
    context = {'user_name':person.name,
    'user_email':current_user.email,
    'rec_imgs' : [person.about],
    'user_age':person.age,
    'user_about':person.about,
    'user_dp':person.dp,
    'user_cover':person.cover,
    'is_self':is_self,
    'MEDIA_URL':MEDIA_URL}
    if person.type == 'C':
        rec_names=['rec1_name', 'rec2_name', 'rec3_name', 'rec4_name', 'rec5_name']
        rec_hrs = [2,4,12,3,5,6]
        rec_mins = [43,21,35,61,78]
        context['recs']=zip(rec_names, rec_hrs, rec_mins)
        context['recNo'] = len(rec_names)
        return render(request, "kitchen/profile_chef.html",context)
    else:
        return render(request, "kitchen/profile_user.html", context)


def signup(request):
    if request.method=='POST':
        entered_email = request.POST.get("signup_email")
        entered_username = request.POST.get("signup_username")
        entered_password = request.POST.get("signup_password")
        if User.objects.filter(email=entered_email).exists():
            return render(request, "kitchen/index.html",{"clickLogin":True,"error_message_login":"You already have an account. Try logging in."})
        else:
            if User.objects.filter(username=entered_username).exists():
                return render(request, "kitchen/index.html",{"clickSignup":True,"error_message_signup":"Username exists. Enter another one."})
            else:
                user = User.objects.create_user(
                    username = entered_username,
                    password = entered_password,
                    email = entered_email
                    )
                every = Everyone.objects.create(
                    id=user,
                    name=request.POST.get("signup_name"),
                    age=request.POST.get("signup_age"),
                    type=request.POST.get("signup_type")
                    )
                user.save()
                every.save()
                login(request, user)
                return HttpResponseRedirect("/profile")
    else:
        return render(request, "kitchen/index.html",{"clickSignup":True})




@login_required(login_url='/login')
def dpChange(request):
    if request.method=="POST":
        picUploaded = request.FILES["selDpUpload"]
        current_user = request.user
        person = Everyone.objects.get(id=current_user)
        if person.dp:
            person.dp.delete()
        person.dp = picUploaded
        person.save()
        return HttpResponseRedirect("/profile")
    else:
        return HttpResponseRedirect("/profile")


@login_required(login_url='/login')
def coverChange(request):
    if request.method=="POST":
        picUploaded = request.FILES["coverUpload"]
        current_user = request.user
        person = Everyone.objects.get(id=current_user)
        if person.cover:
            person.cover.delete()
        person.cover= picUploaded
        person.save()
        return HttpResponseRedirect("/profile")
    else:
        return HttpResponseRedirect("/profile")


@login_required(login_url='/login')
def detailsChange(request):
    if request.method=='POST':
        edited_name = request.POST.get('edit_name')
        edited_age = request.POST.get('edit_age')
        edited_about = request.POST.get('edit_about')
        current_user = request.user
        person = Everyone.objects.get(id=current_user)
        person.about=edited_about
        person.age=edited_age
        person.name=edited_name
        person.save()
        return HttpResponseRedirect('/profile')
    else:
        return HttpResponseRedirect("/profile")

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url='/login')
def newRecipe(request):
    return render(request, "kitchen/new_rec.html")

@login_required(login_url='/login')
def acceptNewRec(request):
    if request.method == 'POST':
        toSend = request.POST
        ingStr = findIngVal(toSend)
        entered_name = request.POST.get('recName')
        entered_desc = request.POST.get('recDesc')
        entered_cal = request.POST.get('recCal')
        entered_dir = request.POST.get('recDir')
        entered_hr = request.POST.get('recHr')
        entered_min = request.POST.get('recMin')
        entered_img = request.FILES['imgUpload']
        return HttpResponse(ingStr)
    else:
        return HttpResponseRedirect("/new")



def findIngVal(vals):
    ingStr = ""
    for i in range(16):
        k=str((i+1))
        keyVal = "ing"+k
        a="0"
        try:
            if str(vals.get(keyVal))=="on":
                a="1"
        except:
            a="0"
        ingStr = ingStr + a
    return ingStr


def category(request, categoryName):
    return render(request, "kitchen/category.html")

def result(request):
    return render(request, "kitchen/result.html")

def team(request):
    return render(request, "kitchen/team.html")