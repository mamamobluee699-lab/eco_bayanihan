from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('register/', views.register, name='register'),
	path('login/', views.volunteer_login, name='volunteer_login'),
	path('logout/', views.volunteer_logout, name='volunteer_logout'),
	path('custom-admin/', views.custom_admin_panel, name='custom_admin_panel'),
    path('select-event/', views.select_event, name='select_event'),
    path('previous-events/', views.previous_events_list, name='previous_events'),
    path('registration-success/<int:event_id>/', views.registration_success, name='registration_success'),
	path('dashboard/', views.volunteer_dashboard, name='volunteer_dashboard'),
	path('home/', views.home, name='home'),
	#path('admin/participants/', views.admin_participants_manage, name='admin_participants'),
	path('status/', views.status_lookup, name='status'),
    # Custom Admin Panel
    path('custom-admin/', views.custom_admin_panel, name='custom_admin_panel'),
    # Show participants of a specific event
path('custom-admin/event-participants/<int:event_id>/', views.event_participants, name='event_participants'),
path("admin-login/", views.admin_login, name="admin_login"),
path("admin-logout/", views.admin_logout, name="admin_logout"),

path("custom-admin/", views.custom_admin_panel, name="custom_admin_panel"),
path('points-history/', views.points_history, name='points_history'),
    path('event-history/', views.event_list, name='event_history'),
    path('combined-history/', views.combined_list, name='combined_history'),


    # CRUD for Events
    path('custom-admin/add-event/', views.add_event, name='add_event'),
    path('custom-admin/edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('custom-admin/delete-event/<int:event_id>/', views.delete_event, name='delete_event'),

    # CRUD for Participants
    path('custom-admin/add-participant/', views.add_participant, name='add_participant'),
    path('custom-admin/edit-participant/<int:participant_id>/', views.edit_participant, name='edit_participant'),
    path('custom-admin/delete-participant/<int:participant_id>/', views.delete_participant, name='delete_participant'),

    # Give Points
    path('custom-admin/give-points/<int:participant_id>/', views.give_points, name='give_points'),
]
	#path('participants/', views.ParticipantListView.as_view(), name='participant_list'),
	#path('registration/<int:registration_id>/upload-proof/', views.upload_proof, name='upload_proof'),
	#path('registration/<int:registration_id>/approve/', views.approve_registration, name='approve_registration'),
	# Custom event management (moved off Django admin prefix)
	#path('admin/events/', views.admin_event_list, name='admin_event_list'),
	#path('admin/events/create/', views.admin_event_create, name='admin_event_create'),
	#path('admin/events/<int:event_id>/edit/', views.admin_event_edit, name='admin_event_edit'),
	#path('admin/events/<int:event_id>/delete/', views.admin_event_delete, name='admin_event_delete'),

