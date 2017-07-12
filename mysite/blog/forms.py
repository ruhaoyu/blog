from django import forms
from .models import Comment, Post
from django.contrib.auth.models import User



class EmailPostForm(forms.Form):
	'''邮件分享表单'''
	name = forms.CharField(max_length=25, label="名称")
	email = forms.EmailField(label='电子邮件')
	to = forms.EmailField(label='接收邮箱')
	comments = forms.CharField(required=False, widget=forms.Textarea, label='建议')


class CommentForm(forms.ModelForm):
	'''帖子评论表单'''
	class Meta:
		model = Comment
		fields = ('name', 'email', 'body')
		labels = {
		'name': "姓名",
		'email': "电子邮件",
		'body':"评论内容"
		}


class PostForm(forms.ModelForm):
	'''编辑帖子表单'''
	class Meta:
		model = Post
		fields = ('title', 'body', 'status', 'tags')
		labels = {
			'title': '标题',
			'body': '正文',
			'status': '是否发布',
			'tags': '标签',
		}
		widget = {'body': forms.Textarea(attrs={'cols':80})}


class UserPostForm(forms.ModelForm):
	"""发帖表单"""
	class Meta:
		model = Post
		fields = ('title', 'publish', 'body', 'status', 'tags')
		'''labels = {
			'title': '标题',
			'body': '正文',
			'status': '是否发布',
			'tags': '标签',
		}'''
		
