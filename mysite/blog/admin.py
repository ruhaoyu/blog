from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
	'''用户管理'''
	list_display = ('title', 'slug', 'author', 'publish', 'status')
	search_fields = ('title', 'body')
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ('author',)
	date_hierarchy = 'publish'
	ordering = ['status','publish']


class CommentAdmin(admin.ModelAdmin):
	'''评论管理'''
	list_display = ('name', 'email', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'email', 'body')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
