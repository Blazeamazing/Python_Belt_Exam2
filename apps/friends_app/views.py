from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def flashErrors(request, errors):
    for error in errors:
    
        messages.error(request, error)

def index(request):

        return render(request, 'friends_app/index.html')
    
def success(request):
    if 'user_id' in request.session:
        #i want to get all the users but myself
        current_user = User.objects.currentUser(request)
        friends = current_user.friends.all()
        #exclude(id__in - means user objects not id in...
        users = User.objects.exclude(id__in=friends).exclude(id=current_user.id)
        context = {
            'current_user': current_user,
            'users': users,
            'friends': friends,
        }
        return render(request, 'friends_app/success.html', context)
   
    return redirect('landing')

def register(request):
    if request.method == "POST":
        errors = User.objects.validateRegistration(request.POST)

        if not errors:
            user = User.objects.createUser(request.POST)
            request.session['user_id'] = user.id

            return redirect('success')
        flashErrors(request, errors)

    return redirect('landing')
    

def login(request):

    if request.method == "POST":
        errors = User.objects.validateLogin(request.POST)
        if not errors:
            user = User.objects.filter(email = request.POST['email']).first()

            if user:
                password = str(request.POST['password'])
                user_password = str(user.password)

                hashed_pw = bcrypt.hashpw(password, user_password)
                
                if hashed_pw == user.password:
                   
                    request.session['user_id'] = user.id

                    return redirect('success')
               
            errors.append("Invalid account information.")

        flashErrors(request, errors)

    return redirect('landing')            

def logout(request):
    if 'user_id' in request.session:
       
        request.session.pop('user_id')

    return redirect('landing')

def profile(request):
    if 'user_id' not in request.session:
        return redirect('success')

        user = User.objects.currentUser(request)
        friends = user.friends.all()
        other_users = User.objects.exclude(id__in = friends)

        context = {
            'current_user': user,
            'friends': friends,
        }
      
    return render(request, 'friends_app/profile.html')

def addFriend(request, id):
    if request.method == "POST":
        
        if 'user_id' in request.session:
            current_user = User.objects.currentUser(request)
            friend = User.objects.get(id=id)
            current_user.friends.add(friend)

            return redirect('success')

    return redirect('landing')

def removeFriend(request, id):
    if request.method == "POST":

        if 'user_id' in request.session:
            current_user = User.objects.currentUser(request)
            friend = User.objects.get(id=id)
            current_user.friends.remove(friend)

            return redirect('success')

    return redirect('landing')