from django.shortcuts import render
from .models import Skill, Category,TeacherProfile
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Teacher
from django.shortcuts import render, redirect
from .forms import RatingForm
from django.contrib.auth.models import User


def home(request):
    skills = Skill.objects.all()[:3]
    categories = Category.objects.all()

    context = {
        'skills': skills,
        'categories': categories
    }

    return render(request, 'home.html', context)





from django.shortcuts import render, redirect
from .models import UserProfile

# def signup(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         role = request.POST.get('role')
#         skill = request.POST.get('skill')

#         UserProfile.objects.create(
#             username=username,
#             email=email,
#             password=password,
#             role=role,
#             skill=skill
#         )

    #     return redirect('skill/explore')

    # return render(request, 'reg.html')



def login_view(request):
    if request.method == 'POST':
       
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role') 

        
        if role == 'teacher':
            return redirect('TeacherProfile') 
        else:
            return redirect('LearnerProfile') 

    return render(request, 'skills/login.html')


def earn_credit(request, teacher_id):
    
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    
    teacher.credits += 10
    teacher.save()
    
    messages.success(request, f"You have started learning from {teacher.name}!")
    return redirect('learn_page') 



def teach(request):
    return render(request, 'teach.html')

def profile(request):
    return render(request, 'profile.html')

def index(request):
    return render(request, 'skills/home.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm
from .models import TeacherProfile, LearnerProfile

def signup_view(request):

    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save()

            role = request.POST.get('role')
            skill = request.POST.get('skill')

            # Teacher signup
            if role == 'teacher':

                TeacherProfile.objects.create(
                    user=user,
                    skill=skill
                )

                login(request, user)

                return redirect('/TeacherProfile/')

            # Learner signup
            else:

                LearnerProfile.objects.create(
                    user=user,
                    skill_to_learn=skill
                )

                login(request, user)

                return redirect('/LearnerProfile/')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {
        'form': form
    })


def teacher(request):
    return render(request, 'TeacherProfile.html')


def learner(request):
    return render(request, 'LearnerProfile.html')              
        
def explore(request):
    return render(request, 'explore.html')




def how_it_works(request):
    return render(request, 'How_it_Works.html')

def logout_page(request):
    return render(request, 'logout.html')

def learner(request):
    return render(request, 'LearnerProfile.html')

def learn(request):
    return render(request, 'skills/learn.html')

def join(request):
    return render(request, 'join.html')


def getstarted(request):
    return render(request, 'login.html')

def message(request):
    return render(request, 'Message.html')




def rate_teacher(request, username):
    teacher = User.objects.get(username=username)

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.teacher = teacher
            rating.learner = request.user
            rating.save()
            return redirect("explore")

    else:
        form = RatingForm()

    return render(request, "rateteacher.html", {"form": form, "teacher": teacher})



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']  # teacher / student

        user = User.objects.create_user(username=username, password=password)

        TeacherProfile.objects.create(user=user, role=role)

    return redirect('reg')


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login,logout
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from .forms import RequestOTPForm, VerifyOTPForm
from .models import EmailOTP
from .tokens import generate_numeric_otp
from .forms import SignupForm
from django.contrib.auth import authenticate

User = get_user_model()

def dashboard(request):
    return render(request, 'skills/base1.html') 

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm
from .models import TeacherProfile, LearnerProfile

from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import TeacherProfile, LearnerProfile

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.db import IntegrityError

from .forms import SignupForm
from .models import TeacherProfile, LearnerProfile


def signup_view(request):

    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():

            try:

                user = form.save()

            except IntegrityError:

                messages.error(request, "Username already exists")

                return render(request, 'signup.html', {
                    'form': form
                })

            role = form.cleaned_data['role']
            skill = form.cleaned_data['skill']

            if role == 'teacher':

                TeacherProfile.objects.create(
                    user=user,
                    skill=skill
                )

                login(request, user)

                return redirect('skills:teach')

            else:

                LearnerProfile.objects.create(
                    user=user,
                    skill_to_learn=skill
                )

                login(request, user)

                return redirect('skills:LearnerProfile')

    else:

        form = SignupForm()

    return render(request, 'signup.html', {
        'form': form
    })

               
       

