from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('custom-admin/view-participants/<int:event_id>/', views.view_event_participants, name='view_event_participants'),

    path('register/', views.register_view, name='register'),
]
    