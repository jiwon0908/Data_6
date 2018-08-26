# 비밀키
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '빅데이터고려대학교6조'