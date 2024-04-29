from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.db.models import Q
from django.utils import timezone
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')

def home(request):
    query = request.GET.get('q')
    status = request.GET.get('status')
    action = request.GET.get('action')
    sort_by = request.GET.get('sort_by')

    tasks = Task.objects.all()
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if status:
        tasks = tasks.filter(status=status)
    if sort_by:
        tasks = tasks.order_by(sort_by)
    if action == 'generate_chart1':
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
        plt.savefig('task_manager/static/chart1.png')
        chart_generated1 = True
        chart_generated2 = False

    elif action == 'generate_chart2':
        executor_tasks_count = {}
        for task in tasks:
            executor = task.executor
            if executor not in executor_tasks_count:
                executor_tasks_count[executor] = {'completed': 0, 'incomplete': 0}
            if task.status == 'Done':
                executor_tasks_count[executor]['completed'] += 1
            else:
                executor_tasks_count[executor]['incomplete'] += 1

        # Створіть списки для міток, кількостей та кольорів
        executor_labels = []
        executor_counts_completed = []
        executor_counts_incomplete = []

        # Заповніть списки даними для графіка
        for executor, counts in executor_tasks_count.items():
            executor_labels.append(executor)
            executor_counts_completed.append(counts['completed'])
            executor_counts_incomplete.append(counts['incomplete'])

        # Створіть графік
        plt.clf()
        plt.bar(executor_labels, executor_counts_completed, color='blue', label='Виконані')
        plt.bar(executor_labels, executor_counts_incomplete, color='red', bottom=executor_counts_completed,
                label='Невиконані')
        plt.xlabel('Виконавець')
        plt.ylabel('Кількість доручень')
        plt.title('Кількість доручень за виконавцями')
        plt.legend()
        plt.xticks(rotation=45)  # Обертання міток осі X для кращої читабельності
        plt.tight_layout()  # Розрахована на компактність графіка
        plt.savefig('task_manager/static/chart2.png')
        chart_generated1 = False
        chart_generated2 = True
    else:
        chart_generated1 = False
        chart_generated2 = False

    return render(request, 'home.html', {'tasks': tasks, 'query': query, 'chart_generated1': chart_generated1,
                                         'chart_generated2': chart_generated2, 'status': status, 'sort_by': sort_by})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if task.final_date <= timezone.now():
                form.add_error('final_date', 'Дата закінчення має бути після дати початку')
                return render(request, 'add_task.html', {'form': form})
            else:
                task.save()
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
            task = form.save(commit=False)
            if task.final_date <= task.created_date:
                form.add_error('final_date', 'Дата закінчення має бути після дати початку')
                return render(request, 'edit_task.html', {'form': form})
            else:
                task.save()
                return redirect('home')
    return render(request, 'edit_task.html', {'form': form})