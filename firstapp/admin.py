from django.contrib import admin


from  firstapp.models import Post


admin.site_header='punda'





# Register your models here.
admin.site.register(Post)