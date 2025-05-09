
from django.urls import path
from .views import ProfileDetailView, SkillListView


urlpatterns = [
    path('', ProfileDetailView.as_view(), name='home'),
    path('skills/', SkillListView.as_view(), name='skill_list'),
   
]