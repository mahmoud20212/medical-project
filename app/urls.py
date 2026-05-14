from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('resources/', views.resources, name='resources'),
  path('specialization/<slug:slug>/', views.specialization_detail, name='specialization_detail'),
  path('course/<int:pk>/detail/', views.course_detail, name='course_detail'),
]