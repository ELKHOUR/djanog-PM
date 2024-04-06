from django.shortcuts import render
from django.contrib.auth.views import LogoutView
# Create your views here.


class LogoutViewWithGet(LogoutView):

    http_method_names = LogoutView.http_method_names + ['get']

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)