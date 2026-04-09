from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Resource
from django.utils import timezone
from .models import UserProfile
from .models import Contact


# ✅ HOME PAGE (SHOW INFORMATION)
def home(request):
    return render(request, 'home.html')


# 🔥 Role function
def get_user_role(email):
    if email.endswith('@gmail.com'):
        return 'student'
    else:
        return 'teacher'


# ✅ SIGNUP
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # ✅ Empty check
        if not username or not email or not password:
            messages.error(request, "❌ All fields are required")
            return redirect('signup')

        # ✅ Password match
        if password != confirm_password:
            messages.error(request, "❌ Passwords do not match")
            return redirect('signup')

        # ✅ Username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "❌ Username already exists")
            return redirect('signup')

        # ✅ Email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "❌ Email already registered")
            return redirect('signup')

        try:
            # ✅ Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # 🔥 Role detect
            role = get_user_role(email)

            # ✅ Create profile
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': role}
            )


            messages.success(request, "✅ Signup successful! Please login.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")
            return redirect('signup')

    return render(request, 'signup.html')



# ✅ login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            profile = UserProfile.objects.get(user=user)
            profile.last_login_time = timezone.now()
            profile.login_count += 1
            profile.save()

            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')




@login_required
def notes_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        category = request.POST.get('category')
        file = request.FILES.get('file')

        # 🔥 Auto role detect
        role = get_user_role(request.user.email)

        Resource.objects.create(
            user=request.user,
            title=title,
            subject=subject,
            description=description,
            category=category,
            teacher_student=role,
            file=file
        )

        messages.success(request, "✅ Notes uploaded successfully!")

        return redirect('student' if role == "student" else 'teacher')

    return render(request, 'notes_form.html')
@login_required
def pyq_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        category = request.POST.get('category')
        exam_year = request.POST.get('exam_year')
        semester = request.POST.get('semester')
        exam_type = request.POST.get('exam_type')
        file = request.FILES.get('file')

        role = get_user_role(request.user.email)

        if file:
            Resource.objects.create(
                user=request.user,
                title=title,
                subject=subject,
                description=description,
                category=category,
                teacher_student=role,
                exam_year=exam_year,
                semester=semester,
                exam_type=exam_type,
                file=file
            )

        messages.success(request, "✅ Uploaded successfully!")

        return redirect('student' if role == "student" else 'teacher')

    return render(request, 'pyq_form.html')

  
def student(request):
    notes = Resource.objects.filter(teacher_student="student")
    
    return render(request, 'student.html', {
        'notes': notes
    })



def teacher(request):
    resources = Resource.objects.filter(teacher_student="teacher")
    
    return render(request, 'teacher.html', {
        'resources': resources
    })


# ✅ LOGOUT
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# ✅ PROFILE PAGE (USER FILES)
@login_required
def profile(request):
    user_files = Resource.objects.filter(user=request.user).order_by('-id')
    return render(request, 'profile.html', {'resources': user_files})


# ✅ BUTTON PAGE
@login_required
def button(request):
    return render(request, 'button.html')


# ✅ CONTACT
@login_required
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
        messages.success(request, "✅ Message sent successfully!")

        return redirect('contact')

    return render(request, 'contact.html')



# ✅ HELP
def help_page(request):
    return render(request, 'help.html')


# ✅ FORGOT PASSWORD
def forgot_password(request):
    return render(request, 'forgot_password.html')


# ✅ notespage
def notespage(request):
    return render(request, 'notespage.html')


# ✅ VERIFY OTP
def verify_otp(request, user_id):
    return render(request, 'verify_otp.html', {'user_id': user_id})


# ✅ RESET PASSWORD
def reset_password(request, user_id):
    return render(request, 'reset_password.html', {'user_id': user_id})


# ✅ RESEND OTP
def resend_otp(request, user_id):
    messages.info(request, "OTP resent!")
    return redirect('verify_otp', user_id=user_id)

