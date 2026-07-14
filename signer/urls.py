from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('sign/<int:doc_id>/', views.sign_document_view, name='sign_document'),
    path('verify/', views.verify_document_view, name='verify'),
    path('verify/<int:doc_id>/', views.verify_document_view, name='verify_document'),
    path('document/<int:doc_id>/', views.document_detail_view, name='document_detail'),
]
