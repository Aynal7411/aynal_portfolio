from django.shortcuts import render

from django.views.generic import DetailView
from core.models import Profile

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.first()  # Assuming single profile
    
from django.views.generic import ListView
from .models import Skill

class SkillListView(ListView):
    model = Skill
    template_name = 'skill_list.html'
    context_object_name = 'skills'
    
    def get_queryset(self):
        return Skill.objects.filter(show_in_skillset=True).order_by('order', '-proficiency')   