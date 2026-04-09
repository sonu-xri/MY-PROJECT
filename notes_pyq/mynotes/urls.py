from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('resend-otp/<int:user_id>/', views.resend_otp, name='resend_otp'),

    path('contact/', views.contact, name='contact'),
    path('help/', views.help_page, name='help'),
    path('button/', views.button, name='button'),

    # ✅ forms
    path('pyq-form/', views.pyq_form, name='pyq_form'),
    path('notes-form/', views.notes_form, name='notes_form'),

    # ✅ upload routes (give DIFFERENT names)
    path('upload/notes/', views.notes_form, name='upload_notes'),
    path('upload/pyq/', views.pyq_form, name='upload_pyq'),
    
    # ✅ PROFILE PAGE
    path('profile/', views.profile, name='profile'),
    
    # ✅ notes PAGE
    path('notespage/', views.notespage, name='notespage'),
    
    path('student/', views.student, name='student'),
    path('teacher/', views.teacher, name='teacher'),
    
    
]