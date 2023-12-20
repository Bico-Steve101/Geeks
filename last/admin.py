
from django.contrib import admin
from .models import Test, Hackathons,  Team, Contacts,  Grade, Projects, User

# Register your models here.


# admin.site.register(User)
admin.site.register(Projects)
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Contacts)
# admin.site.register(UserContact)
admin.site.register(Hackathons)
admin.site.register(Test)
admin.site.register(Grade)
# admin.site.register(Space)
