from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.utils.text import slugify
from django.utils import timezone

class Profile(models.Model):
    name = models.CharField(max_length=100)
    professional_title = models.CharField(max_length=200, blank=True)
    bio = models.TextField()
    short_bio = models.CharField(max_length=200, blank=True, help_text="Short bio for preview cards")
    photo = models.ImageField(upload_to='profile/', default='profile/default.png')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    linkedin = models.URLField(blank=True, validators=[URLValidator()])
    github = models.URLField(blank=True, validators=[URLValidator()])
    twitter = models.URLField(blank=True, validators=[URLValidator()])
    personal_website = models.URLField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    available_for_freelance = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.professional_title}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['-created_at']

class Skill(models.Model):
    SKILL_LEVELS = (
        ('B', 'Beginner'),
        ('I', 'Intermediate'),
        ('A', 'Advanced'),
        ('E', 'Expert'),
    )

    name = models.CharField(max_length=50)
    level = models.CharField(max_length=1, choices=SKILL_LEVELS, default='I')
    proficiency = models.PositiveIntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Proficiency percentage from 0-100"
    )
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    show_in_skillset = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    years_experience = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

    class Meta:
        ordering = ['order', '-proficiency']

class TechStack(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True)
    docs_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    PROJECT_CATEGORIES = (
        ('WD', 'Web Development'),
        ('MD', 'Mobile Development'),
        ('DS', 'Data Science'),
        ('ML', 'Machine Learning'),
    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.TextField()
    excerpt = models.CharField(max_length=200, blank=True)
    tech_stack = models.ManyToManyField(TechStack)
    image = models.ImageField(upload_to='projects/')
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    client_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-featured', '-start_date']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

class Service(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='fas fa-service')
    description = models.TextField()
    short_description = models.CharField(max_length=150, blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    cta_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', '-featured']

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_company = models.CharField(max_length=100, blank=True)
    client_role = models.CharField(max_length=100, blank=True)
    feedback = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    avatar = models.ImageField(upload_to='testimonials/', blank=True)
    featured = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial from {self.client_name}"

    class Meta:
        ordering = ['-featured', '-created_at']

class ContactMessage(models.Model):
    STATUS_CHOICES = (
        ('U', 'Unread'),
        ('R', 'Read'),
        ('A', 'Answered'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='U')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"