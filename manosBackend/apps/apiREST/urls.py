from django.conf.urls import url, include
from apps.apiREST import views


urlpatterns = [
	url(r'^users/$', views.user_list),
	url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
	url(r'^users/(?P<pk>[0-9]+)/address/$', views.addresses_list_by_user),

	url(r'^addresses/$', views.address_list),
	url(r'^addresses/(?P<pk>[0-9]+)/$', views.address_detail),

	url(r'^job_requests/$', views.job_request_list),
	url(r'^job_requests/(?P<pk>[0-9]+)/$', views.job_request_detail),
	url(r'^job_requests_cancel/(?P<pk>[0-9]+)/$', views.job_request_cancel),
	url(r'^users/(?P<pk>[0-9]+)/job_requests/$', views.job_requests_list_by_user),
	url(r'^job_request/(?P<pk>[0-9]+)/job_applications/$', views.job_applications_list_by_request),

	url(r'^job_applications/$', views.job_application_list),
	url(r'^job_applications/(?P<pk>[0-9]+)/$', views.job_application_detail),
	url(r'^job_choose/$', views.job_choose),

	url(r'^comments/$', views.comment_list),
	url(r'^comments/(?P<pk>[0-9]+)/$', views.comment_detail),
	url(r'^worker/(?P<pk>[0-9]+)/comments/$', views.comment_list_by_worker),
	

	url(r'^login/$', views.login)

]