from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin', views.admin, name='admin'),
    path('course', views.course, name='course'),
    path('student', views.student, name='student'),
    path('show', views.show, name='show'),
    path('show_teachers', views.show_teachers, name='show_teachers'),
    path('add_student', views.add_student, name='add_student'),
    path('add_course', views.add_course, name='add_course'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('edit_details/<int:id>', views.edit_details, name='edit_details'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('delete_teacher/<int:id>', views.delete_teacher, name='delete_teacher'),
    path('signup_teacher', views.signup_teacher, name='signup_teacher'),
    path('signup_fun', views.signup_fun, name='signup_fun'),
    path('login_page', views.login_page, name='login_page'),
    path('login_fun', views.login_fun, name='login_fun'),
    path('logout_fun', views.logout_fun, name='logout_fun'),
    path('teacher/<int:id>', views.teacher, name='teacher'),
    path('edit_tchr/<int:id>', views.edit_tchr, name='edit_tchr'),
    path('edit_teacher/<int:id>', views.edit_teacher, name='edit_teacher'),
]