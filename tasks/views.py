from django.shortcuts import render, redirect
from django.views.generic import View,ListView,DetailView,CreateView, TemplateView , FormView
from tasks.forms import TaskForm, RegistrationForm, LoginForm
from tasks.models import Tasks

from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator

# Create your views here.


def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "you must login first")
            return redirect("signin")
        else:
            return fn(request, *args, **kwargs)
    return wrapper


@signin_required
def sign_out(request, *args, **kwargs):
    logout(request)
    return redirect("signin")


class SignUpView(CreateView):
    template_name = "register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("signin")

    def form_valid(self, form) :
        messages.success(self.request, "Your account has been created")
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm


    def post(self, request, *args, **kwargs) :
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            usr = authenticate(request, username=uname, password= pwd)
            if usr:
                login(request,usr)
                messages.success(request, 'Successfully logined')
                return redirect("home")

            else:
                return render(request, "login.html", {"form":form})
        


@method_decorator(signin_required, name="dispatch")
class IndexView(TemplateView):
    template_name = "index.html"

@method_decorator(signin_required, name="dispatch")
class TaskCreateView(CreateView):
    template_name = "task-add.html"
    form_class = TaskForm
    success_url = reverse_lazy("task-list")


    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Task has been added')
        return super().form_valid(form)



# class TaskCreateView(View):
#     def get(self, request, *args, **kwargs):
#         form = TaskForm()
#         return render(request, "task-add.html", {"form":form})

#     def post(self, request, *args, **kwargs):
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("task-create")
#         else:
#             return render(request, "task-add.html", {"form":form})

@method_decorator(signin_required, name="dispatch")
class TaskListView(ListView):
    model= Tasks
    template_name = "task-list.html"
    context_object_name = "todos"

    def get_queryset(self):
        return Tasks.objects.filter(user = self.request.user)


# class TaskListView(View):
#     def get(self, request, *args, **kwargs):
#         qs = Tasks.objects.all()
#         return render(request, "task-list.html", {"todos":qs})


@method_decorator(signin_required, name="dispatch")
class TaskDetailView(DetailView):
    model = Tasks
    template_name = "task-detail.html"
    context_object_name = "todo"

# class TaskDetailView(View):
#     def get(self, request, *args, **kwargs):
#         id = kwargs.get("pk")
#         qs = Tasks.objects.get(id=id)
#         return render(request, "task-detail.html", {"todo":qs})


@method_decorator(signin_required, name="dispatch")
class TaskDeleteView(View):
     def get(self, request, *args, **kwargs):
         id = kwargs.get("pk")
         Tasks.objects.get(id=id).delete()
         messages.success(request, "Task Removed")
         return redirect("task-list")

            
           

            



        
   


     










        



  
 
