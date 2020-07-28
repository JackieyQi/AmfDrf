#! /usr/bin/env python
# coding:utf8

from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView, set_rollback
from rest_framework.exceptions import APIException, NotAuthenticated, AuthenticationFailed, Throttled

from .resp_code import SUCCESS
from .exception import UnAuthorizationExc


class TriDrfApiView(APIView):
	def initial(self, request, *args, **kwargs):
		if request.path.startswith("/api"):
			request._SET_COOKIE = False
			request._DEL_COOKIE = False
			"""
			Make decrypt for each request view here.
			"""
		return super(TriDrfApiView, self).initial(request, *args, **kwargs)

	def finalize_response(self, request, response, *args, **kwargs):
		if not response:
			response = ""

		if isinstance(response, (dict, list, str)):
			response = Response({
				"code": SUCCESS, "message": "", "data": response
			})

		if request._SET_COOKIE:
			response.set_cookie("AUTHORIZATION", "Token {}".format(request._SET_COOKIE), max_age=86400 * 7)
		elif request._DEL_COOKIE:
			response.delete_cookie("AUTHORIZATION")
		return super(TriDrfApiView, self).finalize_response(request, response, *args, **kwargs)

	def handle_exception(self, exc):
		set_rollback()

		response = None
		if isinstance(exc, UnAuthorizationExc):
			response = Response({
				"code": exc.code, "message": exc.message,
			})
			response.delete_cookie("AUTHORIZATION")
		elif isinstance(exc, NotAuthenticated):
			response = Response({"code": exc.default_code, "message": exc.detail}, exception=True)
		elif isinstance(exc, AuthenticationFailed):
			response = Response({"code": exc.default_code, "message": exc.detail}, exception=True)
		elif isinstance(exc, Throttled):
			response = Response({"code": exc.default_code, "message": exc.detail}, exception=True)
		elif isinstance(exc, APIException):
			response = Response({"code": exc.default_code, "message": exc.detail}, exception=True)
		elif isinstance(exc, Http404):
			response = Response({"code": 404, "message": "404 Not Found"}, status=404, exception=True)
		elif isinstance(exc, PermissionDenied):
			response = Response({"code": 403, "message": "403 Forbidden"}, status=403, exception=True)

		if not response:
			self.raise_uncaught_exception(exc)
		else:
			exc.__traceback__ = None
			return response
