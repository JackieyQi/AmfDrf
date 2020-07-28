#! /usr/bin/env python
# coding:utf8

from rest_framework.permissions import IsAuthenticated

from utils.views import TriDrfApiView


class YqApiView(TriDrfApiView):
	permission_classes = (IsAuthenticated,)

	http_method_names = ("get", "post", "put")

	def get(self, request):
		return "test"

	def post(self, request):
		return

	def put(self, request):
		return

	def delete(self):
		return
