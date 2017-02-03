#script for custom management command
#in this example the script command will generate and
#output the static site!

import os

import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.test.client import Client


def get_pages():
  for name in os.listdir(settings.SITE_PAGES_DIRECTORY):
    #loop thru dir -> collect all .html files
    if name.endswith('.html'):
      yield name[:-5]

class Command(BaseCommand):
  help = "Build static site output."

  def handle(self, *args, **options):
    """Request pages, generate content, output content"""
    #check is there is one or more args passed into command
    if args:
      pages = args
      available = list(get_pages())
      invalid = []
      for page in pages:
        if page not in available:
          invalid.append(page)
      if invalid:
        msg = "Invalid pages: {}".format(', '.join(invalid))
        raise CommandError(msg)
    else:
      #if directory exists, wipe clean
      if os.path.exists(settings.SITE_OUTPUT_DIRECTORY):
        shutil.rmtree(settings.SITE_OUTPUT_DIRECTORY)
      os.mkdir(settings.SITE_OUTPUT_DIRECTORY)
      os.makedirs(settings.STATIC_ROOT)
    #copy all static resources into STATIC_ROOT dir
    call_command('collectstatic', interactive=False,
        clear=True, verbosity=0)
    client = Client()
    for page in pages:
      #grabs all .html resources
      url = reverse('page', kwargs={'slug': page})
      response = client.get(url)
      if page == 'index':
        output_dir = settings.SITE_OUTPUT_DIRECTORY
      else:
        output_dir = os.path.join(settings.SITE_OUTPUT_DIRECTORY, page)
        if not os.path.exists(output_dir):
          os.makedirs(output_dir)
      #crawl thru .html pages and write content into
      #SITE_OUTPUT_DIRECTORY
      with open(os.path.join(output_dir, 'index.html'), 'wb') as f:
        f.write(response.content)


#to activiate cd _build
#python -m SimpleHTTPServer 9000

#this will easily deploy hosting files to any hosting platform
#for showing rapid prototype progress.

#updated to build out single pages by kwarg
#ex: python prototype.py build index