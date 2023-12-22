from django.shortcuts import render, redirect,get_object_or_404
from social_media_app.models import User,UserProfile,Post,LikePost,Comment,Follow
from django.http import JsonResponse,HttpResponseRedirect
from datetime import date
from django.contrib.auth.models import auth
from django.urls import reverse_lazy,reverse
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from .forms import ImageUploadForm,DiscriptionChangeForm,CreatePostForm
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
            user_profile, created = UserProfile.objects.get_or_create(user=user,profilepic=profilepic,discription=discription)
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

@login_required
def index_view(request):
    user=request.user
    post_id=request.session.get('post_id')
    posts = Post.objects.all().order_by('-created_at')
    username = request.session.get('username')
    userprofile = None
    for post in posts:
        post.likes_count = request.session.get(f'CountLike_{post.id}', 0)

    if not username:
        username = request.session.get('name')
    if username:
        try:
            user= User.objects.get(username=username)
            userprofile = UserProfile.objects.get(user=user).profilepic.url
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            pass

    following = Follow.objects.filter(follower = user)
    follower = Follow.objects.filter(following = user)
    posts = []
    for follow in following:
        user_being_followed=follow.following   
        user_posts=Post.objects.filter(user=user_being_followed).order_by('-created_at')
        posts.extend(user_posts)
    user_post=Post.objects.filter(user=user).order_by('-created_at')
    posts.extend(user_post)
    return render(request, 'index.html', {'posts': posts,'following':following,'follower':follower,'post_id':post_id,'userprofile': userprofile})

@login_required
def log_out_view(request):
    auth.logout(request)
    return redirect('/')

@login_required
def profile_view(request):
    disable_scroll=True
    username=request.session.get('username')
    
    # discriptionnew = request.session.get('discriptionnew')
    # if not discription:
    #     discription = ""
    # if not discriptionnew:
    #     discriptionnew=discription
    user=request.user
    user_post=Post.objects.filter(user=user)
    post_count=user_post.count()
    profilepic = UserProfile.objects.get(user=request.user).profilepic 
    discription= UserProfile.objects.get(user=request.user).discription 
    return render(request,'profile.html',{'post_count':post_count,'profilepic':profilepic,'discription':discription,'username':username,'disable_scroll' : disable_scroll})

@login_required
def create_view(request):
    if request.method=='POST':
        form=CreatePostForm(request.POST,request.FILES)
        if form.is_valid:
            post=form.save(commit=False)
            post.user=request.user
            user_profile= UserProfile.objects.get(user=request.user)
            post.user_profile=user_profile
            post.save()
            request.session['post_id']=post.id
            return redirect('index')       
    else:
        form=CreatePostForm
    return render(request,'create.html',{'form':form})

@login_required
def settings_view(request):
    disable_scroll=True
    return render(request,'settings.html',{'disable_scroll' : disable_scroll})

@login_required
def edit_profile_view(request):
    username=request.session.get('username')
    discription=UserProfile.objects.get(user=request.user).discription
    profilepic=UserProfile.objects.get(user=request.user).profilepic
    # if not discription:
    #     discription=""
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
        # discription=request.session.get('discription')
        discriptionnew=request.POST.get('discription')
        user_profile=UserProfile.objects.get(user=request.user)
        user_profile.discription=discriptionnew
        user_profile.save()


        user_profile=UserProfile.objects.get(user=request.user)
        discription=user_profile.discription
        # request.session['discriptionnew'] = discriptionnew
        # if not discriptionnew:
        #     discriptionnew=discription
        return render(request,'profile.html',{'discription':discription})
    form=DiscriptionChangeForm
    return render(request,'changediscription.html',{'form':form})

def delete_account_warn(request):
    return render(request,'deleteaccount.html')

def delete_account(request):
    user=request.user
    user.delete()
    auth.logout(request)
    return render(request,'confirmdelete.html')
    
def delete_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if post.user==request.user:
        post.delete()
    return redirect('index')

