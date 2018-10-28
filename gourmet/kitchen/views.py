from django.shortcuts import render
import json
from django.contrib.auth.models import User
from .models import Everyone,Recipe,Ingredient,Rating
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
import difflib
import os
MEDIA_URL = '/media/'


def meet(request):
    return render(request, "kitchen/team.html")

def findTopRated():
    allRecObjs =  Recipe.objects.filter()
    recAndRating = list()
    for i in allRecObjs:
        avg_rat = 2
        if Rating.objects.filter(rec=i).exists():
            rat_objs = Rating.objects.filter(rec=i)
            tot = 0
            for j in rat_objs:
                tot = tot + j.val
            avg_rat = tot / len(rat_objs)
        recAndRating.append((i, avg_rat))
    recAndRating.sort(key= lambda t : t[1], reverse=True)
    if len(recAndRating) > 6:
        recAndRating = recAndRating[0:6]
    try:
        top_rated = list(zip(*recAndRating))[0]
    except:
        top_rated=list()
    return top_rated


def index(request, temp_context = None):
    rec_objs = findTopRated()
    if temp_context is not None:
        context = temp_context
    else:
        context = dict()
    rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals = findAllAboutRecs(rec_objs)
    context['recs']=zip(rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals)
    context['recNo'] = len(rec_names)
    context['MEDIA_URL'] = MEDIA_URL
    return render(request, "kitchen/index.html", context)

def loginview(request):
    redirection = request.POST.get('redirect_url_login')
    if request.method == "POST":
        entered_email = request.POST.get('login_email')
        entered_password = request.POST.get('login_password')
        if User.objects.filter(username=entered_email).exists():
            pass
        elif  User.objects.filter(email=entered_email).exists():
            entered_email = User.objects.get(email=entered_email).username
        else:
            temp_context =  {"clickSignup":True,"error_message_signup":"You don't have an account. You must sign up","redirect_here":redirection}
            return index(request,temp_context= temp_context)
        user = authenticate(username=entered_email, password=entered_password)
        if user is not None:
            login(request, user)
            if redirection == "" or redirection is None:
                return HttpResponseRedirect(f'profile/{entered_email}')
                pass
            else:
                return HttpResponseRedirect(redirection)
        else:
            temp_context =  {"clickLogin":True,"error_message_login":"Enter valid credentials","redirect_here":redirection}
            return index(request,temp_context= temp_context)
    else:
        if redirection is None or redirection == "":
            redirection='/profile/fsegsegsgsgsrgrgsgsrbrs'
        temp_context ={"clickLogin":True,"error_message_login":"You must first Login","redirect_here":redirection}
        return index(request,temp_context= temp_context)


def findAllAboutRecs(rec_objs):
    rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals = list(),list(),list(),list(), list(), list(), list()
    for i in rec_objs:
        rec_names.append(i.name)
        rec_hrs.append(i.time_hr)
        rec_mins.append(i.time_min)
        rec_urls.append(f"/recipe/{i.rec_id}")
        rec_imgs.append(i.rec_img)
        rec_desc.append(i.desc)
        rec_cals.append(i.cal)
    return (rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals)


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
        if Recipe.objects.filter(chef=person).exists():
            rec_objs = Recipe.objects.filter(chef=person)
            rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals = findAllAboutRecs(rec_objs)
            context['recs']=zip(rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals)
            context['recNo'] = len(rec_names)
        else:
            context['recNo'] = 0
            context['recs'] = list()
        return render(request, "kitchen/profile_chef.html",context)
    else:
        if Rating.objects.filter(user=person,sav=True).exists():
            rec_objs = list()
            rats =  Rating.objects.filter(user=person,sav=True)
            for i in rats:
                rec_objs.append(i.rec)
            rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals = findAllAboutRecs(rec_objs)
            context['recs']=zip(rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals)
            context['recNo'] = len(rec_names)
        else:
            context['recNo'] = 0
            context['recs'] = list()
        return render(request, "kitchen/profile_user.html", context)


