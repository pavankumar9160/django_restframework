

from django.urls import path

from .views import *

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    
            path('create_student_record/',create_student_record.as_view(),name="create_student_record"),
            
            path('get_student_record/',get_student_record.as_view(),name="get_student_record"),
            path('update_record/',update_record.as_view(),name="update_record"),
            path('create_author_record/',create_author_record.as_view(),name="create_author_record"),
            path('get_author_records/',get_author_records.as_view(),name='get_author_records'),
            path('update_author_record/',update_author_record.as_view(),name='update_author_record'),
            path('update_student_record/',update_student_record.as_view(),name='update_student_record'),
            path('candidate/',CandidateCreateView.as_view(),name="CandidateCreateView"),
            path('candidates/<int:pk>/',CandidateDetailView.as_view(),name="CandidateDetailView"),
            
          
            
            path('add-student/', views.AddStudentPage, name="add-student"),
            path('edit-candidate/<int:id>/', views.EditCandidate, name="edit-candidate"),
            path('delete-candidate/<int:id>/', views.DeleteCandidate, name="delete-candidate"),


            
            path('GetAllCandidates/',GetAllCandidates.as_view(), name="GetAllCandidates"),
            
            path('signup/',views.signupView,name="signup"),
            
            path('login/',views.loginView,name="login"),
              path('logout/' ,views.logoutView,name="logout"),


            
            
            
              path('', views.CandidatePage, name="CandidatePage"),






]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)