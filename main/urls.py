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
    path('admin/fund-distributions/', views.fund_distribution_list, name='fund_distribution_list'),
    path('admin/fund-distributions/new/', views.fund_distribution_new, name='fund_distribution_new'),
    path('admin/fund-distributions/<int:distribution_id>/approve/', views.fund_distribution_approve, name='fund_distribution_approve'),
    path('admin/fund-distributions/<int:distribution_id>/distribute/', views.fund_distribution_distribute, name='fund_distribution_distribute'),
    path('admin/data-vault/', views.data_vault_list, name='data_vault_list'),
    path('admin/data-vault/upload/', views.data_vault_upload, name='data_vault_upload'),
    path('admin/data-vault/<int:item_id>/', views.data_vault_view, name='data_vault_view'),
]

