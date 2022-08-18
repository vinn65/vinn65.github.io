from multiprocessing import context
from django.shortcuts import redirect, render
from Dashboard.models import Homework, ToDo
from . form import DashboardForm, NotesForm, Notes, Homework, HomeworkForm, TodoForm
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch

# Create your views here.

def home(request):
    return render(request, 'Dashboard/home.html')

def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes added successfully!")
        return redirect("notes")
    else:    
        form = NotesForm()
        notes = Notes.objects.filter(user=request.user)
        context = {'notes':notes,'form':form}
        return render(request, 'Dashboard/notes.html', context)


def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes

  
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished'] 
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False     
            homework = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )       
            homework.save()
            messages.success(request,f'Homework Added Successfully!')    
            return redirect('home')
    else:    
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False    
    context = {
                'homework':homework, 
                'homework_done':homework_done,
                'form':form
                }
    return render(request, 'Dashboard/homework.html',context)

def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)

    if homework.is_finished == True:
          homework.is_finished = False
    
    else:
        homework.is_finished = True  
    homework.save()      
    return redirect('homework')

def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=20)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'viewcount':i['viewcount']['short'],
                'publishedTime':i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
                result_dict['description'] = desc
                result_list.append(result_dict)
                context = {
                    'form':form,
                    'results':result_list
                }
                return render(request, 'Dashboard/youtube.html',context)
    else:   
        form = DashboardForm()
        context= {
        'form':form
    }
    return render(request, 'Dashboard/youtube.html',context)

def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False    
            todos = ToDo(
               user = request.user,
               title= request.POST['title'],
               is_finished  = finished
            )
            todos.save()    
            messages.success(request,f'Todo added successfully!')
             
    form = TodoForm()
    todo = ToDo.objects.filter(user= request.user)
    if len(todo) == 0:
        todos_done = 'True'
    else:
        todos_done = 'False'    
    context = {
        'todos':todo,
        'form':form,
        'todos_done':todos_done
    }
    return render(request, "Dashboard/todo.html", context)     