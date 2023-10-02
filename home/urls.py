from django.urls import path,include
from . views import *
urlpatterns = [
    
    path('',index),
    path('user_login',user_login,name="user_login"),
    path('user_register',user_register,name="user_register"),
    path('user_home',user_home,name="user_home"),
    path('user_logout',user_logout,name="user_logout"),
    path('new_test',new_test,name="new_test"),
    path('download_report/<int:report_id>/', download_pdf_report, name='download_pdf_report'),
    path('test_history',test_history,name="test_history")
   
  
   

]