def signup(request):
    if request.method=='POST':
        redirection = request.POST.get('redirect_url_sign')
        entered_email = request.POST.get("signup_email")
        entered_username = request.POST.get("signup_username")
        entered_password = request.POST.get("signup_password")
        if User.objects.filter(email=entered_email).exists():
            temp_context = {"clickLogin":True,"error_message_login":"You already have an account. Try logging in.","redirect_here":redirection}
            return index(request,temp_context= temp_context)
        else:
            if User.objects.filter(username=entered_username).exists():
                temp_context = {"clickSignup":True,"error_message_signup":"Username exists. Enter another one.","redirect_here":redirection}
                return index(request,temp_context= temp_context)
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
                return HttpResponseRedirect(f"/profile/{entered_username}")
    else:
        temp_context = {"clickSignup":True}
        return index(request,temp_context= temp_context)



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
        return HttpResponseRedirect(f"/profile/{request.user.username}")
    else:
        return HttpResponseRedirect(f"/profile/{request.user.username}")


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
        return HttpResponseRedirect(f"/profile/{request.user.username}")
    else:
        return HttpResponseRedirect(f"/profile/{request.user.username}")


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
        return HttpResponseRedirect(f"/profile/{request.user.username}")
    else:
        return HttpResponseRedirect(f"/profile/{request.user.username}")

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
        logged_chef = Everyone.objects.get(id=request.user)
        print(request.POST.get('recCategory'))
        ingList = request.POST.get('ingAll').replace("^ghhd^", " ").split('/element/')[1:]
        recipe = Recipe.objects.create(
            name = request.POST.get('recName'),
            desc =  request.POST.get('recDesc'),
            dir = request.POST.get('recDir'),
            cal = request.POST.get('recCal'),
            category = str(request.POST.get('recCategory')),
            time_hr = request.POST.get('recHr'),
            time_min = request.POST.get('recMin'),
            chef = logged_chef,
            rec_img = request.FILES['imgUpload'],
        )
        recipe.save()
        for i in ingList:
            ing = Ingredient.objects.create(name=i,rec=recipe)
            ing.save()
        return HttpResponseRedirect(f"/recipe/{recipe.rec_id}")
    else:
        return HttpResponseRedirect("/new")


@login_required(login_url='/login')
def editRec(request,recNoLink):
    logged_chef = Everyone.objects.get(id=request.user)
    if Recipe.objects.filter(rec_id=recNoLink).exists():
        rec = Recipe.objects.get(rec_id=recNoLink)
        ings_obs = Ingredient.objects.filter(rec=rec)
        ings=list()
        modIngs=list()
        for i in ings_obs:
            ings.append(i.name)
            modIngs.append(i.name.replace(' ', '^ghhd^'))
        if logged_chef == rec.chef:
            context = {
            "rec_name" : rec.name,
            "rec_desc": rec.desc,
            "rec_category" : rec.category,
            "rec_dir" : rec.dir,
            "rec_cal": rec.cal,
            "rec_time_hr" : rec.time_hr,
            "rec_time_min" : rec.time_min,
            "rec_img":rec.rec_img,
            "ings": zip(ings,modIngs),
            "MEDIA_URL":MEDIA_URL,
            "rec_no":recNoLink,
            "ModIng":modIngs,
            }
            return render(request,"kitchen/edit_rec.html", context)
        else:
            return render(request, "kitchen/edit_rec.html",{"is_wrong":True,"error_message":"You are trying to edit someone else's recipe"})
    else:
        return render(request, "kitchen/edit_rec.html",{"is_wrong":True,"error_message":"Opps!! Recipe Doesn't exists "})


@login_required(login_url='/login')
def acceptEditRec(request):
    if request.method == 'POST':
        ingList = request.POST.get('ingAll').replace("^ghhd^", " ").split('/element/')[1:]
        current_rec = Recipe.objects.get(rec_id=request.POST.get('recNo'))
        current_rec.name = request.POST.get('recName')
        current_rec.desc =  request.POST.get('recDesc')
        current_rec.dir = request.POST.get('recDir')
        current_rec.cal = request.POST.get('recCal')
        current_rec.category = str(request.POST.get('recCategory'))
        current_rec.time_hr = request.POST.get('recHr')
        current_rec.time_min = request.POST.get('recMin')
        try:
            xyz = request.FILES['imgUpload']
            if xyz is None:
                pass
            else:
                if xyz=="":
                    pass
                else:
                    if current_rec.rec_img:
                        current_rec.rec_img.delete()
                        current_rec.rec_img = xyz
        except:
            pass
        current_rec.save()
        old_ings = Ingredient.objects.filter(rec=current_rec)
        for i in old_ings:
            i.delete()
        for i in ingList:
            ing = Ingredient.objects.create(name=i,rec=current_rec)
            ing.save()
        return HttpResponseRedirect(f"/recipe/{current_rec.rec_id}")
    else:
        return HttpResponseRedirect("/new")


