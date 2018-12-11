from django.conf.urls import url, include

from . import parent_view
from . import caregiver_review_view

urlpatterns = [
    url(r"^(?P<registry_code>\w+)/parent/?$",
        parent_view.ParentView.as_view(), name='parent_page'),
    url(r"^(?P<registry_code>\w+)/parent/(?P<parent_id>\d+)/?$",
        parent_view.ParentEditView.as_view(), name='parent_edit'),
    url(r"^(?P<registry_code>\w+)/cgreview/(?P<patient_id>\d+)/?$",
        caregiver_review_view.CaregiverReviewView.as_view(),name='caregiver_review'),
    url(r'', include('rdrf.urls')),
]
