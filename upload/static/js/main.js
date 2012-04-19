$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
		maxFileSize: 5000000, //4.7mb
		minFileSize: 1,
		acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
	});

	$('#fileupload').bind('fileuploadcompleted', function(e, data) {
	
		if (data.result) {
                    $.each(data.result, function(index, image){
                            
                            var html= '<li class="span2">' +
                            '<a href="/d/'+ image.id + '/">' +
                            '<img class="thumbnail" src="'+ image.thumbnail_url + '"></a>' +
                            '</li>'
                    
                            $(html).prependTo(".thumbnails").fadeIn("slow");
                    
                            // remove last image from thumbs
                            
                            if ($('.thumbnails').children().length >= 42) {
                                    $('.thumbnails li:last-child').remove();
                            }
                    });		
                    data.context.remove();
		}
                
	});
});
