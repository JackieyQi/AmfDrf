#! /usr/bin/env python
# coding:utf8

import hashlib
from uuid import uuid4
from datetime import datetime


def generate_token(random_string, length=32):
	return (uuid4().hex + hashlib.sha256((str(datetime.now()) + str(random_string)).encode("utf8")).hexdigest())[:length].upper()
