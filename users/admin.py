from django.contrib import admin

# Register your models here.
from .models import User, Contact, Spam, SpamMarkedBy


admin.site.register(User)


admin.site.register(Contact)


admin.site.register(Spam)


admin.site.register(SpamMarkedBy)