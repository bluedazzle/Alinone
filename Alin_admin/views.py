# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from AlinLog.models import AccountLog
from merchant_page.models import *
from CronOrder.Aaps import *
from CronOrder.ALO import *
import json
import time
import simplejson
import hashlib
import datetime


def login(request):
    if request.method == 'GET':
        return render_to_response('alin_admin/login.html',
                                  context_instance=RequestContext(request))