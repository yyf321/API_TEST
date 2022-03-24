from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Myapp.models import *
import json
import requests


@login_required  #登录检查装饰符
def welcome(request):
    return render(request,'welcome.html')

@login_required  #登录检查装饰符
def caseList(request):
    return render(request,'caseList.html')

@login_required  #登录检查装饰符
def home(request):
    return render(request,'welcome.html',{"whichHTML": "home.html","oid": ""})

# 返回子页面
def child(request,eid,oid):
    # eid是要进入的html文件名
    res = child_json(eid,oid)
    return render(request,eid,res)

# 控制不同的页面返回不同的数据：数据分发器
def child_json(eid,oid=''):
    res = {}
    if eid == 'home.html':
        data = DB_home_herf.objects.all()
        res = {"hrefs":data}
    if eid == 'project_list.html':
        date = DB_project.objects.all()
        res = {"projects":date}
    if eid == 'P_apis.html':
        project = DB_project.objects.filter(id=oid)[0]
        apis = DB_apis.objects.filter(project_id=oid)
        res = {"project":project,"apis":apis}
    if eid == 'P_cases.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project":project}
    if eid == 'P_project_set.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project":project}

    return res


def login(request):
    return render(request,"login.html")

def login_action(request):
    username = request.GET["username"]
    password = request.GET["password"]
    print(username,password)

    from django.contrib import auth
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        request.session['user'] = username
        return HttpResponse("登陆成功！")
    else:
        return HttpResponse("登陆失败！")

def register_action(request):
    username = request.GET["username"]
    password = request.GET["password"]
    # 开始联通django用户表
    from django.contrib.auth.models import User
    try:
        user = User.objects.create_user(username=username,password=password)
        user.save()
        return HttpResponse("注册成功！")
    except:
        return HttpResponse("注册失败！自己想想为什么！")

def logout(request):
    from django.contrib import auth
    auth.logout(request)
    return HttpResponseRedirect('/login/') #重定向到登录页

def pei(request):
    tucao_text = request.GET["tucao_text"]
    DB_tucao.objects.create(user=request.user.username,text=tucao_text)
    return HttpResponse("")

def api_help(request):
    return render(request,'welcome.html',{"whichHTML": "help.html","oid": ""})

def project_list(request):
    return render(request,'welcome.html',{"whichHTML": "project_list.html","oid": ""})

def delete_project(request):
    id = request.GET['id']
    DB_project.objects.filter(id=id).delete()
    DB_apis.objects.filter(project_id=id).delete()
    return HttpResponse("删除成功！")

def add_project(request):
    print(request)
    project_name = request.GET['project_name']
    DB_project.objects.create(project_name=project_name,remark='',user_name=request.user.username,other_user='')
    return HttpResponse('')

# 进入接口库
def open_apis(request,id):
    project_id = id
    return render(request,'welcome.html',{"whichHTML": "P_apis.html","oid": project_id})

# 进入用例库
def open_cases(request,id):
    project_id = id
    return render(request,'welcome.html',{"whichHTML": "P_cases.html","oid": project_id})

# 进入项目设置
def open_project_set(request,id):
    project_id = id
    return render(request,'welcome.html',{"whichHTML": "P_project_set.html","oid": project_id})

# 保存项目设置
def save_project_set(request,id):
    project_id = id
    project_name = request.GET['project_name']
    remark = request.GET['remark']
    other_user = request.GET['other_user']
    DB_project.objects.filter(id=project_id).update(project_name=project_name,remark=remark,other_user=other_user)
    return HttpResponse('')

def project_api_add(request,id):
    project_id = id
    DB_apis.objects.create(project_id=project_id)
    return HttpResponseRedirect('/apis/%s'%project_id)

def project_api_del(request,id):
    project_id = DB_apis.objects.filter(id=id)[0].project_id
    DB_apis.objects.filter(id=id).delete()
    return HttpResponseRedirect('/apis/%s'%project_id)

def save_bz(request):
    api_id = request.GET['api_id']
    bz_value = request.GET['bz_value']
    DB_apis.objects.filter(id=api_id).update(des=bz_value)
    return HttpResponse("保存成功")

def get_bz(request):
    api_id = request.GET["api_id"]
    bz_value = DB_apis.objects.filter(id=api_id)[0].des
    return HttpResponse(bz_value)

def Api_save(request):
    # 提取所有数据
    api_id = request.GET['api_id']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    api_name = request.GET['api_name']
    ts_api_body = request.GET['ts_api_body']

    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body


    # 保存数据
    DB_apis.objects.filter(id=api_id).update(
        api_method = ts_method,
        api_url = ts_url,
        api_host = ts_host,
        api_header = ts_header,
        body_method = ts_body_method,
        api_body = ts_api_body,
        name = api_name,
    )
    return HttpResponse('success')

def get_api_data(request):
    api_id = request.GET['api_id']
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api),content_type='application/json')

def Api_send(request):
    # 提取所有数据
    api_id = request.GET['api_id']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    api_name = request.GET['api_name']
    ts_body_method = request.GET['ts_body_method']
    ts_api_body = request.GET['ts_api_body']
    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
        # 请求方式和请求体为空时可能是GET请求，参数在url里
        # if ts_body_method in ['',None]:
        #     return HttpResponse('请先选择好请求体编码格式和请求体，再点击Send按钮发送请求')
    else:
        ts_api_body = request.GET['ts_api_body']
        api = DB_apis.objects.filter(id=api_id)
        api.update(last_body_method=ts_body_method,last_api_body=ts_api_body)
    # 发送请求获取返回值
    #处理请求头
    header = json.loads(ts_header) # 从字符串转变为字典
    #处理url
    if ts_url[0] =="/" and ts_host[-1] =="/":  #都有"/"
        url = ts_host[:-1]+ts_url
    elif ts_url[0] !="/" and ts_host[-1] !="/":  #都没有"/"
        url = ts_host+"/"+ts_url
    else:  #只有一个"/"
        url = ts_host+ts_url
    #处理请求体编码方式
    if ts_body_method =="none":
        request = requests.request(ts_method.upper(),url,header=header,data={})
    elif ts_body_method =="form-data":
        files = [];
        body =








    # 把返回值传递给前端页面
    return HttpResponse('{"code":"200"}')