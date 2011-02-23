from PIL import Image
import cStringIO
from django.core.files.base import ContentFile
import random
import os

def randoName(dobj, name):
  '''Takes a name and datetime object and returns a random string.'''
  n, ext = os.path.splitext(name)
  n_ = sum([ord(x) for x in n])
  t = 0
  for i in [['year',1], ['month',12], ['day',31],['hour',24],['minute',60],['second',60]]:
    t = t*i[1]+getattr(dobj,i[0]) * n_
  return hex(t)[2:-1] + ext

def randThumbSize(min_size, max_size):
  '''Returns a random thumbnail size as a tuple.'''
  try:
    x = random.randrange(min_size[0], max_size[0])
    y = random.randrange(min_size[1], max_size[1])
  except Exception:
    raise TypeError('Are you sure min_size and max_size are container types?')
  else:
    return x,y

def generateThumb(img, size, format):
  '''
  Makes a thumbnail and returns the "file" like contents.
        
  img - a file-like object
  size - a tuple with the desired thumbnail size
  format - image format e.g PNG, JPG, GIF
  '''
  
  assert isinstance(size, tuple), "Size must be a tuple in the form (xxx,xxx)"
  img.seek(0)
  image = Image.open(img)

  
  if image.mode not in ('L', 'RGB'):
    image.convert('RGB')
  
  image.thumbnail(size, Image.ANTIALIAS)

  if format.upper() == 'JPG':
    format = 'JPEG'

  sio = cStringIO.StringIO()

  image.save(sio, format)
  return ContentFile(sio.getvalue())
        
def getTags(tags):
  '''Takes a tag QuerySet returns a "sorted" dict'''
  d = {}
  for t in tags:
    d[t.name] = t.count, t.get_absolute_url()
  
  #return sorted(d.items(), key=lambda (k,v): (v,k), reverse=True)
  return d.items()

def genCloud(taglist):
  '''Generates tag cloud.'''
  li = []
  for tag in taglist:   
    cnt = tag[1][0]
    if cnt == 1:
      cls = 'xxs'
    elif cnt > 1 and cnt <= 5:
      cls = 'xs'
    elif cnt > 5 and cnt <= 10:
      cls = 's'
    elif cnt > 10 and cnt <= 15:
      cls = 'n'
    elif cnt > 15 and cnt <= 20:
      cls = 'l'
    elif cnt > 20 and cnt <= 25:
      cls = 'xl'
    elif cnt > 25 and cnt <= 30:
      cls = 'xxl'
    li.append('<li class="%s"><a href="%s" rel="tag">%s</a></li>' % (cls, tag[1][1].replace(' ', '-').lower(), tag[0]))
  return li