@login_required
def like_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        # Check if the user has already liked the post
        try:
            like = LikePost.objects.get(user=user, post=post)
            # User has already liked the post, so unlike it
            like.delete()
            liked = False
            post.likes_count -= 1
        except LikePost.DoesNotExist:
            # User has not liked the post, so like it
            LikePost.objects.create(user=user, post=post)
            liked = True
            post.likes_count += 1

        post.save()  # Save the post with the updated like count

        # Update the session variable for this post
        request.session[f'CountLike_{post_id}'] = post.likes_count

        return JsonResponse({'liked': liked, 'likes_count': post.likes_count})

def increase_comment(post_id):
    post=Post.objects.get(id=post_id)
    post.comment_count+=1
    post.save()

def decrease_comment(post_id):
    post=Post.objects.get(id=post_id)
    post.comment_count-=1
    post.save()

def comment_page(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    comments=Comment.objects.filter(post=post).order_by('-created_at')
    return render(request,'comment.html',{'post': post,'post_id':post_id,'comments':comments})

def add_comment(request,post_id):
    
    if request.method=="POST":
        text=request.POST.get('text')
        user_profile=UserProfile.objects.get(user=request.user)
        Comment.objects.create(post_id=post_id,author=user_profile,text=text)
        increase_comment(post_id)
    return redirect('comment',post_id=post_id)

def delete_comment(request,post_id,comment_id):
    comment=get_object_or_404(Comment,id=comment_id)
    if comment.author.user == request.user:
        comment.delete()
        decrease_comment(post_id)
    return redirect('comment',post_id)

def user_profile(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    target_user = user_profile.user
    current_user = request.user
    follow_status = Follow.objects.filter(follower=current_user,following=target_user).first()

    if follow_status:
        follow_status=follow_status.status
    else:
        follow_status='none'
    profilepic=user_profile.profilepic.url
    user=user_profile.user
    posts = Post.objects.filter(user=user)
    post_count=posts.count()
    follower_count = Follow.objects.filter(following=target_user,status='confirmed').count()
    following_count = Follow.objects.filter(follower=target_user,status='confirmed').count()


    verification_users = Follow.objects.filter(follower= request.user,following=target_user,status='confirmed')
    if verification_users:
        security=True
    else:
        security=False

    
    return render(request, 'user_profile.html', {'posts':posts,'security':security,'following_count':following_count,'follower_count':follower_count,'follow_status':follow_status,'user_profile': user_profile,'post_count':post_count,'profilepic':profilepic})

def user_search(request):
    if request.method == "POST":
        search_query = request.POST['search_query']
        if search_query:
            matched_users = UserProfile.objects.filter(user__username__icontains=search_query)
        return render(request,'search_results.html',{'users':matched_users,'search_query':search_query})
    return redirect('index')

def follow_user(request,username):
    target_user=User.objects.get(username=username)
    current_user = request.user
    follow,created=Follow.objects.get_or_create(
        follower=current_user,
        following=target_user
    )
    if created:
        follow.status='requested'
        follow.save()
    return redirect('user_profile',target_user)

def follow_request_view(request):
    follow_request= Follow.objects.filter(following=request.user,status='requested')
    return render(request,'notifications.html',{'follow_request':follow_request})

def confirm_follow_request(request,follow_id):
    follow=Follow.objects.get(id=follow_id)
    if follow.following== request.user:
        follow.status='confirmed'
        follow.save()
    # return HttpResponseRedirect(reverse('follow_requests'))
    return redirect('index')

def delete_request_view(request,follow_id):
    follow=Follow.objects.get(id=follow_id)
    if follow.following == request.user:
        follow.delete()
    return HttpResponseRedirect(reverse('follow_requests'))

def unfollow_user(request,username):
    target_username=User.objects.get(username=username)
    follow=Follow.objects.filter(follower=request.user,following=target_username)
    if follow.exists():
        follow.delete()
    return redirect('user_profile',username)

def inbox_view(request):
    return render(request,'inbox.html')