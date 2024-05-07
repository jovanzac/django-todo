from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

from .models import Task
from .lamma_model import LammaLLM


# Create your views here.
class TaskList(LoginRequiredMixin, ListView) :
    model = Task
    context_object_name = "tasks"
    
    def get_context_data(self, **kwargs) :
        print("In get")
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()
        
        # Search bar part
        search_input = self.request.GET.get("search") or ""
        if search_input :
            context["tasks"] = context["tasks"].filter(
                title__icontains=search_input
                )
        # LLM part
        task_id = self.request.GET.get("llm_submit") or ""
        llm_response = ""
        if task_id :
            print(f"task_id is: {task_id}")
            prompt = context["tasks"].filter(
                id = task_id
            )[0]
            print(prompt)
            llm_response = llm.prompt_the_llm(prompt)
        context["llm_response"] = llm_response
        print(context['llm_response'])
        context["search_input"] = search_input
        
        return context
    

class TaskDetail(LoginRequiredMixin, DetailView) :
    model = Task
    context_object_name = "task"
    
    
class TaskCreate(LoginRequiredMixin, CreateView) :
    model = Task
    fields = ["title", "description", "complete_by", "complete"]
    success_url = reverse_lazy("tasks")
    # template_name_field = None
    
    def form_valid(self, form) :
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    

class TaskUpdate(LoginRequiredMixin, UpdateView) :
    model = Task
    fields = ["title", "description", "complete_by", "complete"]
    success_url = reverse_lazy("tasks")
    

class TaskDelete(LoginRequiredMixin, DeleteView) :
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")
    

class AppLogin(LoginView) :
    template_name = "main/login.html"
    fields = "__all__"
    redirect_authenticated_user = True
    
    def get_success_url(self) :
        return reverse_lazy("tasks")
    

class AppRegister(FormView) :
    template_name = "main/signup.html"
    form_class = UserCreationForm
    # redirect_authenticated_user = True
    success_url = reverse_lazy("login")
    
    def form_valid(self, form) :
        form.save()
        return super(AppRegister, self).form_valid(form)
    
    def get(self, *args, **kwargs) :
        if self.request.user.is_authenticated :
            return redirect("tasks")
        return super(AppRegister, self).get(*args, **kwargs)
    

class LlmView(DetailView) :
    model = Task
    template_name = "main/llm_pg.html"
    context_object_name = "task"
    
    def get_context_data(self, **kwargs) :
        print("Get request received")
        context = super().get_context_data(**kwargs)
        # print(f"context['task']: {context['task']}")
        task_id = self.request.GET.get("llm_submit") or ""
        llm_response = ""
        if task_id :
            print(f"task_id is: {task_id}")
            prompt = context["tasks"].filter(
                id = task_id
            )
            print(prompt)
            # llm_response = llm.prompt_the_llm()
        context["llm_response"] = llm_response
        
        return context

llm = LammaLLM()