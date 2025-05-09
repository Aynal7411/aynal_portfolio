
from django.urls import path
from .views import ProfileDetailView, SkillListView, ContactView, ContactSuccessView


urlpatterns = [
    path('', ProfileDetailView.as_view(), name='home'),
    path('skills/', SkillListView.as_view(), name='skill_list'),
     path('contact/', ContactView.as_view(), name='contact'),
    path('contact/success/', ContactSuccessView.as_view(), name='contact_success'),
   
]