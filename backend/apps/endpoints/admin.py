from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Endpoint)
admin.site.register(DL_Comment)
admin.site.register(DL_CommentStatus)
admin.site.register(DL_CommentRequest)

