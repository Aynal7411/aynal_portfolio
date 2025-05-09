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
    
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .models import ContactMessage
from .forms import ContactForm
from django.utils import timezone

class ContactView(FormView):
    template_name = 'contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        # Get client IP address
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else self.request.META.get('REMOTE_ADDR')

        ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message'],
            ip_address=ip_address
        )
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'contact_success.html'  