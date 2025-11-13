from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login
from django.contrib import messages
from .models import Student, Course, Teacher
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required(login_url='login_page')
def admin(request):
    return render(request, 'admin.html')

@login_required(login_url='login_page')
def course(request):
    return render(request, 'course.html')

def add_course(request):
    if request.method=='POST':
        course_name=request.POST['course']
        fees=request.POST['fee']

        if Course.objects.filter(coursename= course_name).exists():
            messages.error(request, f"The course '{course_name}' already exists!")
            return redirect('course')
    
        crs=Course(coursename=course_name, fees=fees)
        crs.save()
        messages.success(request, "Course added successfully!")
        return redirect('course')
    return render(request, 'course.html')

@login_required(login_url='login_page')
def student(request):
    crs=Course.objects.all()
    return render(request, 'student.html', {'course': crs})

def add_student(request):
    if request.method=='POST':
        name=request.POST['name']
        adrs=request.POST['address']
        age=request.POST['age']
        date=request.POST['date']
        course=request.POST.get('c')

        if not course:
            messages.error(request, "Please select a course!")
            return redirect('student')

        crs=Course.objects.get(id=course)
        std=Student(studentname=name, address=adrs, age=age, joiningdate=date, course=crs)
        std.save()
        messages.success(request, "Student added successfully!")
        return redirect('student')
    return redirect('student')

@login_required(login_url='login_page')    
def show(request):
    std=Student.objects.all()
    return render(request, 'show.html', {'student': std})

@login_required(login_url='login_page')
def show_teachers(request):
    tchr=Teacher.objects.all()
    return render(request, 'show_teachers.html', {'teacher': tchr})

@login_required(login_url='login_page')
def edit(request, id):
    std= Student.objects.get(id=id)
    crs= Course.objects.all()
    return render(request, 'edit.html', {'student': std, 'course': crs})

def edit_details(request, id):
    if request.method == "POST":
        std = Student.objects.get(id=id)

        course_id = request.POST.get("c")
        selected_course = Course.objects.get(id=course_id)

        std.studentname = request.POST.get("name")
        std.address = request.POST.get("address")
        std.age = request.POST.get("age")
        std.joiningdate = request.POST.get("date")
        std.course = selected_course

        std.save()
        messages.success(request, "Student Details updated successfully!")
        return redirect('show')

def delete(request, id):
    std= Student.objects.get(id=id)
    std.delete()
    messages.success(request, "Student record deleted successfully!")
    return redirect('show')

def delete_teacher(request, id):
    tchr = Teacher.objects.get(id=id)
    user = tchr.user
    tchr.delete()   
    user.delete() 
    messages.success(request, "Teacher record deleted successfully!")
    return redirect('show_teachers')


def signup_teacher(request):
    crs=Course.objects.all()
    return render(request, 'signup_teacher.html', {'course': crs})


def signup_fun(request):
    if request.method == 'POST': 
        first_name = request.POST['fname'].strip()
        last_name = request.POST['lname'].strip()
        username = request.POST['uname'].strip()
        address = request.POST['adrs'].strip()
        age = request.POST['age'].strip()
        email = request.POST['mail'].strip()
        phone = request.POST['phone'].strip()
        password = request.POST['pass']
        cpassword = request.POST['cpass']
        image = request.FILES.get('image')
        course_id = request.POST.get('c')


        if not course_id:
            messages.error(request, "Please select a course!")
            return redirect('signup_teacher')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address!")
            return redirect('signup_teacher')

        if password != cpassword:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup_teacher')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username already exists!')
            return redirect('signup_teacher')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered!')
            return redirect('signup_teacher')

        if Teacher.objects.filter(phone=phone).exists():
            messages.error(request, 'This phone number is already registered!')
            return redirect('signup_teacher')

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            messages.error(request, "Invalid course selected!")
            return redirect('signup_teacher')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password, email=email)


        Teacher.objects.create(user=user, course=course, address=address, age=age, phone=phone, image=image)

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login_page')  

 
    courses = Course.objects.all()
    return render(request, 'signup_teacher.html', {'courses': courses})


def login_page(request):
    return render(request, 'login_page.html')

def login_fun(request):
    if request.method == 'POST':
        usr = request.POST['usname']
        pas = request.POST['passd']
        user = auth.authenticate(username=usr, password=pas)

        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, "You have successfully logged in as Admin.")
                return redirect('admin')

            else:
                login(request, user)
                try:
                    teacher = Teacher.objects.get(user=user)
                    messages.success(request, "You have successfully logged in.")
                    return redirect('teacher', id=teacher.id)
                except Teacher.DoesNotExist:
                    messages.error(request, "Teacher profile not found.")
                    return redirect('login_page')
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('login_page')
        

def logout_fun(request):
    auth.logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login_page')

@login_required(login_url='login_page')
def teacher(request, id):
    tchr = Teacher.objects.get(id=id)
    user = tchr.user
    return render(request, 'teacher.html', {'teacher': tchr, 'user': user})

@login_required(login_url='login_page')
def edit_tchr(request, id):
    tchr= Teacher.objects.get(id=id)
    crs= Course.objects.all()
    return render(request, 'edit_tchr.html', {'teacher': tchr, 'courses': crs})


def edit_teacher(request, id):
    tchr = Teacher.objects.get(id=id)
    crs = Course.objects.all()

    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        address = request.POST['adrs']
        age = request.POST['age']
        email = request.POST['mail']
        phone = request.POST['phone']
        password = request.POST.get('pass')
        confirm_password = request.POST.get('cpass')
        course_id = request.POST.get("c")

        if not course_id:
            messages.error(request, "Please select a course!")
            return redirect('edit_tchr', id=id)

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address!")
            return redirect('edit_tchr', id=id)

        if password and password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('edit_tchr', id=id)

        if User.objects.filter(username=username).exclude(id=tchr.user.id).exists():
            messages.error(request, "This username is already taken!")
            return render(request, 'edit_tchr.html', {'teacher': tchr, 'courses': crs})

        if User.objects.filter(email=email).exclude(id=tchr.user.id).exists():
            messages.error(request, "This email is already registered!")
            return render(request, 'edit_tchr.html', {'teacher': tchr, 'courses': crs})

        if Teacher.objects.filter(phone=phone).exclude(id=tchr.id).exists():
            messages.error(request, "This phone number is already registered!")
            return render(request, 'edit_tchr.html', {'teacher': tchr, 'courses': crs})

        selected_course = Course.objects.get(id=course_id)
        user = tchr.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password:
            user.set_password(password)
        user.save()

        tchr.address = address
        tchr.age = age
        tchr.phone = phone
        tchr.course = selected_course
        if 'image' in request.FILES:
            tchr.image = request.FILES['image']
        tchr.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('teacher', id=tchr.id)

    return render(request, 'edit_tchr.html', {'teacher': tchr, 'courses': crs})

