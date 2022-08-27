from django.contrib import admin
from .models import *

admin.site.register(Memo)
admin.site.register(Comment)
admin.site.register(Clap)
admin.site.register(Readable)
admin.site.register(Alert)