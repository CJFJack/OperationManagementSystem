# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


class LoginView(generic.View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.POST.get('next', '/') or '/')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html', {})
