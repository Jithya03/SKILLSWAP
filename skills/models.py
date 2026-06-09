from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Skill(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    learners = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('learner', 'Learner'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    skill = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name    
    
# from django.contrib.auth.models import User

# class TeacherProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     skill = models.CharField(max_length=100)
#     description = models.TextField()
#     experience = models.TextField(blank=True)
#     rate = models.IntegerField(default=0)
#     credits = models.IntegerField(default=0)  

#     def __str__(self):
#         return self.name
    
   
class Rating(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_rating")
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(blank=True)

    def __str__(self):
        return f"{self.teacher.username} - {self.rating}"
    
from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    skill = models.CharField(max_length=100)
    role = models.CharField(max_length=10)

class Message(models.Model):

    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        User,
        related_name='received_messages',
        on_delete=models.CASCADE
    )

    message = models.TextField(blank=True, null=True)

    file = models.FileField(
        upload_to='chat_files/',
        blank=True,
        null=True
    )

    voice = models.FileField(
        upload_to='voice_notes/',
        blank=True,
        null=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

class Message(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    message = models.TextField(blank=True, null=True)

    file = models.FileField(
        upload_to='chat_files/',
        blank=True,
        null=True
    )

    voice = models.FileField(
        upload_to='voice_notes/',
        blank=True,
        null=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)
        
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
class TeacherProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    skill = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    experience = models.IntegerField(
        default=0
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='teachers/',
        blank=True,
        null=True
    )

    rate = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.full_name or self.user.username

from django.db import models
from django.contrib.auth.models import User


class LearnerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    skill_to_learn = models.CharField(
        max_length=200
    )

    skill_to_teach = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    interests = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='learners/',
        blank=True,
        null=True
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class EmailOTP(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    used = models.BooleanField(default=False)

    def is_expired(self, expiry_seconds):

        return timezone.now() > (
            self.created_at +
            timedelta(seconds=expiry_seconds)
        )

    def __str__(self):
        return f"{self.user.email} - {self.code}"    

class Swap(models.Model):

    learner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='learning_swaps'
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teaching_swaps'
    )

    skill = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.learner.username} learning {self.skill}"