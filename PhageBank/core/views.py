from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
import csv
from django.conf import settings
from .filters import PhageFilter
from io import StringIO
from io import TextIOWrapper
from PhageBank.core.forms import Add_ResearchForm, AForm, AIForm, Edit_Phage_DataForm, Edit_ResearcherForm, Edit_ResearchForm, Edit_IsolationDataForm, Edit_Experiment_Form
from PhageBank.core.forms import SignUpForm, UploadFileForm, LinkForm, LoginForm, Add_Phage_DataForm, Add_ResearcherForm, Add_Experiment_Form,Isolation_Form
from PhageBank.core.models import PhageData, PreData, ExperimentData, IsolationData
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.template import RequestContext
from django.contrib.messages import get_messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

import json
import os
from csvvalidator import *
import datetime
import sqlite3
import pandas as pd

def count(dest_dir):
    count = 0;
    for filename in os.listdir(dest_dir):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            count=count+1;
            continue
    return count

def list_path(dest_dir):
    list_path = [];
    for filename in os.listdir(dest_dir):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            list_path.append(filename)
            continue
    return list_path

def logged_in_index(request):
    last_three = PhageData.objects.all().order_by('-id')[:3]
    dest_dir1=dest_dir2=dest_dir3= name1=name2=name3=""
    count1 = count2 = count3 = -1
    try:
        name1 = last_three[0].phage_name
        dest_dir1 = list_path(os.path.join(settings.MEDIA_ROOT, "images", last_three[0].phage_name))
        count1 = count(os.path.join(settings.MEDIA_ROOT, "images", last_three[0].phage_name))
    except:
        pass

    try:
        name2 = last_three[1].phage_name
        dest_dir2 = list_path(os.path.join(settings.MEDIA_ROOT, "images", last_three[1].phage_name))
        count2 = count(os.path.join(settings.MEDIA_ROOT, "images", last_three[1].phage_name))

    except:
        pass

    try:
        name3 = last_three[2].phage_name
        dest_dir3 = list_path(os.path.join(settings.MEDIA_ROOT, "images", last_three[2].phage_name))
        count3 = count(os.path.join(settings.MEDIA_ROOT, "images", last_three[2].phage_name))

    except:
        pass
    return render(request, 'logged_in_index.html',{'login_status': request.user.is_authenticated(),
                                                       'username': request.user.username,
                                                       'phage1': name1,
                                                       'phage2': name2,
                                                       'phage3': name3,
                                                       'dest_dir1': dest_dir1,
                                                       'dest_dir2': dest_dir2,
                                                       'dest_dir3': dest_dir3,
                                                       'count1': count1,
                                                       'count2': count2,
                                                       'count3': count3
                                                       })

def mylogout(request):
    logout(request)
    last_three = PhageData.objects.all().order_by('-id')[:3]
    dest_dir1 = dest_dir2 = dest_dir3 = name1 = name2 = name3 = ""
    count1 = count2 = count3 = -1
    try:
        name1 = last_three[0].phage_name
        dest_dir1 = list_path(os.path.join(settings.MEDIA_ROOT, "images", last_three[0].phage_name))
        count1 = count(os.path.join(settings.MEDIA_ROOT, "images", last_three[0].phage_name))
    except:
        pass

    try:
        name2 = last_three[1].phage_name
        dest_dir2 = list_path(os.path.join(settings.MEDIA_ROOT, "images", last_three[1].phage_name))
        count2 = count(os.path.join(settings.MEDIA_ROOT, "images", last_three[1].phage_name))

    except:
        pass

    try:
        name3 = last_three[2].phage_name
        dest_dir3 = list_path(os.path.join(settings.MEDIA_ROOT, "images", last_three[2].phage_name))
        count3 = count(os.path.join(settings.MEDIA_ROOT, "images", last_three[2].phage_name))

    except:
        pass
    messages.success(request, 'You have successfully logged out.', extra_tags='alert')
    return render(request, 'logged_in_index.html',{'login_status': request.user.is_authenticated(),
                                                       'username': request.user.username,
                                                       'phage1': name1,
                                                       'phage2': name2,
                                                       'phage3': name3,
                                                       'dest_dir1': dest_dir1,
                                                       'dest_dir2': dest_dir2,
                                                       'dest_dir3': dest_dir3,
                                                       'count1': count1,
                                                       'count2': count2,
                                                       'count3': count3
                                                       })
