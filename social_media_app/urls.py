from django.contrib import admin
from django.urls import path,include
from social_media_app.views import index_view

urlpatterns = [
   path('' , index_view)
]
