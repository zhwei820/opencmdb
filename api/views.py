#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015-06-09

@author: zw
'''

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from mydecorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
import json
from django.http import HttpResponse
import logging
import random
import traceback
import datetime
import json
import copy
from config import global_conf
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from util.fields_validation import _valid_fields, _fields_comment
from util.util import *

logger = logging.getLogger('default')


@login_required
def field_list(request):
    if request.method == 'GET':
        return JsonResponse({"field_list":_valid_fields, "fields_comment":_fields_comment}, safe = False)


@login_required
def current_user(request):
    if request.method == 'GET':
        return JsonResponse({"username":request.user.username, "realname":request.user.first_name + request.user.last_name}, safe = False)

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        res = handle_uploaded_file(request.FILES['file'])
        return JsonResponse({"url":res[0], "name":res[1]})
    else:
        return JsonResponse({"error":1}, status=status.HTTP_400_BAD_REQUEST)








import hmac, hashlib
import time, json

def create_signature(secret, *parts):
    hash = hmac.new(secret, digestmod=hashlib.sha1)
    for part in parts:
        hash.update(str(part))
    return hash.hexdigest()

@csrf_exempt
def get_auth_obj(request):
    user = request.user.username
    # 安装gateone的服务器以及端口.
    gateone_server = 'https://localhost:10443'
    # 之前生成的api_key 和secret 
    secret = b"OGZlMmFjNmFjNjQ1NGExOTk3MjVlNTA4YjViNWQ0YmEyZ"
    api_key = "YjQyY2ViZmNkODllNGRmNzg5YjUyNzA2YzA4MTkyN2U5N"


    authobj = {
        'api_key': api_key,
        'upn': "gateone",
        'timestamp': str(int(time.time() * 1000)),
        'signature_method': 'HMAC-SHA1',
        'api_version': '1.0'
    }
    my_hash = hmac.new(secret, digestmod=hashlib.sha1)
    my_hash.update((authobj['api_key'] + authobj['upn'] + authobj['timestamp']).encode("utf-8")) 

    authobj['signature'] = my_hash.hexdigest()
    auth_info_and_server = {"url": gateone_server, "auth": authobj}
    valid_json_auth_info = json.dumps(auth_info_and_server)
    #   print valid_json_auth_info
    return HttpResponse(valid_json_auth_info)