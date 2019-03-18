from django.conf.urls import include
from django.urls import re_path

from . import parent_view

urlpatterns = [
    re_path(r"^(?P<registry_code>\w+)/parent/?$",
            parent_view.ParentView.as_view(), name='parent_page'),
    re_path(r"^(?P<registry_code>\w+)/parent/(?P<parent_id>\d+)/?$",
            parent_view.ParentEditView.as_view(), name='parent_edit'),
    re_path(r'', include('rdrf.urls')),
]
