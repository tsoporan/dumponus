import os, sys
import site

proj_name = 'dumponus'

#Find the root directory based on this files location.
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

#Adds dir to python path and processes any .pth files it finds.
site.addsitedir(os.path.join(root_dir, 'lib/python2.6/site-packages'))

#Add root dir of env and project to path
sys.path.insert(0, root_dir)
sys.path.insert(0, os.path.join(root_dir, proj_name))

#Point django to the projects setting file
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

