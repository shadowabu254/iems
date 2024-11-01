from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('energy_visualization/', views.energy_visualization_view, name='energy_visualization'),
    path('energy_tips/', views.energy_tips_view, name='energy_tips'),
    path('carbon_calculator/', views.carbon_calculator_view, name='carbon_calculator'),
    path('community/', views.community_view, name='community'),
]
