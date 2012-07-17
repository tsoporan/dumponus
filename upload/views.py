import os
from upload.models import Image
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.utils import simplejson
from sorl.thumbnail import get_thumbnail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#passing to template because causes django template errors otherwise
js_tmpl = """
<!-- The template to display files available for upload -->
<script id="template-upload" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-upload fade">
        <td class="preview"><span class="fade"></span></td>
        <td class="name"><span>{%=file.name%}</span></td>
        <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
        {% if (file.error) { %}
            <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
        {% } else if (o.files.valid && !i) { %}
            <td>
                <div class="progress progress-success progress-striped active"><div class="bar" style="width:0%;"></div></div>
            </td>
            <td class="start">{% if (!o.options.autoUpload) { %}
                <button class="btn btn-primary">
                    <i class="icon-upload icon-white"></i>
                    <span>{%=locale.fileupload.start%}</span>
                </button>
            {% } %}</td>
        {% } else { %}
            <td colspan="2"></td>
        {% } %}
        <td class="cancel">{% if (!i) { %}
            <button class="btn btn-warning">
                <i class="icon-ban-circle icon-white"></i>
                <span>{%=locale.fileupload.cancel%}</span>
            </button>
        {% } %}</td>
    </tr>
{% } %}
</script>
<!-- The template to display files available for download -->
<script id="template-download" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-download fade">
        {% if (file.error) { %}
            <td></td>
            <td class="name"><span>{%=file.name%}</span></td>
            <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
            <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
        {% } else { %}
            <td class="preview">{% if (file.thumbnail_url) { %}
                <a href="{%=file.url%}" title="{%=file.name%}" rel="gallery" download="{%=file.name%}"><img src="{%=file.thumbnail_url%}"></a>
            {% } %}</td>
            <td class="name">
                <a href="{%=file.url%}" title="{%=file.name%}" rel="{%=file.thumbnail_url&&'gallery'%}" download="{%=file.name%}">{%=file.name%}</a>
            </td>
            <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
            <td colspan="2"></td>
        {% } %}
        <td class="delete">
            <button class="btn btn-danger" data-type="{%=file.delete_type%}" data-url="{%=file.delete_url%}">
                <i class="icon-trash icon-white"></i>
                <span>{%=locale.fileupload.destroy%}</span>
            </button>
        </td>
    </tr>
{% } %}
</script>

"""

def imgs_with_thumbs(image_qs, thumb_size='150x150', amount=None):
    if amount:
        image_qs = image_qs[:amount]

    return [
        (image, get_thumbnail(image.file, thumb_size, crop='center', quality=100)) for image in image_qs 
    ]

def upload(request):
   
    if request.method == 'POST':
        
        if not request.FILES:
            return HttpResponseBadRequest("No files were attached with request.")
        
        tmp = request.FILES["files[]"]

        fname, ext = os.path.splitext(tmp.name)

        if not ext:
            return HttpResponseBadRequest("All filenames must have an extension.")

        img = Image.objects.create(
            file = tmp,    
            ext = ext[1:], #strip period
            name = fname, 
        )

        thumb = get_thumbnail(img.file, "150x150", crop="center", quality=100)

        resp = simplejson.dumps([{
            'name': img.name,
            'size': img.file.size,
            'thumbnail_url': thumb.url,
            'url': img.file.url,
            'id': img.id,
            'ext': img.ext,
        },])

        return HttpResponse(resp, mimetype='application/json')

    amount = request.GET.get('a', 25)
    page   = request.GET.get('p', 1)
    
    images_thumbs = imgs_with_thumbs(Image.objects.order_by('-created'))
 
    paginator = Paginator(images_thumbs, amount)
    
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage: #out of range, give last results
        images = paginator.page(paginator.num_pages)

    return render(request, 'upload.html', {
        'js_tmpl': js_tmpl,
        'images': images, 
        'amount': amount,
        'page': page,
    })

def detail(request, id, ext=None):

    image = get_object_or_404(Image, id=id)

    if ext:
        if image.ext != ext: 
            raise Http404
        return HttpResponse(image.file, mimetype = 'image/' + ext)

    return render(request, 'detail.html', {'image': image})