def login_request_view(request):
    if request.method == 'POST':
        form = RequestOTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Email not registered. Please signup first.")
                return redirect('skills:signup')

            # generate OTP
            otp_code = generate_numeric_otp(settings.OTP_LENGTH)
            EmailOTP.objects.create(user=user, code=otp_code)

            # send OTP via email
            send_mail(
                subject="Your Login OTP",
                message=f"Your OTP code is {otp_code}. It expires in {settings.OTP_EXPIRY_SECONDS // 60} minutes.",
                from_email=None,
                recipient_list=[email],
                fail_silently=False
            )

            # redirect to verify page using reverse
            return redirect(f"{reverse('skills:verify')}?email={email}")
    else:
        form = RequestOTPForm()
    return render(request, 'skills/log1.html', {'form': form})

def verify_otp_view(request):
    initial_email = request.GET.get('email') or request.POST.get('email')

    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = form.cleaned_data['otp'].strip()

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
                return redirect('skills:log1')

            # Get last unused OTP
            otps = EmailOTP.objects.filter(user=user, used=False).order_by('-created_at')
            if not otps:
                messages.error(request, "No OTP found, request a new one.")
                return redirect('skills:log1')

            latest = otps[0]

            if latest.code != otp:
                messages.error(request, "Invalid OTP")
                return redirect(f'/verify/?email={email}')
            if latest.is_expired(settings.OTP_EXPIRY_SECONDS):
                messages.error(request, "OTP expired. Request a new one.")
                return redirect('skills:log1')

            # Mark OTP as used and log in
            latest.used = True
            latest.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            # ✅ Redirect after login
            return redirect('skills:dashboard')

    else:
        form = VerifyOTPForm(initial={'email': initial_email})

    return render(request, 'skills/verify.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('skills:base1') 
from django.shortcuts import render
from .models import TeacherProfile

def search_teachers(request):

    query = request.GET.get('skill')

    teachers = TeacherProfile.objects.filter(
        skill__icontains=query
    )

    return render(request, 'search_results.html', {
        'teachers': teachers,
        'query': query
    })


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message

from django.db.models import Q

def chat(request, user_id):

    receiver = User.objects.get(id=user_id)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')

    # mark received messages as read
    Message.objects.filter(
        sender=receiver,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    if request.method == "POST":

        text = request.POST.get('message')

        uploaded_file = request.FILES.get('file')

        voice = request.FILES.get('voice')

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            message=text,
            file=uploaded_file,
            voice=voice
        )

        return redirect('skills:chat', user_id=user_id)

    return render(request, 'skills/chat.html', {
        'receiver': receiver,
        'messages': messages
    })
from .models import Message

def inbox(request):

    received_messages = Message.objects.filter(
        receiver=request.user
    ).order_by('timestamp')

    return render(request, 'skills/inbox.html', {
        'messages': received_messages
    })

from django.contrib.auth.decorators import login_required
from .models import TeacherProfile

@login_required(login_url='skills:log1')
def profile(request):

    teacher, created = TeacherProfile.objects.get_or_create(
        user=request.user
    )

    return render(request, 'TeacherProfile.html', {
        'teacher': teacher
    })

from .models import LearnerProfile

def learner(request):

    learner, created = LearnerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        learner.bio = request.POST.get('bio')

        learner.skill_to_teach = request.POST.get('teach')

        learner.skill_to_learn = request.POST.get('learn')

        interests = request.POST.getlist('interests')

        learner.interests = ", ".join(interests)

        learner.save()

        return redirect('skills:LearnerProfile')

    return render(request, 'learn.html', {
        'learner': learner
    })




from django.contrib.auth.decorators import login_required
from .models import TeacherProfile

@login_required
def teach(request):

    teacher, created = TeacherProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        teacher.full_name = request.POST.get('full_name')
        teacher.skill = request.POST.get('skill')
        teacher.bio = request.POST.get('bio')
        teacher.experience = request.POST.get('experience')
        teacher.rate = request.POST.get('rate')

        if request.FILES.get('profile_image'):
            teacher.profile_image = request.FILES.get('profile_image')

        teacher.save()

        return redirect('skills:TeacherProfile')

    return render(request, 'teach.html', {
        'teacher': teacher
    })

def explore(request):

    teachers = TeacherProfile.objects.all()

    query = request.GET.get('q')

    if query:
        teachers = teachers.filter(skill__icontains=query)

    return render(request, 'explore.html', {
        'teachers': teachers,
        'query': query
    })

from .models import LearnerProfile
def learner(request):

    learner, created = LearnerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        learner.bio = request.POST.get('bio')
        learner.skill_to_teach = request.POST.get('teach')
        learner.skill_to_learn = request.POST.get('learn')

        interests = request.POST.getlist('interests')
        learner.interests = ", ".join(interests)

        learner.save()

        return render(request, 'LearnerProfile.html', {
            'learner': learner
        })

    return render(request, 'learn.html')


from .models import LearnerProfile, Message

def learner_profile(request):

    learner = LearnerProfile.objects.get(
        user=request.user
    )

    unread_count = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()

    return render(request, 'LearnerProfile.html', {
        'learner': learner,
        'unread_count': unread_count
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import LearnerProfile


@login_required
def edit_learner_profile(request):

    learner = LearnerProfile.objects.get(user=request.user)

    if request.method == 'POST':

        learner.bio = request.POST.get('bio')
        learner.skill_to_teach = request.POST.get('skill_to_teach')
        learner.skill_to_learn = request.POST.get('skill_to_learn')
        learner.interests = request.POST.get('interests')

        learner.save()

        return redirect('skills:learner_profile')

    return render(request,
    'skills/EditLearnerProfile.html',
    {'learner': learner})

from django.contrib.auth.decorators import login_required
from .models import LearnerProfile

@login_required
def learner(request):

    learner, created = LearnerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        learner.bio = request.POST.get('bio')

        learner.skill_to_teach = request.POST.get('teach')

        learner.skill_to_learn = request.POST.get('learn')

        interests = request.POST.getlist('interests')

        learner.interests = ", ".join(interests)

        # SAVE PROFILE IMAGE
        if request.FILES.get('profile_image'):

            learner.profile_image = request.FILES.get('profile_image')

        learner.save()

        return redirect('skills:learner_profile')

    return render(request, 'learn.html', {
        'learner': learner
    })
from django.contrib.auth.decorators import login_required

@login_required
def swap_dashboard(request):

    return render(request, 'swap_dashboard.html')

from django.contrib.auth.decorators import login_required
from .models import LearnerProfile, TeacherProfile

@login_required
def active_swaps(request):

    learner = LearnerProfile.objects.get(
        user=request.user
    )

    teachers = TeacherProfile.objects.filter(
        skill__icontains=learner.skill_to_learn
    )

    return render(request, 'active_swaps.html', {
        'learner': learner,
        'teachers': teachers
    })



def learning_dashboard(request):
    return render(request, 'learning.html')


def teaching_dashboard(request):
    return render(request, 'teaching.html')

from django.contrib.auth.models import User

def chat_view(request, user_id):

    receiver = User.objects.get(id=user_id)

    messages = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by('timestamp')

    return render(request, 'chat.html', {
        'receiver': receiver,
        'messages': messages
    })

from django.contrib.auth.decorators import login_required
from .models import TeacherProfile, LearnerProfile

@login_required
def teaching_dashboard(request):

    try:
        teacher_profile = TeacherProfile.objects.get(user=request.user)
    except TeacherProfile.DoesNotExist:
        return render(request, 'teaching.html', {
            'students': [],
            'error': "Complete your teacher profile first."
        })

    # IMPORTANT: exact matching is more reliable than icontains
    students = LearnerProfile.objects.filter(
        skill_to_learn=teacher_profile.skill
    ).select_related('user')

    return render(request, 'teaching.html', {
        'students': students,
        'teacher': teacher_profile
    })

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import LearnerProfile, TeacherProfile

def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # CHECK LEARNER PROFILE
            if LearnerProfile.objects.filter(user=user).exists():
                return redirect('skills:learner_profile')

            # CHECK TEACHER PROFILE
            elif TeacherProfile.objects.filter(user=user).exists():
                return redirect('skills:TeacherProfile')

        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def video_call(request, user_id):

    receiver = User.objects.get(id=user_id)

    room_name = f"skillswap_{min(request.user.id, receiver.id)}_{max(request.user.id, receiver.id)}"

    return render(request, 'video_call.html', {
        'receiver': receiver,
        'room_name': room_name
    })