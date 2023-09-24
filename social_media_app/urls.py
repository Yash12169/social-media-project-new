from django.contrib import admin
from django.urls import path,include
from social_media_app.views import index_view,tab1_view,tab2_view,tab3_view,tab4_view,login_view,privacy_view
from . import views
urlpatterns = [
   path('' , index_view),
   path('tab-1/', views.tab1_view,name='tab-1'),
   path('tab-2/' , views.tab2_view,name='tab-2'),
   path('tab-3/', views.tab3_view,name='tab-3'),
   path('tab-4/' , views.tab4_view,name='tab-4'),
   path('Log-in/' , views.login_view,name='Log-in'),
   path('Privacy/' , views.privacy_view,name='Privacy'),
   path('About/' , views.about_view,name='About'),
   
  
]
