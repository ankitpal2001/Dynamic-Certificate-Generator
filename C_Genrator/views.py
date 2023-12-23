from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Certificate
import hashlib
from django.shortcuts import render, get_object_or_404
from .models import Certificate
from django.http import JsonResponse

def home(request):

  return render(request,"Home.html")


def about(request):
  return render(request,"about.html")


def login_page(request):
  if request.method=="POST":
    Username = request.POST.get('username')
    Password=request.POST.get('password')
    if not User.objects.filter(username=Username).exists():
      messages.info(request,"Invalid username")
      return redirect("/login/")
    
    user=authenticate(username = Username,password = Password)

    if user is not None:
      print(user.is_active)
      if user.is_active:   
         login(request, user)
         return redirect("/generate-certificate/")
      else:
        
        messages.info(request,"The password is valid, but the account has been disabled!")
        return redirect("/login/")
        
    else:
     messages.info(request,"Invalid Passoword")
     return redirect("/login/")
     
     
         

        

  return render(request,"login.html")




def register_page(request):
  if request.method =="POST":
    first_name=request.POST.get("first_name")
    last_name=request.POST.get("last_name")
    Username=request.POST.get("username")
    Password=request.POST.get("password")
 

    user =User.objects.filter(username=Username)

    if user.exists():
      messages.info(request,"Username alredy taken")
      return redirect("/register/")

    user=User.objects.create(
      first_name=first_name,
      last_name=last_name,
      username=Username,
      
    )

    user.set_password(Password)
    user.save()
    messages.info(request,"Account created succesfully")
    return redirect("/register/")
  return render(request,"register.html")



def generate_certificate_view(request):
    if request.method == 'POST':
        recipient_name = request.POST.get('recipient_name')
        course_name = request.POST.get('course_name')
        completion_date = request.POST.get('completion_date')

        # Generate a unique ID based on certificate data
        certificate_data = f"{recipient_name}{course_name}{completion_date}"
        unique_id = hashlib.sha256(certificate_data.encode()).hexdigest()

        # Save the data in the database along with the unique ID
        certificate = Certificate.objects.create(
            recipient_name=recipient_name,
            course_name=course_name,
            completion_date=completion_date,
            unique_id=unique_id,
        )

        # Pass the data to the certificate_template.html page
        context = {
            'recipient_name': recipient_name,
            'course_name': course_name,
            'completion_date': completion_date,
            'unique_id': unique_id,
        }

        return render(request, 'certTemplate1.html', context)

    return render(request, 'generate_certificate.html')


# def verify_certificate(request, unique_id):
#     certificate = get_object_or_404(Certificate, unique_id=unique_id)
#     return render(request, 'verification_result.html', {'certificate': certificate})

def verify_certificate(request, unique_id):
    certificate = get_object_or_404(Certificate, unique_id=unique_id)
    if certificate:
        return JsonResponse({'message': f'Certificate with Unique ID "{unique_id}" is valid.'})
    else:
        return JsonResponse({'message': 'Certificate not found or invalid.'}, status=404)
