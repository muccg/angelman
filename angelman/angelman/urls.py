from django.conf.urls import url, include

from . import parent_view

urlpatterns = [
    url(r"^(?P<registry_code>\w+)/parent/?$",
        parent_view.ParentView.as_view(), name='parent_page'),
    url(r"^(?P<registry_code>\w+)/parent/(?P<parent_id>\d+)/?$",
        parent_view.ParentEditView.as_view(), name='parent_edit'),
    url(r'', include('rdrf.urls')),
]
