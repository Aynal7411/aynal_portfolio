from django.contrib import admin
from core.models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'professional_title', 'email', 'available_for_freelance')
    search_fields = ('name', 'email')
    
    def has_add_permission(self, request):
        """Prevent creating multiple profiles"""
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'proficiency', 'show_in_skillset')
    list_filter = ('level', 'show_in_skillset')
    list_editable = ('proficiency', 'show_in_skillset')
    ordering = ('order', '-proficiency')

@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'docs_url')
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'client_name', 'start_date')
    list_filter = ('featured', 'tech_stack')
    search_fields = ('title', 'description')
    filter_horizontal = ('tech_stack',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'order')
    list_editable = ('featured', 'order')
    ordering = ('order',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'approved', 'featured')
    list_filter = ('approved', 'featured')
    list_editable = ('approved', 'featured')
    search_fields = ('client_name', 'feedback')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('ip_address', 'created_at')
    actions = ['mark_as_read', 'mark_as_answered']

    def mark_as_read(self, request, queryset):
        queryset.update(status='R')
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_answered(self, request, queryset):
        queryset.update(status='A')
    mark_as_answered.short_description = "Mark selected as answered"