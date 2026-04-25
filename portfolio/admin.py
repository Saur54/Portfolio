from django.contrib import admin
from .models import SocialLink, HomeSection, AboutSection, Skill, Education, Experience, Service, Project, ContactInfo, QueryMessage, Blog

admin.site.register(SocialLink)
admin.site.register(HomeSection)
admin.site.register(AboutSection)
admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Service)
admin.site.register(Project)
admin.site.register(ContactInfo)
admin.site.register(QueryMessage)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
