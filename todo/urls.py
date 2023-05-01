from django.urls import path
from .views import TaskList, TaskDetail, CreateTask, UpdateTask, DeleteTask, Login, Register
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TaskList.as_view(), name="task"),
    path('task-create/', CreateTask.as_view(), name="task-create"),     #new path for CreateTask view
    path('login/', Login.as_view(), name="login" ),                     #new path for Login
    path('logout/', LogoutView.as_view(next_page = "login"), name="logout" ),                  
    path('register/', Register.as_view(), name="register" ),                  
    path('task/<int:pk>/', TaskDetail.as_view(), name="task-detail" ),
    path('task-update/<int:pk>/', UpdateTask.as_view(), name="task-update" ),
    path('task-delete/<int:pk>/', DeleteTask.as_view(), name="task-delete" ),
]