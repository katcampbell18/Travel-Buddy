from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    return render(request, 'myapps/index.html')

#validation for registration
def register(request):
    info = User.objects.reg_validator(request)

    if info[1]:
        return redirect('/travels')
    else:
        for key, value in info[0].items():
            messages.error(request, value)
        return redirect('/')

#validation for login
def login(request):
    info = User.objects.login_validator(request)
    if info[1]:
        return redirect('/travels')
    else:
        for key, value in info[0].items():
            messages.error(request, value)
        return redirect('/')

#show trips user created and trips to be joined, planned by other users 
def travels(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        trips = Trip.objects.all()
        mytrips = user.trips.all()
        
        joined = user.joins.all()
        notJoined = trips.difference(joined)

        joinedstillnotUser = joined.exclude(planner=user)

        context = {
            'user': user,
            'mytrips': mytrips,
            'joined' : joined,
            'notJoined' : notJoined,
            'joinedstillnotUser' : joinedstillnotUser,

        }
        return render(request, 'myapps/trips.html', context)

#add a trip
def add(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user
        }
        return render(request, 'myapps/create.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

#adds joined trip to user schedule
def join(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    user.joins.add(trip)
    return redirect('/travels')

#allow user to join trip
def gowith(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    user.join.remove(trip)
    return redirect('/travels')
    
#display trip information
def show(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    joined = trip.join.all()
    context = {
        'trip': trip,
        'joined': joined
    }
    return render(request, 'myapps/display.html', context)

#validation for adding trip
def create(request):
    errors = Trip.objects.trip_validator(request)

    if len(errors) < 1:
        return redirect('/travels')
    else:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add')

 

