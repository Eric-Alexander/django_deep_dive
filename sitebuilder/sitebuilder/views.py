import os

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template
from django.utils._os import safe_join

def get_page_or_404(name):
  #return content as Django template or raire 404
  try:
    #safe_join returns an absolute version of final path
    file_path = safe_join(settings.SITE_PAGES_DIRECTORY, name)
  except ValueError:
    raise Http404('Page not found.')
  else:
    if not os.path.exists(file_path):
      raise Http404('Page not found, either.')
  #open each file and creates new template obj w/ contents
  with open(file_path, 'r') as f:
    page = Template(f.read())

  return page

def page(request, slug='index'):
  #if page is found....render it!
  file_name = '{}.html'.format(slug)
  page = get_page_or_404(file_name)
  context = {
    'slug': slug,
    'page': page,
  }
  #pass context to be rendered into layout
  return render(request, 'page.html', context)