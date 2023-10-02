from django.shortcuts import render, HttpResponse, redirect
from social_media_app.models import User,UserProfile
from datetime import date,datetime
from django.contrib.auth.models import auth

# Create your views here.
from django.contrib.auth.decorators import login_required


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

        # Save form data to the session
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
        birthdate_str = request.POST.get('birthdate')  # Get the birthdate from the form
        try:
            # Parse the birthdate string into a date object (assuming it's in "yyyy-mm-dd" format)
            birthdate = date.fromisoformat(birthdate_str)
        except ValueError:
            # Handle invalid date format
            # You can add your error handling logic here
            pass

        if birthdate:
            age = calculate_age(birthdate)  # Calculate the age
            age_str = birthdate.strftime("%d %m %Y")  # Format age as "dd mm yyyy"

            tab2_data = {
                'age': age_str,
            }
            request.session['tab2_data'] = tab2_data  # Save tab2 data to the session
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
            tab3_data = {
            'username' : username,
            'password' : password,
            }
            User.objects.create_user(username=username,password=password)
            user=auth.authenticate(username=username,password=password)
            if user:
                request.session['user_id'] = user.id
                request.session['name']=user.username
                return redirect('tab-4')
            else:
                return render(request,'tab3.html',{'error':True,'error_message':"*Authentication Unsuccessfull"})
        else:
            error_message="*Passwords do not match"
            return render(request,'tab3.html',{'error':True,'error_message':error_message})
    else:
        return render(request, 'tab3.html' , {'disable_scroll' : disable_scroll})


# def tab4_view(request):
#     user_id = request.session.get('user_id')
#     disable_scroll=True
#     if request.method == 'POST' and user_id:
#         image=request.FILES.get('profilepic')
#         user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
#         # Update the profile with the new image
#         if image:
#             user_profile.image = image
#             user_profile.save()
#         discription= request.POST['discription']
#         user=User.objects.get(id=user_id)
#         auth.login(request,user)
#         request.session['user_id']=user.id
#         request.session['image']=user.image
#         request.session['discription']=user.discription
#         return redirect('index')
    
#     else:
#         return render(request , 'tab4.html' , {'disable_scroll' : disable_scroll})






def tab4_view(request):
    if request.method == 'POST':
        # Assuming you have a way to create a new user account
        # and authenticate the user after submitting data
        username = request.POST['username']
        password = request.POST['password']

        # Create a new user account
        user = User.objects.create_user(username=username, password=password)

        # Authenticate the user
        auth.login(request, user)

        # Continue processing the profile image upload
        image = request.FILES.get('profilepic')
        if image:
            user.userprofile.image = image
            user.userprofile.save()

        return redirect('index')
    else:
        return render(request, 'tab4.html')






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
    image=request.session.get('image')
    if not discription:
        discription = ""
    if not image:
        return render(request,'profile.html',{'discription':discription,'username':username})
                      
    return render(request,'profile.html',{'discription':discription,'username':username,'image':image}, {'disable_scroll' : disable_scroll})

@login_required
def create_view(request):
    return render(request,'create.html')