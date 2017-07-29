from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def currentUser(self, request):
        id = request.session['user_id']

        return User.objects.get(id=id)
    #so now i need to make this validateRegistration work: and need to pass in that form_data argument
    def validateRegistration(self, form_data):
    #now i need to check for required
        errors = []

        if len(form_data['name']) == 0:
            errors.append("Name is required.")
        if len(form_data['alias']) == 0:
            errors.append("Alias is required.")
        if len(form_data['email']) == 0:
            errors.append("Email is required.")
        if len(form_data['password']) < 8:
            errors.append("Please enter a password that is 8 or more characters.")
        if form_data['password'] != form_data['password_confirmation']:
            errors.append("Passwords do not match.")
        
        return errors
    #now go to views and insert "if not errors:" for verification

    def validateLogin(self, form_data):
        errors = []
#also check to see if user exists in DB. see views

        if len(form_data['email']) == 0:
            errors.append("Email is required.")
        if len(form_data['password']) == 0:
            errors.append("Password is required.")

        return errors

    #insert 'createUser' method here
    def createUser(self, form_data):
    #bcrypt step 1: is to convert user password to a str
    #password is the str form of password
        password = str(form_data['password'])
    #step 2: we need to hash that password copy and past this line: "hashed = bcrypt.hashpw(password, bcrypt.gensalt())"
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        #here is going to be all the keys and their values
        user = User.objects.create(
            name = form_data['name'],
            alias = form_data['alias'],
            email = form_data['email'],
            #so instead of saving the password to our form = "form_data['password']" we are going to save the hashed_pw
            password = hashed_pw,
            #now we are going to store this in session in views
        )

        return user
        #now we are goin to do bcrypt from here (also ref platform)
        #bcryt has installed successfully, now just import at top of this page.

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    friends = models.ManyToManyField("self", related_name="friend_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

#   ******POTENTIALLY ON BELT EXAM: many to many******
#friend to friend relationship; a self joining table to "self".
#So I am going to say a User can have friends (inserted into User model)
#Related Names:   user.friends - would mean 'all of the people I have friended.'
#a user has friends and a user is friended by people = "friend_by"
#ManyToManyField only works once, so it is good so you can have a repeat of the same action or cause.

#after creating relationship modify your success page.So on my views.py on success i am going to get all uses. (removed the line under )