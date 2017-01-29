#setting up different django development environments breakdown

#using the https://12factor.net/ 12 Factor App philosophy

#The goal is to build for minimal differences between environments
# Only two settings are to be changed between environments: DEBUG and SECRET_KEY


import os
import sys
#for URLs
from django.conf.urls import url
#for Views
from django.http import HttpResponse


from django.conf import settings


#DEBUG will change between envirnoments, set the default to be true
DEBUG = os.environ.get('DEBUG', 'on') == 'on'

#SECRET_KEY to be generated randomly every application load if not set
#Good for practice but not ideal for prod as it uses
#signed cookies (which, in this case, would be frequently invalidated)
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))

#When DEBUG = False an error arises declaring to set setting.ALLOWED_HOSTS
# For validating incoming HTTP HOST header values and set to a list of
# acceptable values. If not set it will allow requests ONLY FROM LOCALHOST

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
    DEBUG = DEBUG,
    SECRET_KEY = SECRET_KEY,
    #add ALLOWED_HOSTS to settings here
    ALLOWED_HOSTS = ALLOWED_HOSTS,
    ROOT_URLCONF = __name__,
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

#Root View - typically in views.py (although can be named anything)
def index(request):
    return HttpResponse('Hello Eric')

#pair a View to a URL with regex! (conventionally in urls.py)
urlpatterns = (
    url(r'^$', index),
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