def recipe(request, recNoLink):
    if request.user.is_authenticated:
        if Recipe.objects.filter(rec_id=recNoLink).exists():
            current_person = Everyone.objects.get(id=request.user)
            rec = Recipe.objects.get(rec_id=recNoLink)
            ings_obs = Ingredient.objects.filter(rec=rec)
            is_saved = False
            inital_star = 0
            if Rating.objects.filter(rec=rec, user=current_person).exists():
                is_saved = Rating.objects.get(rec=rec, user=current_person).sav
                inital_star =  Rating.objects.get(rec=rec, user=current_person).val
            ings=list()
            for i in ings_obs:
                ings.append(i.name)
            context = {
            "rec_name" : rec.name,
            "rec_desc": rec.desc,
            "rec_category" : rec.category,
            "rec_dir" : rec.dir.split('\n'),
            "rec_cal": rec.cal,
            "rec_time_hr" : rec.time_hr,
            "rec_time_min" : rec.time_min,
            "rec_img":rec.rec_img,
            "ings":ings,
            "MEDIA_URL":MEDIA_URL,
            "rec_no":recNoLink,
            "chef_name":rec.chef.name,
            "chef_url":f"/profile/{rec.chef.id.username}",
            "is_saved" : is_saved,
            "inital_star" : inital_star,
            }
            if rec.chef == current_person :
                context['allow_edit']=True
            elif current_person.type == 'U':
                context['allow_rating']=True
            return render(request, 'kitchen/disp_recipe.html', context)
        else:
            return render(request, 'kitchen/disp_recipe.html', {'no_exist':True})
    else:
        temp_context = {"clickLogin":True,"error_message_login":"You must first Login","redirect_here":f"recipe/{recNoLink}"}
        return index(request,temp_context= temp_context)



def searching(searchIngs):
    allRecObjs =  Recipe.objects.filter()
    allRecAndIng = list()
    for i in allRecObjs:
        ings=list()
        ings_obs = Ingredient.objects.filter(rec=i)
        for j in ings_obs:
            ings.append(j.name)
        allRecAndIng.append((i,ings))
    recAndRank=list()
    for i in allRecAndIng:
        a=0
        for j in searchIngs:
            a = a + len(difflib.get_close_matches(j,i[1]))
        rank = a/len(i[1])
        rank = 100*(rank/len(searchIngs))
        if rank>0:
            recAndRank.append((i[0],rank))
    return recAndRank


@login_required(login_url='/login')
def search(request):
    if request.method == 'POST':
        searchIngs = request.POST.get('ingAll').split('/element/')[1:]
        search_results = searching(searchIngs)
        search_results.sort(key = lambda t : t[1], reverse=True)
        if len(search_results)>12:
            search_results=search_results[0:12]
        rec_objs=list()
        for i in search_results:
            rec_objs.append(i[0])
        context=dict()
        rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals = findAllAboutRecs(rec_objs)
        context['recs']=zip(rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals)
        context['recNo'] = len(rec_names)
        context["MEDIA_URL"] = MEDIA_URL
        return render(request, 'kitchen/result.html', context)

def saveTarget(request):
    if request.method == 'POST':
        rec = Recipe.objects.get(rec_id=request.POST.get('recNumber'))
        user = Everyone.objects.get(id=User.objects.get(username=request.POST.get('user')))
        to_do = request.POST.get('to_save')
        rat_obj = None
        if Rating.objects.filter(rec=rec, user=user).exists():
            rat_obj = Rating.objects.get(rec=rec, user=user)
        else:
            rat_obj = Rating.objects.create(rec=rec,user=user)
            rat_obj.save()
        to_send=dict()
        if to_do == 'add':
            rat_obj.sav=True
            rat_obj.save()
            to_send['final_save']="Yes"
        elif to_do == 'remove':
            rat_obj.sav=False
            rat_obj.save()
            to_send['final_save']="No"
        return JsonResponse(json.dumps(to_send), safe=False)
    else:
        return HttpResponse('Not allowed')

def starTarget(request):
    if request.method == 'POST':
        rec = Recipe.objects.get(rec_id=request.POST.get('recNumber'))
        user = Everyone.objects.get(id=User.objects.get(username=request.POST.get('user')))
        new_rating = int(request.POST.get('to_save'))
        rat_obj = None
        to_send=dict()
        if Rating.objects.filter(rec=rec, user=user).exists():
            rat_obj = Rating.objects.get(rec=rec, user=user)
        else:
            rat_obj = Rating.objects.create(rec=rec,user=user)
            rat_obj.save()
        rat_obj.val=new_rating
        rat_obj.save()
        to_send['final_rating']=str(new_rating)
        return JsonResponse(json.dumps(to_send), safe=False)
    else:
        return HttpResponse('Not allowed')

def category(request, urlCategory):
    allCats = ['Indian', 'Chinese', 'Italian', 'Mexican', 'Thai', 'Other']
    if urlCategory in allCats:
        rec_objs = Recipe.objects.filter(category=urlCategory)
        rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals = findAllAboutRecs(rec_objs)
        context=dict()
        context['recs']=zip(rec_names, rec_desc, rec_hrs, rec_mins, rec_urls , rec_imgs, rec_cals)
        context['recNo'] = len(rec_names)
        context["MEDIA_URL"] = MEDIA_URL
        context['category'] = urlCategory+ " Cuisine"
        return render(request, 'kitchen/category.html', context)
    else:
        return HttpResponse("Not a valid category")
