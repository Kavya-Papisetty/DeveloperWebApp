from django.urls import path
from . import views
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.home_view),

    path('adminclick', views.adminclick_view, name = 'adminclick'),
    path('studentclick', views.studentclick_view, name = 'studentclick'),


    path('adminsignup', views.adminsignup_view, name = 'adminsignup'),
    path('studentsignup', views.studentsignup_view, name = 'studentsignup'),
    path('adminlogin', LoginView.as_view(template_name='library/adminlogin.html'), name = 'adminlogin'),
    path('studentlogin', LoginView.as_view(template_name='library/studentlogin.html'), name = 'studentlogin'),

    path('logout', LogoutView.as_view(template_name='library/index.html'), name = 'logout'),
    path('afterlogin', views.afterlogin_view, name = 'afterlogin'),

    path('addbook', views.addbook_view, name = 'addbook'),
    path('viewbook', views.viewbook_view, name = 'viewbook'),
    path('issuebook', views.issuebook_view, name = 'issuebook'),
    path('viewissuedbook', views.viewissuedbook_view, name = 'viewissuedbook'),
    path('viewstudent', views.viewstudent_view, name ='viewstudent'),
    path('viewissuedbookbystudent', views.viewissuedbookbystudent, name = 'viewissuedbookbystudent'),

    path('aboutus', views.aboutus_view, name = 'aboutus'),
    path('contactus', views.contactus_view, name = 'contactus'),
    path('delete/<str:pk>/', views.delete_book, name = 'delete'),
    path('update', views.Update, name = 'update'),
    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),

    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('my-fines/',views.myfines, name = 'my-fines'),
    path('payfines/<int:fineID>/',views.payfine,name = 'payfines'),
    path('paystatus/<int:fineID>/',views.pay_status, name = 'paystatus'),
    path('all-fines/',views.allfines, name = 'all-fines'),
]
