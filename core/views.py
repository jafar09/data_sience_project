from django.shortcuts import render, HttpResponse , redirect
from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from .utils import is_ajax, classify_face
import base64
from logs.models import Log
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from profiles.models import Profile
from django.shortcuts import render
from django.http import HttpResponse
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

def login_view(request):
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return redirect('login')

# @login_required
def home_view(request):
    return render(request, 'main.html', {})

def find_user_view(request):
    if is_ajax(request):
        photo = request.POST.get('photo')
        _, str_img = photo.split(';base64')

        # print(photo)
        decoded_file = base64.b64decode(str_img)
        print(decoded_file)

        x = Log()
        x.photo.save('upload.png', ContentFile(decoded_file))
        x.save()

        res = classify_face(x.photo.path)
        if res:
            user_exists = User.objects.filter(username=res).exists()
            if user_exists:
                user = User.objects.get(username=res)
                profile = Profile.objects.get(user=user)
                x.profile = profile
                x.save()
                login(request, user)
                return JsonResponse({'success': True})
        return JsonResponse({'success': False})
    return render(request, 'main.html', {})

# registratsiya qismi boshlandi
def SignupPage_view(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request, 'signup.html')
# registratsiya qismi tugadi

# login qismi boshlandi
def LoginPage1_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login1.html')
# login qismi tugadi

def LogoutPage(request):
    logout(request)
    return redirect('login')


# eda_view boshlandi
def eda_view(request):
    if request.method == 'GET':
        return render(request, 'EDA.html')

    elif request.method == 'POST':
        notebook_path = 'C:/Users/Lenovo/Desktop/django-faceid/jupeter.ipynb'
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)

            # Daftaringizni bajarish
            ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
            ep.preprocess(nb, {'metadata': {'path': './'}})

            # Daftaringizni HTML formatiga o'zgartirish
            html_exporter = HTMLExporter()
            (body, resources) = html_exporter.from_notebook_node(nb)

            # HTML kontentni qaytarish
            return HttpResponse(body)

        except UnicodeDecodeError as e:
            return HttpResponse(f"UnicodeDecodeError: {e}", status=500)
        except Exception as e:
            return HttpResponse(f"Xato yuz berdi: {e}", status=500)
    return render(request, 'EDA.html')

 # eda_view tugadi

 # eda_view tugadi
# eda_view tugadi
