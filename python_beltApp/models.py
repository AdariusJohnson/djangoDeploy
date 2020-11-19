from django.db import models
import re
from datetime import date

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        usersEmailMatch = User.objects.filter(email = postData['e'])
        print(f"USERS WITH MATCHING EMAIL: {usersEmailMatch}")

        errors = {}
        if len(postData['fname']) == 0:
            errors['fnamereq'] = "First Name is required!" 
        if len(postData['lname']) == 0:
            errors['lnamereq'] = "Last Name is required!"
        if len(postData['e']) == 0:
            errors['emailreq'] = "Email is required!"
        elif not EMAIL_REGEX.match(postData['e']):
            errors['emailpat'] = "Invalid Email"
        elif len(usersEmailMatch)>0:
            errors['emailtaken'] = "This email is already registered!"
        if len(postData['pw']) == 0:
            errors['pwreq'] = "Password is required!"
        elif len(postData['pw'])< 8:
            errors['pwlength'] = "Password must be a MIN of 8 characters!"
        if postData['pw'] != postData['cpw']:
            errors['pwmatch'] = "Passwords must match!"
        
        return errors 
    def loginValidator(self, postData):
        errors = {}
        usersEmailMatch = User.objects.filter(email = postData['e'])
        if len(usersEmailMatch) == 0:
            errors['emailNotfound'] ="This email is not registered. Please register above!"
        else:
            print(usersEmailMatch[0].password)
            if usersEmailMatch[0].password != postData['pw']:
                errors['incorrectPW'] = "Incorrect Password!"

        return errors

class TripManager(models.Manager):
    def createTripValidator(self, postData):
        errors = {}
        today = str(date.today())
        if len(postData['dname']) ==0:
            errors['tripReq'] = "Trip Destination is required!"
        if len(postData['tripPlan']) ==0:
            errors['descReq'] = "Trip Description is required!"
        if len(postData['sdate']) ==0:
            errors['sDateReq'] = "Trip start date is required!"
        elif postData['sdate'] < today:
            errors['noStart'] = "Start date must not be before Todays date!"
        if len(postData['edate']) ==0:
            errors['eDateReq'] = "Trip end date is required!"
        if postData['edate'] < postData['sdate']:
            errors['noEnd'] = "End date must not be before Start date!"
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length= 255)
    last_name = models.CharField(max_length= 255)
    email = models.CharField(max_length= 255)
    password = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    name = models.CharField(max_length= 255)
    creator = models.ForeignKey(User, related_name = 'trips_created', on_delete = models.CASCADE)
    travelers = models.ManyToManyField(User, related_name = 'trips_joined')
    start = models.DateField()
    end = models.DateField()
    plan = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
