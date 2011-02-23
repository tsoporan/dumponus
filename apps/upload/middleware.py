import sys
try:
    import cProfile as profile
except ImportError:
    import profile
from cStringIO import StringIO
from django.conf import settings
#import tempfile
#import hotshot
#import hotshot.stats

class ProfilerMiddleware(object):
#    def process_request(self, request):
#    	if settings.DEBUG and request.GET.has_key('prof'):
#	    self.tmpfile = tempfile.NamedTemporaryFile()
#	    self.prof = hotshot.Profile(self.tmpfile.name)

    def process_view(self, request, callback, callback_args, callback_kwargs):		
    	if settings.DEBUG and request.GET.has_key('prof'):
    	    self.profiler = profile.Profile()
	    args = (request,) + callback_args
	    return self.profiler.runcall(callback, *args, **callback_kwargs)
	    #return self.prof.runcall(callback, request, *callback_args, **callback_kwargs)

    def process_response(self, request, response):
	if settings.DEBUG and request.GET.has_key('prof'):
	    #self.prof.close()

	    self.profiler.create_stats()

	    out = StringIO()
	    old_stdout, sys.stdout = sys.stdout, out

#	    stats = hotshot.stats.load(self.tmpfile.name)
#	    stats.sort_stats('time', 'calls')
#	    stats.print_stats()

	    self.profiler.print_stats(1)
	    sys.stdout = old_stdout

	    stats_str = out.getvalue()

	    if response and response.content and stats_str:
	    	response.content = '<pre>%s</pre>' % stats_str
		
	return response
