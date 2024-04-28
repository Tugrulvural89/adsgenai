from django.contrib import admin
from .models import Blog, Contact, CustomPage, BusinessInquiry


@admin.register(BusinessInquiry)
class BusinessInquiryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_description', 'ad_product', 'chatgpt_response']
    list_filter = ['ad_product']
    search_fields = ['user_description', 'ad_product']

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'status')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'text')
    prepopulated_fields = {'slug': ('title',)}

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'content')
    search_fields = ('name', 'email')


class CustomPageAdmin(admin.ModelAdmin):
    list_display = ('tag', 'title', 'text', 'image', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Blog, BlogAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(CustomPage, CustomPageAdmin)
