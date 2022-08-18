from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('notes/',views.notes, name='notes'),
    path('delete-note/<int:pk>/',views.delete_note, name='delete'),
    path('notes-detail/<int:pk>/',views.NotesDetailView.as_view(), name='details'),
    path('homework/',views.homework, name='homework'),

    path('update-homework/<int:pk>/',views.update_homework, name='update-homework'),
    path('delete-homework/<int:pk>/',views.delete_homework, name='deleteh'),
    path('youtube/',views.youtube, name='youtube'),
    path('todo/',views.todo, name='todo'),
]
