from django.conf.urls import include
from django.urls import re_path

from . import parent_view
#from two_factor import views as twv
#from rdrf.auth.views import QRGeneratorView, SetupView, DisableView

#two_factor_auth_urls = [
#    re_path(r'^account/login/?$',twv.LoginView.as_view(),name='login'),
#    re_path(r'^account/two_factor/setup/?$', SetupView.as_view(), name='setup'),
#    re_path(r'^account/two_factor/qrcode/?$', QRGeneratorView.as_view(), name='qr'),
#    re_path(r'^account/two_factor/setup/complete/?$', twv.SetupCompleteView.as_view(),
#        name='setup_complete'),
    #    We're not using a few of these urls currently
    #
    #    url(
    #        regex=r'^account/two_factor/backup/tokens/?$',
    #        view=twv.BackupTokensView.as_view(),
    #        name='backup_tokens',
    #    ),
    #    url(
    #        regex=r'^account/two_factor/backup/phone/register/?$',
    #        view=twv.PhoneSetupView.as_view(),
    #        name='phone_create',
    #    ),
    #    url(
    #        regex=r'^account/two_factor/backup/phone/unregister/(?P<pk>\d+)/?$',
    #        view=twv.PhoneDeleteView.as_view(),
    #        name='phone_delete',
    #    ),
    #    url(
    #        regex=r'^account/two_factor/?$',
    #        view=twv.ProfileView.as_view(),
    #        name='profile',
    #    ),
#    re_path(r'^account/two_factor/disable/?$', DisableView.as_view(), name='disable'),
#]



urlpatterns = [
    re_path(r"^(?P<registry_code>\w+)/parent/?$",
        parent_view.ParentView.as_view(), name='parent_page'),
    re_path(r"^(?P<registry_code>\w+)/parent/(?P<parent_id>\d+)/?$",
        parent_view.ParentEditView.as_view(), name='parent_edit'),
    re_path(r'', include('rdrf.urls')),
]
