__author__ = 'valeriy'

from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='home'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<post_id>[0-9]+)/addlike/$', views.PostLikeToggle.as_view(), name='add_like'),
    url(r'^search/$', views.PostSearchListView.as_view(), name='post_search_list_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()