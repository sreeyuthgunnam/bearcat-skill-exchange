from django.urls import path

from . import views

app_name = 'listings'

urlpatterns = [
    path('post/', views.submit_listing, name='submit'),
    path('post/submitted/', views.submission_received, name='submitted'),
]