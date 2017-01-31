import hashlib
import os
import sys


#converts content to bytes
from io import BytesIO
#PIL is Pillow, a python image manipulation module
#Image generates a new image, ImageDraw allows text to be written over image.
from PIL import Image, ImageDraw

from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY',
    '%jv_4#hoaqwih3hu!eg#^ozptd*a@88u(aasv7z!7xt^5(*i&k')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

BASE_DIR = os.path.dirname(__file__)

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    #add this line for {% static %} tag to be available
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
    ),
    TEMPLATES=(
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': (os.path.join(BASE_DIR, 'templates'), ),
        },
    ),
    STATICFILES_DIRS=(
        os.path.join(BASE_DIR, 'static'),
    ),
    STATIC_URL='/static/',
)
#typically Django Forms are used to validate POST and GET
#However, they can also be used for validating URL values
from django import forms
from django.conf.urls import url
#to cache client-side URLs to save CPU
from django.core.cache import cache
from django.core.urlresolvers import reverse
#Web Server Gate Interface    using Gunicorn
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
#HTTP ETag is the response header of a protocol cycle
from django.views.decorators.http import etag

#Validate the placeholder URL for image size
class ImageForm(forms.Form):
    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    #creating an image with Pillow requires 2 args:
        #color mode
        #size as a tuple
        #optional 3rd arg: sets color (default = black)
    def picgen(self, image_format='PNG'):
        #clean the data (convert from string to integer)
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        key = '{}.{}.{}'.format(width, height, image_format)
        #to impede unecessay requests to the server use cache
        #this will exchange memory use to store cached variables (height, width)
        #while saving CPU cycles required to generate images
        content = cache.get(key)
        #before a new image is created the cache will check to see
        #if it's already stored
        if content is None:
            #new img is constructed with Pillow's Image class
            image = Image.new('RGB', (width, height))
            #use ImageDraw to throw height X width variables atop of image for ref
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
        #if text can fit into the image....
        if textwidth < width and textheight < height:
            texttop = (height - textheight) // 2
            textleft = (width - textwidth) // 2
            draw.text((textleft, texttop), text, fill=(255,0,0))
        #set the image content to bytes
        content = BytesIO()
        #save image, converted to bits, in PNG format
        image.save(content, image_format)
        #selects the pointer and brings it back to index(0)
        content.seek(0)
        #When cache is missed and new image is created, this saves cached image
        #for up to one hour.
        cache.set(key, content, 60*60)
        return content



#takes same arguments as the placeholder view
def generate_etag(request, width, height):
    content = 'Placeholder: {0} x {1}'.format(width, height)
    #hashlob returns an ETag based on w and h values
    return hashlib.sha1(content.encode('utf-8')).hexdigest()

#With this decorator the server will only need to generate the image the
#first time after the broswer requests it (for up to an hour, in this case)
#Using the decorator has an advantage over Middleware ETag because the latter
#uses md5 hashing which would be computed in the view...which takes more time
#whereas this decorator calculates the ETag prior to calling the view!
@etag(generate_etag)


#we must add validation to the form to send an error message if the form values
#are invalid
def placeholder(req, width, height):
    #store values from form into variable
    form = ImageForm({'height': height, 'width': width})
    #conditonal statement to check validity of variable 'form'
    if form.is_valid():
        #call picgen() to clean, convert and create a png image
        #after data is cleaned URL has 2 values between 1-2000
        image = form.picgen()
        return HttpResponse(image, content_type='image/png')
    #if the form is not valid send an error message
    else:
    #HttpResponseBadRequest is a subclass of HttpResponse -> sends a 400
        return HttpResponseBadRequest("Invalid request, number values must be less than 2001.")


def index(request):
    #updated index view builds example URL by reversing placeholder view
    #passes it to template context
    example = reverse('placeholder', kwargs={'width': 666, 'height': 222})
    context = {
    'example': request.build_absolute_uri(example)
    }
    return render(request, 'home.html', context)

urlpatterns = (
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder,
    name="placeholder"),
    url(r'^$', index, name='homepage'),
)


application = get_wsgi_application()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
