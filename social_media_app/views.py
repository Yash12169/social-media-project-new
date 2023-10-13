from django.shortcuts import render, redirect
from social_media_app.models import User,UserProfile,Profile
from datetime import date
from django.contrib.auth.models import auth
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from .forms import ImageUploadForm,DiscriptionChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def home_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request, "homepage.html")

def tab1_view(request):
    disable_scroll=True
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        country = request.POST['country']
        request.session['tab1_data'] = {
            'name': name,
            'gender': gender,
            'country': country,
        }
        request.session['authenticated_step'] = 1
        return redirect('tab-2')
    else:
        return render(request, "tab1.html" , {'disable_scroll' : disable_scroll})

def calculate_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def tab2_view(request):
    authenticated_step = request.session.get('authenticated_step', 0)
    disable_scroll = True
    if authenticated_step<1:
        return redirect('tab-1')
    if request.method == 'POST':
        birthdate_str = request.POST.get('birthdate')
        try:
            birthdate = date.fromisoformat(birthdate_str)
        except ValueError:
            pass
        if birthdate:
            age = calculate_age(birthdate)  
            age_str = birthdate.strftime("%d %m %Y")  

            tab2_data = {
                'age': age_str,
            }
            request.session['tab2_data'] = tab2_data  
            if age>=18:
                return redirect('tab-3')
            else:
                error_message="*You must be above the age of 18 to create a account"
                return render(request,'tab2.html',{'error':True,'error_message' : error_message})
    else:
        return render(request, 'tab2.html', {'disable_scroll': disable_scroll})

def tab3_view(request): 
    disable_scroll=True
    tab2_data = request.session.get('tab2_data')
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        repassword=request.POST.get('repassword')
        if User.objects.filter(username=username).exists():
            error_message = "*Username is already taken"
            return render(request, 'tab3.html', {'error': True, 'error_message': error_message})
        if password == repassword:
            request.session['username'] = username
            request.session['password'] = password
            return redirect('tab-4')
        else:
            error_message="*Passwords do not match"
            return render(request,'tab3.html',{'error':True,'error_message':error_message})
    else:
        return render(request, 'tab3.html' , {'disable_scroll' : disable_scroll})

def tab4_view(request):
    username=request.session.get('username')
    password=request.session.get('password')
    disable_scroll=True
    if request.method == 'POST':
        profilepic=request.FILES.get('profilepic')
        request.session['profilepic'] = profilepic
        discription= request.POST['discription']
        request.session['discription']=discription
        User.objects.create_user(username=username,password=password)
        user=auth.authenticate(username=username,password=password)
        if user:
           
            auth.login(request,user)
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.profilepic = profilepic
            user_profile.save()
            return redirect('index')
        else:
            return render(request,'tab4.html',{'error':True,'error_message':"*Authentication Unsuccessfull"})
    
    else:
        return render(request , 'tab4.html' , {'disable_scroll' : disable_scroll})

def login_view(request):
    disable_scroll=True
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        request.session
        user=auth.authenticate(username=username,password=password)
        if user:
            request.session['username']=user.username
            auth.login(request,user)
            return redirect('index')
        else:
            error_message="*incorrect username or password"
            return render(request,'login.html',{'error':True,"error_message":error_message})
    else:
        return render(request, 'login.html' , {'disable_scroll' : disable_scroll} )

def privacy_view(request):
    return render(request,'privacy.html')

def about_view(request):
    return render(request,'about.html')

def index_view(request):
    username=request.session.get('username')
    if not username:
        username=request.session.get('name')
    return render(request,'index.html',{'username':username})

@login_required
def log_out_view(request):
    auth.logout(request)
    return redirect('/')

@login_required
def profile_view(request):
    disable_scroll=True
    username=request.session.get('username')
    discription=request.session.get('discription')
    if not discription:
        discription = ""
    profilepic = UserProfile.objects.get(user=request.user).profilepic  
    return render(request,'profile.html',{'profilepic':profilepic,'discription':discription,'username':username,'disable_scroll' : disable_scroll})

@login_required
def create_view(request):
    return render(request,'create.html')

@login_required
def settings_view(request):
    disable_scroll=True
    return render(request,'settings.html',{'disable_scroll' : disable_scroll})

@login_required
def edit_profile_view(request):
    username=request.session.get('username')
    discription=request.session.get('discription')
    profilepic=UserProfile.objects.get(user=request.user).profilepic
    if not discription:
        discription=""
    data={
        'username':username,
        'discription':discription,
        'profilepic':profilepic

    }
    return render(request,'editprofile.html',data)

class ImageUploadView(FormView):
    form_class = ImageUploadForm
    template_name = 'changeprofile.html'
    success_url = reverse_lazy('profile_view')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        if not created:
            user_profile.profilepic = form.cleaned_data['profilepic']
            user_profile.save()
        else:
            form.instance.user = self.request.user 
            form.save()  
        
        return super().form_valid(form)

class ImageListView(ListView):
    model = UserProfile
    template_name = 'profile.html'
    context_object_name = 'images'

def change_discription(request):
    if request.method=="POST":
        form=DiscriptionChangeForm
        discription=request.session.get('discription')
        discriptionnew=request.POST.get('discription')
        if not discriptionnew:
            discriptionnew=discription
        return render(request,'profile.html',{'discriptionnew':discriptionnew})
    form=DiscriptionChangeForm
    return render(request,'changediscription.html',{'form':form})

def delete_account_warn(request):
    return render(request,'deleteaccount.html')

def delete_account(request):
    
    user=request.user
    user.delete()
    auth.logout(request)
    return render(request,'confirmdelete.html')
    
    
    