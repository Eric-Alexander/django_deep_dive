# WSGI (Web Server Gateway Interface) is the spec for how web servers
#communicate with application frameworks [like Django] defined by PEP 3333
# examples include Gunircorn, Tornado Apache

#there is a baked-in Django function to set this up: get_wsgi_application
# in this example, I have installed gunicorn and applied function at bottom
# from the command line: gunicorn <filename> --log-file=-

import os
import sys
#for URLs
from django.conf.urls import url
#for Views
from django.http import HttpResponse

#for WSGI (normally in wsgi.py)
from django.core.wsgi import get_wsgi_application


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


# more WSGI setup
#VAR MUST BE TITLED application

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
