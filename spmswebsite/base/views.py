from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, redirect
from .forms import  PostForm, RoomForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from .models import Message, Post, Result, Room, Student, Task, Topic, Lecturer
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.db.models import Q


# Create your views here.
def is_student(user):
    return user.groups.filter(name='student').exists()

def is_lecturer(user):
    return user.groups.filter(name='lecturer').exists()



@login_required(login_url="login")
def home(request):
    user = request.user
    group = str(user.groups.all())
    students = Student.objects.all()

    if request.method == "POST":
      data = request.POST.dict()
      username = data.get("username")
      consultation = data.get("consultation")
      progress = data.get("progress")
    #   user = User.objects.get(username=str(username))
      user = User.objects.filter(username__icontains=username)[0]
    #   print(username,"qqqqqqq")
      print(user.users, "hjkjkjnkj")

     
      student = Student.objects.get(user=user)
      Result.objects.create( student= student, consultation = consultation, progress = progress)
    
    

    
    return render(request, 'base/home.html',{"group":group, "students":students})


@login_required(login_url="/login")
def dashboard(request):
    posts = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")
        
        if post_id:
            
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("base.delete_post")):
              post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    return render(request, 'base/dashboard.html',{"posts":posts})


@login_required(login_url="/login")
@permission_required("base.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, 'base/create_post.html', {"form": form})
   

def student_signup(request):
    if request.method == 'POST':
            data = request.POST.dict()
            username = data.get("username")
            email = data.get("email")
            studentemail = data.get("studentemail") 
            password1 = data.get("password1")
            password2 = data.get("password2")

            user = User.objects.create(username = username, email = email, password = password1)
            student = Student.objects.create(user=user, studentemail=studentemail)
           
        # form = RegisterForm(request.POST)
        # if form.is_valid():
        #     user = form.save()
            login(request, user)
            student =  Group.objects.get_or_create(name='student')
            student[0].user_set.add(user)

            login(request, user)
            if is_student(request.user):
                return redirect('/home')
            
            else:
                return redirect('/dashboard')

            
            return redirect('/home')
            

    # else:
    #     form = RegisterForm()  
    return render(request, 'registration/sign_up_lecturer.html')  

def lecturer_signup(request):
    if request.method == 'POST':
            data = request.POST.dict()
            username = data.get("username")
            email = data.get("email")
            lectureremail = data.get("lectureremail") 
            password1 = data.get("password1")
            password2 = data.get("password2")

            user = User.objects.create(username = username, email = email, password = password1)
            lecturer = Lecturer.objects.create(user=user, staffemail=lectureremail)
           
        # form = RegisterForm(request.POST)
        # if form.is_valid():
        #     user = form.save()
            login(request, user)
            lecturer =  Group.objects.get_or_create(name='lecturer')
            lecturer[0].user_set.add(user)

            login(request, user)
            if is_lecturer(request.user):
                return redirect('/dashboard')
            
            else:
                return redirect('/home')

            
            return redirect('/home')
            

    # else:
    #     form = RegisterForm()  
    return render(request, 'registration/sign_up_lecturer.html')  



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

     #for count you have specifiy in get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.model.objects.filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area','')
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input)
        context['search_input'] = search_input
        return context   
        


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
    
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description','complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
        
        
class TaskUpdate(LoginRequiredMixin,UpdateView): 
    model = Task
    fields = ['title', 'description','complete']
    success_url = reverse_lazy('tasks')
    
class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task  
    context_object_name = 'task' 
    success_url = reverse_lazy('tasks')


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('chat')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
   
    return render(request, 'base/update-user.html')


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})




def notifications(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    
    return render(request, 'base/notifications.html', context)


def chat(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    
    return render(request, 'base/chat.html', context)

def Reports(request):
    return render(request, 'base/reports.html')
