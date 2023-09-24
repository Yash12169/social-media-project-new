from django.shortcuts import render, HttpResponse, redirect
from social_media_app.models import User
from datetime import date,datetime
# Create your views here.

def index_view(request):
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

        if password == repassword:
            tab3_data = {
            'username' : username,
            'password' : password,
            }
            request.session['tab3_data'] = tab3_data
            return redirect('tab-4')
        
        else:
            error_message="*Passwords do not match"
            return render(request,'tab3.html',{'error':True,'error_message':error_message})
    else:
        return render(request, 'tab3.html' , {'disable_scroll' : disable_scroll})


def tab4_view(request):
    
    disable_scroll=True
    return render(request , 'tab4.html' , {'disable_scroll' : disable_scroll})


def login_view(request):
    return render(request, 'login.html')


def privacy_view(request):
    return render(request,'privacy.html')


def about_view(request):
    return render(request,'about.html')