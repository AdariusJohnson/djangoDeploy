from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Trip

# Create your views here.
def index(request):
    return render(request, "login.html")

def register(request):
    print(request.POST)
    errorsFromValidator = User.objects.registrationValidator(request.POST)
    print(errorsFromValidator)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/")
    else:
        newUser = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['e'], password = request.POST['pw'])

        request.session['loggedInId']= newUser.id
    return redirect('/travels')

def success(request):
    if 'loggedInId' not in request.session:
            messages.error(request, 'You must be logged in first.')
            return redirect("/")
    context ={
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
        'allTrips': Trip.objects.all(),
        'favTrips': Trip.objects.filter(travelers=User.objects.get(id=request.session['loggedInId'])),
        'nonFavTrips': Trip.objects.exclude(travelers=User.objects.get(id=request.session['loggedInId']))
    }
    return render(request, 'travels.html', context)

def login(request):
    errorsFromValidator = User.objects.loginValidator(request.POST)
    print(errorsFromValidator)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/")
    else:
        usersEmailMatch = User.objects.filter(email = request.POST['e'])
        usersEmailMatch[0].id
        request.session['loggedInId']= usersEmailMatch[0].id
    return redirect("/travels")


def logout(request):
    request.session.clear()
    return redirect('/')

def addTrip(request):
    return render(request, "addtrip.html")

def uploadTrip(request):
    print(request.POST)
    errorsFromValidator = Trip.objects.createTripValidator(request.POST)
    print(errorsFromValidator)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/addtrip")
    else:
        Trip.objects.create(name = request.POST['dname'], creator = User.objects.get(id=request.session['loggedInId']), start = request.POST['sdate'], end = request.POST['edate'], plan = request.POST['tripPlan'])
    return redirect("/travels")

def tripInfo(request, tripId):
    context = {
        'oneTrip': Trip.objects.get(id= tripId),
        'userTrip': User.objects.get(id= tripId)
    }
    return render(request, "tripviews.html", context)

def joinTrip(request, tripId):
    Trip.objects.get(id=tripId).travelers.add(User.objects.get(id=request.session['loggedInId']))
    return redirect("/travels")

def removeTrip(request, tripId):
    Trip.objects.get(id=tripId).travelers.remove(User.objects.get(id=request.session['loggedInId']))
    return redirect("/travels")

def deleteTrip(request, tripId):
    trip2Delete= Trip.objects.get(id=tripId)
    trip2Delete.delete()
    return redirect('/travels')