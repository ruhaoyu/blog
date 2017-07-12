from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.db.models import Count
from taggit.models import Tag
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, PostForm, UserPostForm


def post_list_index(request, tag_slug=None):
	'''显示所有用户的帖子'''
	#posts = Post.published.all()
	object_list = Post.published.all().order_by('-publish')
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list =object_list.filter(tags__in=[tag])
	paginator = Paginator(object_list,5) # 每个页面显示3条博客
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer diliver the first page
		posts = paginator.page(1)
	except EmptyPage:
		# if page is out of range deliver last page of results
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/list.html', {
												'page':page,
												'posts': posts,
												'tag':tag})


@login_required		# 需要登录
def user_list(request, tag_slug=None):
	'''显示当前登录用户的帖子，包括已发布和草稿'''
	object_list = Post.objects.filter(author=request.user).order_by('-publish')
	sums = Post.objects.filter(author=request.user).count()
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])
	paginator = Paginator(object_list,5) # 每个页面显示5条博客
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer diliver the first page
		posts = paginator.page(1)
	except EmptyPage:
		# if page is out of range deliver last page of results
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/user_list.html', {'sums': sums,
												'page':page,
												'posts': posts,
												'tag': tag})



def post_detail(request, year, month, day, post):
	'''帖子详细内容'''
	post = get_object_or_404(Post, slug=post, status='published',
						publish__year=year,
						publish__month=month,
						publish__day=day)
	comments = post.comments.filter(active=True)
	if request.method == 'POST':
		# A comment was posted
		comment_form = CommentForm(data=request.POST)
		new_comment = None
		if comment_form.is_valid():
			# 先不保存到数据库
			new_comment = comment_form.save(commit=False)
			# assign the current post to the comment
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = CommentForm()
	# 相似帖子
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
							.order_by('-same_tags','-publish')[:4]
	return render(request,'blog/post/detail.html',
									{'post':post,
									'comments':comments,
									'comment_form':comment_form,
									'similar_posts':similar_posts})


@login_required
def post_share(request, post_id):
	'''邮件分享'''
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False

	if request.method == 'POST':
		# 获取用户所填数据
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# 用户所填表单数据合法化
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = '阅读"{}"通过以下链接{}\n\n{}的建议{}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, '3533186315@qq.com', [cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post': post,
													'form': form,
													'sent': sent})


@login_required
def post_edit(request, post_id):
	'''编辑帖子'''
	post = Post.objects.get(id=post_id)
	edit_status = False
	if request.method != 'POST':
		form = PostForm(instance=post)
	else:
		form = PostForm(instance=post,data=request.POST)
		if form.is_valid():
			form.save()
			edit_status = True
	return render(request, 'blog/post/post_edit.html',
							{'post': post,
							'form': form,
							'edit_status': edit_status})


@login_required
def post_by_user(request):
	'''用户发帖'''
	status = False
	if request.method == "POST":
		form = UserPostForm(request.POST)
		new_form = None
		if form.is_valid():
			new_form = form.save(commit=False)
			new_form.author = request.user
			new_form.slug = new_form.title
			new_form.save()
			status = True
	else:
		form = UserPostForm()
	return render(request, 'blog/post/post_by_user.html',
								{'form': form,
								'status': status,
								})


@login_required
def post_delete(request, post_id):
	'''shangchu'''
	post = get_object_or_404(Post, id=post_id)
	post.delete()
	return HttpResponseRedirect(reverse('blog:user_list'))
