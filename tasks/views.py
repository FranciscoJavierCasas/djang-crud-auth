from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UserChangeForm 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .form import TaskForm, CustomUserCreationForm, SetPasswordForm, PasswordChangeForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
# plantilla html home


def home(request):
    return render(request, 'home.html')

# plantilla html signup y confiuracion para crear un nuevo usuario
def signup(request):
    if request.method == 'GET':
        # print('enviando formulario')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # registrar usuario
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
                #return HttpResponse('Usuario creado')
            except IntegrityError:
                # return HttpResponse('El usuario ya existe')
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Contraseña diferentes'
        })

        # print(request.POST)
        # print('obteniendo datos')
#Plantilla de Tareas
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks} )
#Plantilla de Tareas completadas
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks} )    
# plantilla de creacion de tareas y configuracion
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
            #print(new_task)
            #print(request.POST)
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Por favor provee datos validos'
            })

#Plantilla de html de task detail y configuracion de la vista
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        #print(request.POST)
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task, 
                'form': form,
                'error': 'error actualizando'
                })


#vista que nos muestra las tareas completadas
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
#vista para poder eliminar las tareas que tengamos
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
#configuracion para cerrar sesion y regresasr a home
@login_required
def signout(request):
    logout(request)
    return redirect('home')
#plantilla html de signiup, para iniciar sesion
def signin(request):
    if request.method == 'GET':
            return render(request, 'signin.html', {
                'form': AuthenticationForm
            })
    else:
        #print(request.POST)
        user= authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "Usuario o Password es incorrecto"
            })
        else:
            login(request, user)
            return redirect('tasks')

#plantilla de configuracion de usuario login
@login_required
def settings(request, user_id):
    if request.method == 'GET':
        settings = get_object_or_404(User, pk=user_id)
        form = CustomUserCreationForm(instance=settings)
        return render(request, 'setting.html', {'settings': settings, 'form': form})
    else:
        #print(request.POST)
        try:
            settings = get_object_or_404(User, pk=user_id)
            form = CustomUserCreationForm(request.POST, instance=settings)
            form.save()
            #return redirect('home')
            return render(request, 'setting.html', {
                'settings': settings, 
                'form': form,
                'error': 'Usuario actualizado'
                })
        except ValueError:
            return render(request, 'setting.html', {
                'settings': settings, 
                'form': form,
                'error': 'error actualizando'
                })
# cambiar contraseña
@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # dont logout the user.
            #messages.success(request, "password actualizada.")
            return render(request,"password.html", {
                'error':"Contraseña actualizada"
            })
    else:
        form = PasswordChangeForm(request.user)
    data = {
        'form': form
        
    }
    return render(request, "password.html", data)
 

