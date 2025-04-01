from django.urls import path
from . import views

urlpatterns = [
    path('note/',views.CreateNote.as_view(), name='Creat-note'),
    path('note/delete/<int:pk>/', views.DeleteNote.as_view(), name='Delete-note'),
]