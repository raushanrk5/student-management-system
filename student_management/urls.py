"""student_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from student_management import settings
from student_app import views,Hodviews,Staffviews,Studentviews

urlpatterns = [
    path('', views.show_login, name="show_login"),
    path('dologin/', views.dologin, name='dologin'),
    path('demo/',views.demo),
    path('admin/', admin.site.urls, name='admin'),
    path('get_user_details/', views.GetUserDetails),
    path('logout/',views.Logout, name='logout'),
    path('admin_home',Hodviews.admin_home, name="admin_home"),
    path('add_staff',Hodviews.add_staff, name='add_staff'),
    path('add_staff_save',Hodviews.add_staff_save, name='add_staff_save'),
    path('add_student',Hodviews.add_student, name='add_student'),
    path('add_student_save',Hodviews.add_student_save, name='add_student_save'),
    path('add_course',Hodviews.add_course, name='add_course'),
    path('add_course_save',Hodviews.add_course_save, name='add_course_save'),
    path('add_subject',Hodviews.add_subject, name='add_subject'),
    path('add_subject_save',Hodviews.add_subject_save, name='add_subject_save'),
    path('manage_staffs',Hodviews.manage_staffs, name='manage_staffs'),
    path('manage_students',Hodviews.manage_students, name='manage_students'),
    path('manage_courses',Hodviews.manage_courses, name='manage_courses'),
    path('manage_subjects',Hodviews.manage_subjects, name='manage_subjects'),
    path('edit_staff/<str:staff_id>',Hodviews.edit_staff, name='edit_staff'),
    path('edit_staff_save',Hodviews.edit_staff_save, name='edit_staff_save'),
    path('edit_student/<str:student_id>',Hodviews.edit_student, name='edit_student'),
    path('edit_student_save',Hodviews.edit_student_save, name='edit_student_save'),
    path('edit_course/<str:course_id>',Hodviews.edit_course, name='edit_course'),
    path('edit_course_save',Hodviews.edit_course_save, name='edit_course_save'),
    path('edit_subject/<str:subject_id>',Hodviews.edit_subject, name='edit_subject'),
    path('edit_subject_save',Hodviews.edit_subject_save, name='edit_subject_save'),
    
    #staff urls
    path('staff_home', Staffviews.staff_home, name="staff_home"),
                  
    #student urls
    path('student_home', Studentviews.student_home, name="student_home"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
