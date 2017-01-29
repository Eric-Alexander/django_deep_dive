#Ultimately, Django is simply a Python frameworks that handles
#incoming HTTP requests and returning HTTP responses
####secondary tasks include rendering HTML, persisting session state,
####parsing form data etc...

import sys
#for URLs
from django.conf.urls import url
#for Views ->inspects HTTP reqs and queries and other data to send
#to templates
from django.http import HttpResponse



#typically in manage.py ONLY 10 lines
#in this breakdown scenario these settings must live here
#as any additional imports need this required
from django.conf import settings
settings.configure(
    DEBUG = True,
    SECRET_KEY = 'secret_key',
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
