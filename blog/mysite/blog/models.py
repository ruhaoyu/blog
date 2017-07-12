from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
	'''用于筛选发布状态的帖子'''
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset().filter(status='published')


class Post(models.Model):
	'''帖子数据模型'''
	# owner = models.ForeignKey(User, verbose_name='所有者')
	STATUS_CHOICES = (
	('draft','存为草稿'),('published','直接发布'),
	)
	title = models.CharField('标题',max_length=250)
	slug = models.SlugField('链接', max_length=250,unique_for_date='publish')
	author = models.ForeignKey( User,related_name='blog_posts', verbose_name='作者')
	body = models.TextField('正文')
	publish = models.DateTimeField('发布时间', default=timezone.now)
	created = models.DateTimeField('创建时间',auto_now_add=True)
	updated = models.DateTimeField('修改时间', auto_now=True)
	status = models.CharField('状态', max_length=10,choices=STATUS_CHOICES,default='draft')
	objects = models.Manager() # 默认管理员
	published = PublishedManager() # 用户管理员
	tags = TaggableManager('标签')
	
	class Meta:
		ordering = ('publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_detail',
				args=[self.publish.year,self.publish.strftime('%m'),
				self.publish.strftime('%d'),
				self.slug])


class Comment(models.Model):
	'''评论数据模型'''
	post = models.ForeignKey(Post, related_name='comments', verbose_name='标题')
	name = models.CharField('名字', max_length=80)
	email = models.EmailField('邮件')
	body = models.TextField('评论内容')
	created = models.DateTimeField('创建时间',auto_now_add=True)
	updated = models.DateTimeField('修改时间', auto_now=True)
	active = models.BooleanField('是否有效',default=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)
			

