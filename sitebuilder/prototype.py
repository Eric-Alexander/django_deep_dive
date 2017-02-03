
import os
import sys


from django.conf import settings

BASE_DIR = os.path.dirname(__file__)

settings.configure(
  DEBUG=True,
  SECRET_KEY='my_secret',
  ROOT_URLCONF='sitebuilder.urls',
  MIDDLEWARE_CLASSES=(),
  INSTALLED_APPS=(
    'django.contrib.staticfiles',
    'sitebuilder',
    #compresses static files AND provides LESS SASS compilation!
    'compressor',
  ),
  TEMPLATES=(
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS':True,
    },
),
  STATIC_URL='/static/',
  SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR, 'pages'),
  #these two commands will store generated content but
  #will not checked into version control!!!
  #based upon sitebuilder/management/commands/build.py
  SITE_OUTPUT_DIRECTORY=os.path.join(BASE_DIR, '_build'),
  STATIC_ROOT=os.path.join(BASE_DIR, '_build', 'static'),
  #files will get unique hash when DEBUG=False
  STATICFILES_STORAGE='django.contrib.staticfiles.storage.CachedStaticFilesStorage',
  STATICFILES_FINDERS=(
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
  )

)


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)