def signup(request):
    data = dict()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = SignUpForm()

    context = {'form': form}
    data['html_form'] = render_to_string('partial_signup.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(data)

def mylogin(request):
    msg = dict()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print (form.errors)
        username = request.POST['username']
        password = request.POST['password']
        if form.is_valid():
            msg['form_is_valid'] = True
        else:
            form.add_error('password', 'Please enter a correct username and password. Note that both fields are case-sensitive.')
            msg['form_is_valid'] = False

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    msg['form_is_valid'] = True
                else:
                    msg['form_is_valid'] = False
    else:
        form = AuthenticationForm()
    context = {'form': form}
    msg['html_form'] = render_to_string('partial_login.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(msg)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('logout')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form,
                                                    'login_status': request.user.is_authenticated(),
                                                    'username': request.user.username,
                                                    })


def handle_uploaded_file(f, dest):
    with open(dest, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


#Fill the model object in similar fashion
def fillExpObject(expform, phage):
    exp =  ExperimentData.objects.create(expkey=phage)
    exp.expkey = phage
    exp.owner = expform.cleaned_data.get('owner')
    exp.timestamp = expform.cleaned_data.get('TimeStamp')
    exp.category = expform.cleaned_data.get('category')
    exp.short_name = expform.cleaned_data.get('short_name')
    exp.full_name = expform.cleaned_data.get('full_name')
    exp.methods = expform.cleaned_data.get('methods')
    exp.results = expform.cleaned_data.get('results')
    exp.save()

def fillExpObjectedit(expform, exp):
    exp.owner = expform.cleaned_data.get('owner')
    exp.timestamp = expform.cleaned_data.get('TimeStamp')
    exp.category = expform.cleaned_data.get('category')
    exp.short_name = expform.cleaned_data.get('short_name')
    exp.full_name = expform.cleaned_data.get('full_name')
    exp.methods = expform.cleaned_data.get('methods')
    exp.results = expform.cleaned_data.get('results')
    exp.save()

def fillIsoltionObject(isoform, phage):
    iso = IsolationData.objects.create(isokey=phage)
    iso.isokey = phage
    iso.owner_name = isoform.cleaned_data.get('owner_name')
    iso.location = isoform.cleaned_data.get('location')
    iso.type1 = isoform.cleaned_data.get('type1')
    iso.TimeStamp = isoform.cleaned_data.get('timestamp')
    iso.save()

def fillIsoltionObjectedit(isoform, iso):
    iso.owner_name = isoform.cleaned_data.get('owner_name')
    iso.location = isoform.cleaned_data.get('location')
    iso.type1 = isoform.cleaned_data.get('type')
    iso.TimeStamp = isoform.cleaned_data.get('TimeStamp')
    iso.save()

def validate_latest_phage(query_results):
    if(query_results.count()>0):
        latest = query_results.latest('id')
        return latest.phage_name
    else:
        return ""

@login_required
def add_phage(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            pform = Add_Phage_DataForm(request.POST)    #phage_name
            rrform = Add_ResearcherForm(request.POST)
            rform = Add_ResearchForm(request.POST)      #CPT ID
            expform = Add_Experiment_Form(request.POST)
            isoform = Isolation_Form(request.POST)
            aform = AForm(request.POST, request.FILES)
            aiform = AIForm(request.POST)

            if pform.is_valid() and rrform.is_valid() and rform.is_valid() and expform.is_valid() and isoform.is_valid() \
                    and aform.is_valid() and aiform.is_valid():
                phagename = pform.cleaned_data.get('phage_name')
                CPTid = rform.cleaned_data.get('phage_CPT_id')

                #approvePhage = 1 if no duplicates in phage_name. 0 otherwise
                #approveCPTid = 1 if no duplicates in CPT id
                #duplicatePhagesPhages : list of phages due to duplicates in phage names
                #duplicatePhagesCPTid : list of CPT ids due to duplicates in phage names
                #duplicateCPTidPhages : list of phages due to duplicates in CPT ids
                #duplicateCPTidCPTid : list of duplicate CPT ids

                #chkDuplicatesFlag = 0
                chkDuplicatesFlag = int(request.POST['flag'])
                #chkDuplicatesFlag = 1

                msg = dict()

                if chkDuplicatesFlag==1:
                    approvePhage, approveCPTid, duplicatePhagesPhages, duplicatePhagesCPTid, duplicateCPTidPhages\
                    , duplicateCPTidCPTid = checkDuplicatesInAddPhage(phagename, CPTid)

                    print(approvePhage, approveCPTid)

                    msg['approvePhage']=approvePhage
                    msg['approveCPTid']=approveCPTid

                    if (approvePhage==0 or approveCPTid==0):
                        msg['duplicatePhagesPhages']=json.dumps(duplicatePhagesPhages)
                        msg['duplicatePhagesCPTid']=json.dumps(duplicatePhagesCPTid)
                        msg['duplicateCPTidPhages']=json.dumps(duplicateCPTidPhages)
                        msg['duplicateCPTidCPTid']=json.dumps(duplicateCPTidCPTid)

                        return JsonResponse(msg)

                pform.save()

                phage = PhageData.objects.get(phage_name=phagename)
                phage.phage_CPT_id = rform.cleaned_data.get('phage_CPT_id')
                phage.phage_isolator_loc = rform.cleaned_data.get('phage_isolator_loc')
                phage.phage_all_links = aiform.cleaned_data.get('link')
                phage.phage_isolator_name = rrform.cleaned_data.get('phage_isolator_name')
                phage.phage_experimenter_name = rrform.cleaned_data.get('phage_experimenter_name')
                phage.phage_submitted_user = request.user.username
                phage.phage_lab = rrform.cleaned_data.get('phage_lab')

                phage.save()
                fillIsoltionObject(isoform, phage)

                fillExpObject(expform, phage)
                # print(phage.phage_submitted_user)
                phagedoc = aform.cleaned_data.get('doc')
                phageimage = aform.cleaned_data.get('image')
                dest_dir = os.path.join(settings.MEDIA_ROOT, "images", phagename)
                docs_dest_dir = os.path.join(settings.MEDIA_ROOT, "docs", phagename)
                try:
                    os.mkdir(dest_dir)
                    os.mkdir(docs_dest_dir)
                except:
                    pass
                dest = os.path.join(dest_dir, str(phageimage))
                docsdest = os.path.join(docs_dest_dir, str(phagedoc))
                if phageimage is None:
                    pass
                else:
                    handle_uploaded_file(phageimage, dest)
                if phagedoc is None:
                    pass
                else:
                    handle_uploaded_file(phagedoc, docsdest)

                # query_results = PhageData.objects.all()

                return JsonResponse(msg)

                #if the data is valid
                #render(request, 'view_phages.html', {'add_status':'true','query_results':query_results}  )
                #render(request, 'view_phages.html', {'add_status':'true','query_results':query_results ,
                #                                            'login_status': request.user.is_authenticated(),
                #                                            'username': request.user.username})

            else:
                pform.add_error("phage_name","This field is required.")
                rform.add_error("phage_CPT_id","This field is required.")
                return render(request, 'add_phage.html', {'pform': pform,
                                                          'rrform': rrform,
                                                          'rform': rform,
                                                          'expform': expform,
                                                          'isoform': isoform,
                                                          'aform': aform,
                                                          'aiform': aiform,
                                                          'login_status': request.user.is_authenticated(),
                                                          'username': request.user.username,
                                                         })
        else:
            pform = Add_Phage_DataForm()
            rrform = Add_ResearcherForm()
            rform = Add_ResearchForm()
            expform = Add_Experiment_Form()
            isoform = Isolation_Form()
            aform = AForm()
            aiform = AIForm()
            return render(request, 'add_phage.html', {'pform': pform,
                                                      'rrform': rrform,
                                                      'rform': rform,
                                                      'expform': expform,
                                                      'isoform':isoform,
                                                      'aform': aform,
                                                      'aiform': aiform,
                                                      'login_status': request.user.is_authenticated(),
                                                      'username': request.user.username,
                                                     })
#this form show the phages per user
def my_phages(request):
    query_results = PhageData.objects.filter(phage_submitted_user=request.user.username)
    name = validate_latest_phage(query_results)
    return render(request, 'view_phages.html', {'query_results': query_results,
                                                'edit_status':'false','add_status':'false',
                                                'delete_status':'false','latest':name,
                                               'login_status': request.user.is_authenticated(),
                                               'username': request.user.username
                                               })
#this form shows all the phages
def view_phages(request):
    query_results = PhageData.objects.all()
    name = validate_latest_phage(query_results)
    return render(request, 'view_phages.html', {'query_results': query_results,
                                                'edit_status': 'false', 'add_status': 'false',
                                                'delete_status': 'false', 'latest': name,
                                                'login_status': request.user.is_authenticated(),
                                                'username': request.user.username
                                                })
@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def delele_all_phages(request):
    phage = PhageData.objects.all().delete()
    query_results = PhageData.objects.all()
    return render(request, 'view_phages.html', {'query_results': query_results,
                                                'edit_status':'false','add_status':'false',
                                                'delete_status':'false',
                                               'login_status': request.user.is_authenticated(),
                                               'username': request.user.username
                                               })
#this form shows a particular phage
def view_phage(request):
    phageName = request.GET.get('name')
    phage = PhageData.objects.get(phage_name=phageName)
    previous_names = phage.PhageName.all()
    expdata = phage.PName.all()
    isodata = phage.iso_phageName.all()
    dest_dir = os.path.join(settings.MEDIA_ROOT, "images", phageName)
    list_path=[]
    count = 0;
    try:
        for filename in os.listdir(dest_dir):
            if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                list_path.append(filename)
                count=count+1;
                continue
            else:
                continue
    except:
        pass
    return render(request, 'view_phage.html', {'item': phage,'previous_names':previous_names,'expdata':expdata,'isodata':isodata,
                                              'login_status': request.user.is_authenticated(),'dest_dir':list_path,'count':count,
                                              'username': request.user.username
                                              })

@login_required
def deletephages(request):
    if request.user.is_authenticated():
        x = request.GET.get('name')
        dest_dir = os.path.join(settings.MEDIA_ROOT, "images", x)
        docs_dest_dir = os.path.join(settings.MEDIA_ROOT, "docs", x)
        try:
            os.rmdir(dest_dir)
            os.rmdir(docs_dest_dir)
        except:
            pass
        phage = PhageData.objects.get(phage_name=x).delete()
        query_results = PhageData.objects.all()
        name = validate_latest_phage(query_results)
        return render(request, 'view_phages.html', {'query_results': query_results,'delete_status':'true',
                                               'login_status': request.user.is_authenticated(),'latest':name,
                                               'username': request.user.username
                                               })
    else:
        #messages.error(request,'Login or signup first!')
        return render(request,'login.html',
                      {'login_status': request.user.is_authenticated()
                       })


def search_phage(request):
    phage_list = PhageData.objects.all()
    request.GET._mutable = True
    print("$$$$")
    if request.GET.get('submitted_year_gt'):
        #print(request.GET['submitted_year_gt'])
        if int(request.GET.get('submitted_year_gt')) < 0:
            messages.error(request, 'Invalid value for "Year Submitted After" entered. Setting it to 1')
            request.GET['submitted_year_gt'] = 1
        #print(request.GET['submitted_year_gt'])
    if request.GET.get('submitted_year_lt'):
        if int(request.GET.get('submitted_year_lt')) < 0:
            messages.error(request, 'Invalid value for "Year Submitted Before" entered. Setting it to 1')
            request.GET['submitted_year_lt'] = 1
    if request.GET.get('submitted_month_gt'):
        if int(request.GET.get('submitted_month_gt')) < 0:
            messages.error(request, 'Invalid value for "Month Submitted After" entered. Setting it to 1')
            request.GET['submitted_month_gt'] = 1
    if request.GET.get('submitted_month_lt'):
        if int(request.GET.get('submitted_month_lt')) < 0:
            messages.error(request, 'Invalid value for "Month Submitted Before" entered. Setting it to 1')
            request.GET['submitted_month_lt'] = 1

    phage_filter = PhageFilter(request.GET, queryset=phage_list)
    return render(request, 'search_phage.html', {'filter': phage_filter,
                                                 'login_status': request.user.is_authenticated(),
                                                 'username': request.user.username,
                                                 })

def check_entry(name):
    print(PhageData.objects.filter(phage_name=name).count())
    if (PhageData.objects.filter(phage_name=name).count() == 0 and PreData.objects.filter(phagename=name).count()==0 ):
        return False
    else:
        return True

@login_required
def editPhage(request):
    if request.user.is_authenticated():
        name = request.GET.get('name')
        phage = PhageData.objects.get(phage_name = name)
        isodata = IsolationData.objects.filter(isokey = phage)
        expdata = ExperimentData.objects.filter(expkey = phage)
        last = isodata.latest('id')
        last_exp = expdata.latest('id')
        pform = Edit_Phage_DataForm(request.POST, instance=phage, initial = {'phage_name':phage.phage_name })
        rrform = Edit_ResearcherForm(request.POST, instance=phage)
        rform = Edit_ResearchForm(request.POST, instance=phage)
        isoform = Edit_IsolationDataForm(request.POST)
        expform = Edit_Experiment_Form(request.POST)
        aform = AForm(request.POST, request.FILES)
        aiform = AIForm(request.POST)
        if request.method=="POST":
            if pform.is_valid() and rrform.is_valid() and rform.is_valid() and aform.is_valid() and aiform.is_valid()\
                    and isoform.is_valid() and expform.is_valid():
                curr_phage = pform.cleaned_data.get('phage_name')
                if(check_entry(curr_phage) and curr_phage!=name):
                    return render(request, 'EditPhage.html', {'item': phage,
                                                              'pform': pform,
                                                              'rrform': rrform,'expform':expform,
                                                              'rform': rform,
                                                              'aform': aform,
                                                              'aiform': aiform,'duplicate':'true',
                                                              'isoform':isoform,'iso':last,'exp':last_exp,
                                                              'login_status': request.user.is_authenticated(),
                                                              'username': request.user.username,
                                                             })
                phage.phage_name = curr_phage
                if(name!=phage.phage_name and PreData.objects.filter(phagename = name).count()==0):
                    obj = PreData.objects.create(testkey=phage)
                    obj.testkey = phage
                    obj.phagename = name
                    print (obj.phagename)
                    obj.save()
                    print (phage.PhageName.all().values())
                #phage = PhageData.objects.get(phage_name=phagename)
                phage.phage_isolator_name = rrform.cleaned_data.get('phage_isolator_name')
                phage.phage_experimenter_name = rrform.cleaned_data.get('phage_experimenter_name')
                phage.phage_CPT_id = rform.cleaned_data.get('phage_CPT_id')
                phage.phage_isolator_loc = rform.cleaned_data.get('phage_isolator_loc')
                phage.phage_all_links = aiform.cleaned_data.get('link')
                phage.phage_lab = rrform.cleaned_data.get('phage_lab')
                #isolator_data = phage.iso_phageName.objects.latest(iso_phageName)
                pform.save()
                phage.save()
                #last.delete()
                fillExpObjectedit(expform, last_exp)
                fillIsoltionObjectedit(isoform, last)
                phagedoc = aform.cleaned_data.get('doc')
                phageimage = aform.cleaned_data.get('image')
                dest_dir_old = os.path.join(settings.MEDIA_ROOT, "images", name)
                docs_dest_dir_old = os.path.join(settings.MEDIA_ROOT, "docs", name)
                dest_dir = os.path.join(settings.MEDIA_ROOT, "images", phage.phage_name)
                docs_dest_dir = os.path.join(settings.MEDIA_ROOT, "docs", phage.phage_name)
                try:
                    os.rename(dest_dir_old,dest_dir)
                    os.rename(docs_dest_dir_old,docs_dest_dir)
                except:
                   pass
                dest = os.path.join(dest_dir, str(phageimage))
                docsdest = os.path.join(docs_dest_dir, str(phagedoc))
                if phageimage is None:
                    pass
                else:
                    handle_uploaded_file(phageimage, dest)
                if phagedoc is None:
                    pass
                else:
                    handle_uploaded_file(phagedoc, docsdest)
                query_results = PhageData.objects.all()
                lname = validate_latest_phage(query_results)
                return render(request, 'view_phages.html', {'edit_status':'true','query_results':query_results,'latest':lname,
                                                            'login_status': request.user.is_authenticated(),
                                                            'username': request.user.username}  )
            else:
                phage = PhageData.objects.get(phage_name=name)
                phage.save()
                return render(request, 'EditPhage.html', {'item': phage,
                                                          'pform': pform,
                                                          'rrform': rrform,'expform':expform,
                                                          'rform': rform,
                                                          'aform': aform,
                                                          'aiform': aiform,
                                                          'isoform':isoform,'iso':last,'exp':last_exp,
                                                          'login_status': request.user.is_authenticated(),
                                                          'username': request.user.username,
                                                         })
        else:
            pform = Edit_Phage_DataForm(request.POST, instance=phage)
            rrform = Edit_ResearcherForm(request.POST, instance=phage)
            rform = Edit_ResearchForm(request.POST, instance=phage)
            isoform = Edit_IsolationDataForm(request.POST)
            expform = Edit_Experiment_Form(request.POST)
            aform = AForm()
            aiform = AIForm()
            return render(request, 'EditPhage.html', {'item': phage,
                                                      'pform': pform,
                                                      'rrform': rrform,
                                                      'rform': rform,
                                                      'aform': aform,
                                                      'aiform': aiform, 'isoform' : isoform,'expform':expform,
                                                      'iso':last,
                                                      'exp': last_exp,
                                                      'login_status': request.user.is_authenticated(),
                                                      'username': request.user.username,
                                                     })
    else:
        return render(request,'Login.html',
                      {'login_status': request.user.is_authenticated()
                       })


def func(phagename):
    dest_dir = os.path.join(settings.MEDIA_ROOT, "images", phagename)
    docs_dest_dir = os.path.join(settings.MEDIA_ROOT, "docs", phagename)
    try:
        os.mkdir(dest_dir)
        os.mkdir(docs_dest_dir)
    except:
        pass


def populate(reader, request):
    fields = reader.fieldnames
    for row in reader:
        flag = 0
        obj = PhageData.objects.create()
        iso = IsolationData.objects.create(isokey = obj)
        exp = ExperimentData.objects.create(expkey = obj)
        if 'phage_name' in fields:
            name = row['phage_name']
            if not name:
                flag = 0
            elif(PhageData.objects.filter(phage_name=name).count() == 0 and PreData.objects.filter(phagename=name).count() == 0):
                obj.phage_name = name
            else:
                obj.delete()
                exp.delete()
                iso.delete()
                if (PhageData.objects.filter(phage_name=name).count() > 0):
                    obj = PhageData.objects.get(phage_name=name)
                else:
                    obj1 = PreData.objects.get(phagename=name)
                    obj = obj1.testkey

                isodata = IsolationData.objects.filter(isokey=obj)
                expdata = ExperimentData.objects.filter(expkey=obj)
                iso = isodata.latest('id')
                exp = expdata.latest('id')
            flag = 1
        if 'phage_host_name' in fields:
            obj.phage_host_name = row['phage_host_name']
        if 'phage_isolator_name' in fields:
            obj.phage_isolator_name = row['phage_isolator_name']
        if 'phage_experimenter_name' in fields:
            obj.phage_experimenter_name = row['phage_experimenter_name']
        if 'phage_CPT_id' in fields:
            obj.phage_CPT_id = row['phage_CPT_id']
        if 'phage_isolator_loc' in fields:
            obj.phage_isolator_loc = row['phage_isolator_loc']
        if 'owner_name' in fields:
            iso.owner_name = row['owner_name']
        if 'location' in fields:
            iso.location = row['location']
        if 'type' in fields:
            iso.type = row['type']
        if 'TimeStamp' in fields:
            iso.TimeStamp = row['TimeStamp']
        if 'owner' in fields:
            exp.owner = row['owner']
        if 'timestamp' in fields:
            exp.timestamp = row['timestamp']
        if 'methods' in fields:
            exp.methods = row['methods']
        if 'results' in fields:
            exp.results = row['results']
        if 'short_name' in fields:
            exp.short_name = row['short_name']
        if 'full_name' in fields:
            exp.full_name = row['full_name']
        if 'category' in fields:
            exp.category = row['category']
        obj.phage_submitted_user = request.user.username

        if flag == 0:
            obj.delete()
            exp.delete()
            iso.delete()
        else:
            obj.save()
            func(obj.phage_name)
            iso.save()
            exp.save()



@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def model_form_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            paramFile = TextIOWrapper(request.FILES['file'].file, encoding=request.encoding)
            reader = csv.DictReader(paramFile,delimiter=';',skipinitialspace=True,)
            populate(reader, request)
            query_results = PhageData.objects.all()
            lname = validate_latest_phage(query_results)
            return render(request, 'view_phages.html', {'query_results': query_results,
                                                        'edit_status': 'false', 'add_status': 'false',
                                                        'delete_status': 'false','latest':lname,
                                                        'login_status': request.user.is_authenticated(),
                                                        'username': request.user.username
                                                        })
    else:
        form = UploadFileForm()
    return render(request, 'model_form_upload.html', {'form': form,'login_status': request.user.is_authenticated(),
                                                        'username': request.user.username})

def checkDuplicatesInAddPhage(phage_name, phage_CPT_id):
    #db=sqlite3.connect('db.sqlite3')
    #params={'phage_name':phage_name, 'phage_CPT_id':phage_CPT_id}
    #q1="SELECT phage_name, phage_CPT_id FROM core_phagedata WHERE phage_name='{phage_name}'"
    #rowsPhage = pd.read_sql_query(q1.format(**params), db)

    rowsPhage = PhageData.objects.filter(phage_name = phage_name).values('phage_name','phage_CPT_id')
    #.values() is a list of dict

    rowsCPTid = PhageData.objects.filter(phage_CPT_id = phage_CPT_id).values('phage_name','phage_CPT_id')

    duplicatePhagesPhages = [d['phage_name'] for d in rowsPhage] # rowsPhage["phage_name"].values.tolist()
    #print(duplicatePhagesPhages)

    duplicatePhagesCPTid = [d['phage_CPT_id'] for d in rowsPhage]

    duplicateCPTidPhages = [d['phage_name'] for d in rowsCPTid]
    duplicateCPTidCPTid = [d['phage_CPT_id'] for d in rowsCPTid]

    approvePhage=1
    approveCPTid=1
    if len(rowsPhage)>0:
        approvePhage=0

    if len(rowsCPTid)>0:
        approveCPTid=0

    return approvePhage, approveCPTid, duplicatePhagesPhages, duplicatePhagesCPTid, duplicateCPTidPhages\
    , duplicateCPTidCPTid

#def checkDuplicatesInFile(decoded_file):
#    db=sqlite3.connect('db.sqlite3')
#    io_string = io.StringIO(decoded_file)
#    
#    phage_names=[]
#    
#    for line in csv.reader(io_string, delimiter=','):
#        phage_names.append(line[0])
#    
#    df=pd.read_sql_query('SELECT phage_name FROM core_phagedata',db)
#    
#    stored_phages = df["phage_name"].values.tolist()
#    
#    common_phages = set(phage_names).intersection(stored_phages)
#    
#    approveFlag=1
#    if len(common_phages)>0:
#        approveFlag=0
#        
#    #print(common_phages)
#    return common_phages, approveFlag










