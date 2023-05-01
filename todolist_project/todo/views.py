from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin # used to restrict user from going to task-list and other template without login (redirects to login page)
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task
from django.urls import reverse_lazy
from django.db import IntegrityError


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['tasks'] = context['tasks'].filter(user = self.request.user)
            context['count'] = context['tasks'].filter(complete=False).count()

            search_input = self.request.GET.get('search_text') or ''
            if search_input:
                context['tasks'] = context['tasks'].filter(title__icontains=search_input)
                context['search_input'] = search_input
            return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "tasks"
    template_name = 'todo/task.html'

class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']                  # all fields from models.py Task (for new form)
    success_url = reverse_lazy('task')  # once a new task is created , reload the page

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)



class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields =  ['title', 'description', 'complete']                    # all fields from models.py Task (for new form)
    success_url = reverse_lazy('task')  # once the task is updated, reload the page

class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "tasks"
    success_url = reverse_lazy('task')

class Login(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__" 
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('task')
    

class Register(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return super(Register, self).form_valid(form)
        else:
            # Check for weak password
            if len(form.errors.get('password1', [])) > 0:
                form.add_error('password1', 'Please choose a stronger password')
            
            # Check for existing user with the same credentials
            if len(form.errors.get('__all__', [])) > 0 and 'already exists' in form.errors['__all__'][0]:
                form.add_error('username', 'A user with that username already exists')
                
            return super(Register, self).form_invalid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(Register, self).get(*args, **kwargs)