from django.urls import path, include
from . import views
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate, DeleteView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('dashboard', views.dashboard, name="dashboard"),
    # path('sign-up', views.sign_up, name="sign_up"),

    path('student_signup/', views.student_signup, name="student_signup"),
    path('lecturer_signup/', views.lecturer_signup, name="lecturer_signup"),


    path('room/<str:pk>/', views.room, name="room"),

    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('notifications/', views.notifications, name="notifications"),

    path('reports/', views.Reports, name="notifications"),


    


    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    
    
    
    path('chat', views.chat, name='chat'),
    path('create-post', views.create_post, name='create_post'),
    path('task-list/', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', DeleteView.as_view(), name='task-delete'),
    
]
