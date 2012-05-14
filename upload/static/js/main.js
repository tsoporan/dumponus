$.urlParam = function(name) {
		var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);
		if (!results) {
			return 0;
		}
		return results[1] || 0;
	}

$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
		maxFileSize: 5000000, //4.7mb
		minFileSize: 1,
		acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
	});

	var amount = $.urlParam('a') > 0 ? $.urlParam('a') : 25;

	$('#fileupload').bind('fileuploadcompleted', function(e, data) {
	
		if (data.result) {
                    $.each(data.result, function(index, image){
                            
                            var html= '<li class="span2">' +
                            '<a href="/'+ image.id + '/">' +
                            '<img class="thumbnail" src="'+ image.thumbnail_url + '"></a>' +
                            '</li>'
                    
                            $(html).prependTo(".thumbnails").fadeIn("slow");
                    
                            // remove last image from thumbs
                            
                            if ($('.thumbnails').children().length >= amount) {
                                    $('.thumbnails li:last-child').remove();
                            }
                    });		
                    data.context.remove();
		}
                
	});
});
