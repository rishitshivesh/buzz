from django.contrib import admin
from .models import User,Post,Like,Profile

# Register your models here.
class UserDisplay(admin.ModelAdmin):
    list_display = ("id","first_name","last_name","username","email")
admin.site.register(User,UserDisplay)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Profile)

