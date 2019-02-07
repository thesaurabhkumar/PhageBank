from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from PhageBank.core import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Uncomment the next line to enable the admin:
    # url(r'^$', core_views.new_index, name='index'),
    url(r'^$', core_views.logged_in_index, name='index'),
    url(r'^add_phage/', core_views.add_phage, name='add_phage'),
    url(r'^admin/', admin.site.urls),
    url(r'^delete_all/$', core_views.delele_all_phages, name='delete_all'),
    url(r'^mylogin/$', core_views.mylogin, name='mylogin'),
    url(r'^logout/$', core_views.mylogout, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^change_password/$', core_views.change_password, name='change_password'),
    url(r'^view_phages/$', core_views.view_phages, name='view_phages'),
    url(r'^view_phage/$', core_views.view_phage, name='phage'),
    url(r'^search_phage/$', core_views.search_phage, name='search_phage'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^uploads/form/$', core_views.model_form_upload, name='model_form_upload'),
    url(r'^edit_details/$', core_views.editPhage, name='edit_details'),
    url(r'^delete/$', core_views.deletephages, name='view'),
    url(r'^my_phages/$', core_views.my_phages, name='my_phages'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
