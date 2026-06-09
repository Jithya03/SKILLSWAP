from django.urls import path
from .import views
app_name = 'skills'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('TeacherProfile/', views.profile, name='TeacherProfile'),
    path('teach/', views.teach, name='teach'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   # path('signup/', views.signup_view, name='signup'),
    path('how_it_works/', views.how_it_works, name='How_it_Works'),
    path('learn/', views.learn, name='learn'),
    path('myprofile/',views.learner_profile,name='learner_profile'),
    path('edit-learner-profile/',views.edit_learner_profile,name='edit_learner_profile'),
    path('join/', views.join, name='join'),
    path('learn/', views.learn, name='learn'),
    path('LearnerProfile/', views.learner, name='LearnerProfile'),
    path('myprofile/',views.learner_profile,name='learner_profile'),
    path('explore/', views.explore, name='Explore'),
    path('profile/', views.teacher, name='profile'),
    path('teacher/', views.teacher, name='teacher'),
    path('login/', views.login_view, name='login'),
    path('learn/', views.learn, name='learn'), 
    path('teach/', views.teach, name='teach'), 
    path('rate/<str:username>/', views.rate_teacher, name='rate_teacher'),
    path('message/', views.teach, name='Message'),
    path('register/', views.register, name='register'),
    path('',views.index,name='index'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_request_view, name='log1'),
    path('verify/', views.verify_otp_view, name='verify'),
    path('logout/', views.logout_view, name='logout'),
    path('search/',views.search_teachers,name='search_teachers'),
    path('chat/<int:user_id>/', views.chat, name='chat'),
    path('inbox/', views.inbox, name='inbox'),
    path('swap-dashboard/', views.swap_dashboard, name='swap_dashboard'),
    path('active-swaps/',views.active_swaps,name='active_swaps'),
    path('learning/', views.learning_dashboard, name='learning_dashboard'),
    path('teaching/', views.teaching_dashboard, name='teaching_dashboard'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('video-call/<int:user_id>/',views.video_call,name='video_call'),
    
]

    




    