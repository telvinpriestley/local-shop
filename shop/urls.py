from django.urls import path
from shop import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('name_list', views.name_list, name='name_list'),
    path('update_customer_view', views.update_customer_view, name='update_customer_view'),
    path('delete_view', views.delete_view, name='delete_view'),
    path('delete', views.delete, name='delete'),
    
    path('items_view', views.items_view, name='items_view'),
    path('reg_items', views.reg_items, name='reg_items'),
    path('update_items_view/<int:id>', views.update_items_view, name='update_items_view'),
    path('update_items/<int:id>', views.update_items, name='update_items'),
    
    path('neworder_view', views.neworder_view, name='neworder_view'),
    path('newreg_order', views.newreg_order, name='newreg_order'),
    path('delete_order/<int:ord_id>', views.delete_order, name='delete_order'),
    
    path('payment_history/<int:cus_id>', views.payment_history, name='payment_history'),
    path('history_admin', views.history_admin, name='history_admin'),
    path('payment_page', views.payment_page, name='payment_page'),
    path('payment_view', views.payment_view, name='payment_view'),
    
    
    
    path('signup_view', views.signup_view, name='signup_view'),
    path('signup', views.signup, name='signup'),
    path('login_view', views.login_view, name='login_view'),
    path('log_in', views.log_in, name='log_in'),
    path('loginFirst', views.loginFirst, name='loginFirst'),
    path('logout_view/', views.logout_view, name='logout_view'),
    
    path('sendemail', views.sendemail, name='sendemail'),
    path('emailVerification_sign_up', views.emailVerification_sign_up, name='emailVerification_sign_up'),
    path('verification_view', views.verification_view, name='verification_view'),
    path('verification_proper', views.verification_proper, name='verification_proper'),
    
    path('login_email_verify', views.login_email_verify, name='login_email_verify'),
    path('login_verify_view', views.login_verify_view, name='login_verify_view'),
    path('login_proper', views.login_proper, name='login_proper'),
    
    path('toggle_ban_user', views.toggle_ban_user, name='toggle_ban_user'),
    
    path('notauth', views.notauth, name='notauth'),
    
    

   
]