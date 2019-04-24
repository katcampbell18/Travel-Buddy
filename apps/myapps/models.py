from django.db import models
from datetime import datetime, date
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def login_validator(self, request):
        errors = {}
        is_logged_in = False
        user = User.objects.filter(username=request.POST['username'])
        print(user)

        if len(user) < 1:
            errors['username'] = "There is no match for that username"
        else:
            if not bcrypt.checkpw(request.POST['password'].encode(), User.objects.get(username=request.POST['username']).password.encode()):
                errors['password'] = "The password is invald, please try again"

        if len(errors) < 1:
            user = User.objects.get(username=request.POST['username'])
            request.session['user_id'] = user.id
            is_logged_in = True
        info = [errors, is_logged_in]
        return info
            


    def reg_validator(self, request):

        errors = {}
        is_logged_in = False

        user = User.objects.filter(username=request.POST['username'])

        if len(user) > 0:
            errors['username'] = "An account with that username already exists"

        if len(request.POST['name']) < 3:
            errors['name'] = "Name must be at least 3 characters long"

        if len(request.POST['username']) < 2:
            errors['username'] = "Username must be at least 3 characters long"

        if len(request.POST['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"

        elif request.POST['password'] != request.POST['password_confirmation']:
            errors['password'] = "Passwords do not match"

        if len(errors) < 1:
            hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=request.POST['name'],username=request.POST['username'],password=hashedpw.decode())
            request.session['user_id'] = user.id
            is_logged_in = True

        info = [errors, is_logged_in]
        return info

class TripManager(models.Manager):
    def trip_validator(self, request):
        errors = {}
        user = User.objects.get(id=request.session['user_id'])
        now = datetime.now()

        if len(request.POST['dest']) < 1:
            errors['dest'] = "Destination cannot be blank"

        if len(request.POST['desc']) < 1:
            errors['desc'] = "Description cannot be blank"

        if len(request.POST['start']) < 10 or len(request.POST['end']) < 10:
            errors['date'] = "Dates cannot be empty"
        else:
            start = datetime.strptime(request.POST['start'], "%Y-%m-%d")
            end = datetime.strptime(request.POST['end'], "%Y-%m-%d")
            if start < now:
                errors['date'] = "Start date must be in the future"
            else:
                if end < start:
                    errors['date'] = "End date must be after Start date"
        
        if len(errors) < 1:
            trip = Trip.objects.create(dest=request.POST['dest'], desc=request.POST['desc'], trav_from=request.POST['start'], trav_to=request.POST['end'], planner=user)
            user.joins.add(trip)
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password =  models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    dest = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    trav_from = models.DateField()
    trav_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    planner = models.ForeignKey(User, related_name="trips", on_delete=models.CASCADE)
    join = models.ManyToManyField(User, related_name="joins")
    objects = TripManager()

