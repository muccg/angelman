from django.conf.urls import include
from django.urls import re_path

from . import parent_view
from . import caregiver_review_view

urlpatterns = [
    re_path(r"^(?P<registry_code>\w+)/parent/?$",
            parent_view.ParentView.as_view(), name='parent_page'),
    re_path(r"^(?P<registry_code>\w+)/parent/(?P<parent_id>\d+)/?$",
            parent_view.ParentEditView.as_view(), name='parent_edit'),
    re_path(r"^(?P<registry_code>\w+)/cgreview/(?P<patient_id>\d+)/?$",
        caregiver_review_view.CaregiverReviewView.as_view(),name='caregiver_review'),
    re_path(r'', include(r'', include('rdrf.urls')),
]
