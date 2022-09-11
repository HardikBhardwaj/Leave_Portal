from django.urls import path

from. import views

urlpatterns = [
    path('password/', views.change_password, name='change_password'),
    path('',views.home,name='home'),
    path('home/',views.home1,name='home1'),
    path('adminview/',views.adminview,name='adminview'),
    path('showdata/',views.showdata,name='showdata'),
    path('leavepolicy/',views.leavepolicy,name='leavepolicy'),
     path('forreason1/',views.forreason1,name='forreason1'),
    path('holiday/',views.holiday,name='holiday'), 
     path('leave',views.leave,name='leave'),
      path('overwork/',views.overwork,name='overwork'),
      path('delete/',views.delete,name='delete'),
      path('reset/',views.reset,name='reset'),
      path('forgot/',views.forgot1,name="forgot1"),
      path('forgotsave',views.forgotsave,name="forgotsave"),
      path('showholiday',views.showholiday,name="showholiday"),
]