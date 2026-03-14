from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Task
from .forms import TaskForm


# Create your views here.

def index(request):
    """Display pending and completed tasks and handle creation."""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks:index")
    else:
        form = TaskForm()

    pending_tasks = Task.objects.filter(is_completed=False)
    completed_tasks = Task.objects.filter(is_completed=True)

    return render(request, "tasks/index.html", {
        "form": form,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
    })


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks:index")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/edit.html", {"form": form, "task": task})


def delete_task(request, task_id):
    """Securely delete a task."""
    if request.method in ["POST", "GET"]:
        task = get_object_or_404(Task, pk=task_id)
        task.delete()
    return redirect("tasks:index")


def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if not task.is_completed:
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
    return redirect("tasks:index")


def uncomplete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.is_completed:
        task.is_completed = False
        task.completed_at = None
        task.save()
    return redirect("tasks:index")
