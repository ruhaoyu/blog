from django.conf.urls import url,include
from haystack.views import SearchView
from . import views
from .feeds import LatestPostsFeed


urlpatterns = [
        # 所有用户帖子
	url(r'^$', views.post_list_index, name='post_list'),
	# 分享帖子
	url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
	# 直接调用django用PostListView方法
	#url(r'^$', views.PostListView.as_view(), name='post_list'),
	# 根据帖子的日期作为帖子详情的url
	url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
		r'(?P<post>[-\w]+)/$', views.post_detail, name='post_detail'),
	# 首页相同标签帖子
	url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list_index, name='post_list_by_tag'),
	# 个人中心页面相同标签帖子
	url(r'^personal_tag/(?P<tag_slug>[-\w]+)/$', views.user_list, name='user_list_by_tag'),
	url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
	# 编辑帖子
	url(r'^(?P<post_id>\d+)/edit/$', views.post_edit, name='post_edit'),
	# 个人中心页面
	url(r'^user/$', views.user_list, name='user_list'),
	# 发布帖子
	url(r'^post/$', views.post_by_user, name='post_by_user'),
	url(r'^(?P<post_id>\d+)/delete/$', views.post_delete, name='post_delete'),
	url(r'^user_home/$', views.user_home, name='user_home'),
]
