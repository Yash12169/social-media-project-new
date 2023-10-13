from django.contrib import admin
from django.urls import path,include
from social_media_app.views import home_view,delete_account_warn,delete_account,change_discription,settings_view,tab1_view,tab2_view,tab3_view,tab4_view,login_view,privacy_view,index_view,log_out_view,profile_view,create_view
from . import views
from django.urls import path,include
from .views import ImageListView,ImageUploadView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   path('' , home_view),
   path('index/' , views.index_view,name='index'),
   path('tab-1/', views.tab1_view,name='tab-1'),
   path('tab-2/' , views.tab2_view,name='tab-2'),
   path('tab-3/', views.tab3_view,name='tab-3'),
   path('tab-4/' , views.tab4_view,name='tab-4'),
   path('Log-in/' , views.login_view,name='Log-in'),
   path('Privacy/' , views.privacy_view,name='Privacy'),
   path('About/' , views.about_view,name='About'),
   path('Log-out/' , views.log_out_view,name='Log-out'),
   path('Profile/', views.profile_view,name='profile_view'),
   path('Create/', views.create_view,name='Create'),
   path('Settings/', views.settings_view,name='Settings'),
   path('Edit-profile/',views.edit_profile_view,name='Edit-profile'),
   path('upload-image/', ImageUploadView.as_view(),name='image_upload'),
   path('change-description/',views.change_discription,name='change-discription'),
   path('delete-warning/',views.delete_account_warn,name='delete-warning'),
   path('confirm-delete/',views.delete_account,name='confirm-delete'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)