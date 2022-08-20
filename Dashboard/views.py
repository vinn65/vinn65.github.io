from enum import auto
import imp
from multiprocessing import context
from django.shortcuts import redirect, render
from Dashboard.models import Homework, ToDo
from . form import ConversionForm, ConversionLengthForm,ConversionMassForm, DashboardForm, NotesForm, Notes, Homework, HomeworkForm, TodoForm, UserRegistrationForm
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests, wikipedia
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'Dashboard/home.html')
@login_required
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

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes

@login_required
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
@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)

    if homework.is_finished == True:
          homework.is_finished = False
    
    else:
        homework.is_finished = True  
    homework.save()      
    return redirect('homework')
@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
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
@login_required
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
@login_required
def update_todo(request, pk=None):
    todo = ToDo.objects.get(id=pk)

    if todo.is_finished == True:
          todo.is_finished = False
    
    else:
        todo.is_finished = True  
    todo.save()      
    return redirect('todo')    
@login_required    
def delete_todo(request, pk=None):
    ToDo.objects.get(id=pk).delete()
    return redirect('delete_todo')

def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        ans = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                    'title':ans['items'][i]['volumeInfo']['title'],
                    'subtitle':ans['items'][i]['volumeInfo'].get('subtitle'),            
                    'description':ans['items'][i]['volumeInfo'].get('description'),
                    'count':ans['items'][i]['volumeInfo'].get('pageCount'),
                    'categories':ans['items'][i]['volumeInfo'].get('categories'),
                    'rating':ans['items'][i]['volumeInfo'].get('pageRating'),
                    'thumbnail':ans['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                    'preview':ans['items'][i]['volumeInfo'].get('previewLinks')             
                    
                    }
            result_list.append(result_dict)
            context = {
                    'form':form,
                    'results':result_list
                }
            return render(request, 'Dashboard/books.html',context)
    else:   
        form = DashboardForm()
    return render(request, "Dashboard/books.html",{'form':form})



def dictionary(request):
     if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        ans = r.json()
        try:
            phonetics = ans[0]['phonetics'][0]['text']
            audio = ans[0]['phonetics'][0]['audio']
            definition = ans[0]['meanings'][0]['definitions'][0]['definition']
            example = ans[0]['meanings'][0]['definitions'][0]['example']
            synonyms = ans[0]['meanings'][0]['definitions'][0]['synonyms']
            context={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context={
                'form':form,
                'input':'',
            }
        return render(request, "Dashboard/dictionary.html",context)
    
     else:
        form = DashboardForm() 
        context = {'form':form}
        return render(request, "Dashboard/dictionary.html",context)

def wiki(request):
    if request.method == 'POST':
        text = request.POST('text')
        form = DashboardForm(request.POST) 
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,"Dashboard/wiki.html",context)

    else:
        form = DashboardForm() 
        context = {'form':form}
        return render(request,"Dashboard/wiki.html",context)


def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input1':True
            }
            if 'input1' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input1 = request.POST['input1']
                answer = ''
                if input1 and int(input1) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input1} pound = {int(input1)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input1} kilogram = {int(input1)/0.453592} pound'
                    context = {
                        'form':form,
                        'm_form':measurement_form,
                        'input1':True,
                        'answer':answer
                    }
        if request.POST['measurement'] == 'Length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input1':True
            }
            if 'input1' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input1 = request.POST['input1']
                answer = ''
                if input1 and int(input1) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input1} yard = {int(input1)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input1} foot = {int(input1)/3} yard'
                    context = {
                        'form':form,
                        'm_form':measurement_form,
                        'input1':True,
                        'answer':answer
                    }            
    else:  
        form = ConversionForm()
        context =  {
            'form':form,
            'input1':False
        }                   
    return render(request,"Dashboard/conversion.html",context)

                      
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f" Hey {username}! Your Account has been Created!!")
            return redirect('login')
    else:           
        form = UserRegistrationForm()
    context = {
            "form":form
        }
    return render(request,'Dashboard/register.html',context)
@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = ToDo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
       homework_done = False     

    if len(todos) == 0:
       todos_done = True
    else:
       todos_done = False    
    context ={
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done
    }
    return render(request,'Dashboard/profile.html',context)