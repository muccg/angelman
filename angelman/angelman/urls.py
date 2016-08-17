from django.conf.urls import patterns, url, include

import parent_view
import patient_view

urlpatterns = patterns('',
                       url(r"^(?P<registry_code>\w+)/parent/?$",
                           parent_view.ParentView.as_view(), name='parent_page'),

                       url(r"^(?P<registry_code>\w+)/parent/(?P<parent_id>\d+)/?$",
                           parent_view.ParentEditView.as_view(), name='parent_edit'))

#                       url(r"^(?P<registry_code>\w+)/patient/?$",
#                           patient_view.PatientView.as_view(), name='patient_page'))

urlpatterns += patterns('',
                        url(r'', include('rdrf.urls')),
                        )
