from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.db.models import Q
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')

def home(request):
    query = request.GET.get('q')
    status = request.GET.get('status')
    action = request.GET.get('action')
    tasks = Task.objects.all()
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if status:
        tasks = tasks.filter(status=status)
    if action == 'generate_chart':
        completed_tasks_count = tasks.filter(status='Done').count()
        incomplete_tasks_count = tasks.filter(status='To Do').count()
        total_tasks_count = completed_tasks_count + incomplete_tasks_count

        completed_tasks_percentage = (completed_tasks_count / total_tasks_count) * 100
        incomplete_tasks_percentage = (incomplete_tasks_count / total_tasks_count) * 100

        labels = [f'Виконані {completed_tasks_percentage:.2f}%', f'Невиконані {incomplete_tasks_percentage:.2f}%']
        counts = [completed_tasks_count, incomplete_tasks_count]
        colors = ['blue', 'red']

        plt.clf()
        plt.bar(labels, counts, color=colors)
        plt.xlabel('Статус')
        plt.ylabel('Кількість доручень')
        plt.title(f'Загальна кількість доручень {total_tasks_count}')
        plt.savefig('task_manager/static/chart.png')
        chart_generated = True
    else:
        chart_generated = False

    return render(request, 'home.html', {'tasks': tasks, 'query': query, 'chart_generated': chart_generated, 'status': status})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    return render(request, 'delete_task.html', {'task': task})

def change_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.status == 'To Do':
        task.status = 'Done'
    else:
        task.status = 'To Do'
    task.save()
    return redirect('home')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'edit_task.html', {'form': form})