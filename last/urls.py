from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from last import views

app_name = "last"

urlpatterns = [
                  path('', views.index, name="index"),
                  path('dashboard/', views.dashboard, name='dashboard'),
                  path('all_projects/', views.all_projects, name='all_projects'),
                  path('all_hackathons/', views.all_hackathons, name='all_hackathons'),
                  path('hackathon/<int:hackathon_id>', views.hackathon_detail, name='hackathon_details'),
                  path('profile/<str:pk>/', views.UserProfile, name="profile"),
                  path('members/', views.members, name="members"),
                  path('login/', views.user_login, name='login'),
                  path('logout/', views.user_logout, name='logout'),
                  path('register/', views.register, name='register'),
                  path('edit-profile/', views.updateProfile, name="edit-profile"),
                  path('update_hackathon/<int:hackathon_id>/', views.updateHackathon, name='update-hackathon'),
                  path('edit_contact/<int:contact_id>/', views.edit_contact, name='edit-contact'),
                  path('edit_project/<int:project_id>/', views.edit_project, name='edit-project'),
                  path('add_hackathon/', views.add_hackathon, name='add-hackathon'),
                  path('add_project/', views.add_project, name='add-project'),
                  path('project/<int:project_id>/', views.edit_project, name='project_detail'),
                  path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
                  path('hackathon/<int:hackathon_id>/delete/', views.delete_hackathon, name='delete_hackathon'),
                  path('profile/<int:user_id>/delete/', views.delete_profile, name='delete_profile'),
                  path('add-contact/', views.add_contact, name='add_contact'),
                  path('edit-contact/<int:contact_id>/', views.edit_contact, name='edit_contact'),
                  path('delete-contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
                  path('join-hackathon/<int:hackathon_id>/', views.join_hackathon, name='join_hackathon'),
                  path('grade-participant/<int:hackathon_id>/<int:participant_id>/', views.grade_participant,
                       name='grade_participant'),
                  path('grade_all_participants/<int:hackathon_id>/', views.grade_all_participants,
                       name='grade_all_participants'),
                  path('hackathon/<int:hackathon_id>/download-report/', views.download_hackathon_report,
                       name='download_hackathon_report'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'last.views.error_404_view'

handler403 = 'last.views.error_403_view'

handler401 = 'last.views.error_401_view'

handler400 = 'last.views.error_400_view'

handler500 = 'last.views.error_500_view'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
