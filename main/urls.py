from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('programs/', views.list_programs, name='list_programs'),
    path('programs/<int:program_id>/', views.program_detail, name='program_detail'),
    path('programs/new/', views.new_program, name='new_program'),
    path('participants/', views.list_participants, name='list_participants'),
    path('participants/new/', views.new_participant, name='new_participant'),
    path('membership/', views.membership, name='membership'),
    path('membership/upload-document/', views.upload_document, name='upload_document'),
    path('donate/', views.donate, name='donate'),
    path('vendor/', views.vendor, name='vendor'),
    path('register/', views.register, name='register'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

