from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/user/', views.user_login_view, name='user_login'),
    path('login/authority/', views.authority_login_view, name='authority_login'),
    path('login/', views.user_login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('authority/', views.authority_dashboard_view, name='authority_dashboard'),
    path('authority/verify/<int:doc_id>/', views.authority_verify_sign_view, name='authority_verify_sign'),
    path('authority/document/<int:doc_id>/', views.authority_document_detail_view, name='authority_document_detail'),
    path('verify/<int:doc_id>/', views.verify_document_view, name='verify_document'),
    path('document/<int:doc_id>/', views.document_detail_view, name='document_detail'),
]
