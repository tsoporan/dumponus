from django.shortcuts import render_to_response, get_object_or_404
from upload.forms import UploadForm
from upload.models import Upload
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.template import defaultfilters
from django.contrib import messages

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
            upload.save()
            messages.success(request, "Upload was successful!")
            return HttpResponseRedirect(reverse('upload-detail', args=[upload.id]))
    else:
        form = UploadForm()

    return render_to_response('upload/index.html', {
        'form': form,  
        'latest': Upload.objects.order_by('-created')[:20],
    }, context_instance=RequestContext(request))

def upload_list(request):
    upload_list = Upload.objects.order_by('-created')
    paginator = Paginator(upload_list, 20)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        uploads = paginator.page(page)
    except (EmptyPage, InvalidPage):
        uploads = paginator.page(paginator.num_pages)

    return render_to_response('upload/list.html', {
        'uploads': uploads,
    }, context_instance=RequestContext(request))
    
def upload_detail(request, id):
    upload = get_object_or_404(Upload, id=id)
    return render_to_response('upload/detail.html', {
        'upload': upload,
    }, context_instance=RequestContext(request))
