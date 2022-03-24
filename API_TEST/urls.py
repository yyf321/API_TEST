"""API_TEST URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url


from Myapp.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^welcome/', welcome),
    url(r'^caseList/', caseList),
    url(r'^home/', home),
    url(r"^child/(?P<eid>.+)/(?P<oid>.*)/$", child),  # 返回子页面
    url(r"^login/", login),
    url(r"^login_action/$", login_action),
    url(r"^register_action/$",register_action),
    url(r"^accounts/login/$", login), # 未登录都跳转至login页面
    url(r"^logout/$", logout),
    url(r"^pei/$", pei),#匿名吐槽
    url(r"^help/$", api_help),
    url(r"^project_list/$", project_list),
    url(r"^delete_project/$", delete_project),
    url(r"^add_project/$", add_project),
    url(r"^apis/(?P<id>.*)/$", open_apis),
    url(r"^cases/(?P<id>.*)/$", open_cases),
    url(r"^open_project_set/(?P<id>.*)/$", open_project_set),
    url(r"^save_project_set/(?P<id>.*)/$", save_project_set),
    url(r"^project_api_add/(?P<id>.*)/$", project_api_add),
    url(r"^project_api_del/(?P<id>.*)/$", project_api_del),
    url(r"^save_bz/$", save_bz),
    url(r"^get_bz/$", get_bz),
    url(r"^Api_save/$", Api_save),
    url(r"^get_api_data/$", get_api_data),
    url(r"^Api_send/$", Api_send),
    111
]
