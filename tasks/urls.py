from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<int:task_id>/", views.edit_task, name="edit"),
    path("delete/<int:task_id>/", views.delete_task, name="delete"),
    path("complete/<int:task_id>/", views.complete_task, name="complete"),
    path("uncomplete/<int:task_id>/", views.uncomplete_task, name="uncomplete"),
]
