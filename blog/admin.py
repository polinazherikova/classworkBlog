from django.contrib import admin
from .models import Post,Category,Tags,Comment,Subscriber,PostPhoto,Profile
# Register your models here.

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Tags)
admin.site.register(Comment)
admin.site.register(Subscriber)
admin.site.register(PostPhoto)
admin.site.register(Profile)
