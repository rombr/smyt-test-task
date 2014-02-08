jQuery(function($){
	$(document).ajaxSend(function (event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
        }
    
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
    
    $.datepicker.setDefaults({
		dateFormat: 'yy-mm-dd',
		changeMonth: true,
		changeYear: true,
		yearRange: '1900:+10'
	});
	
	var modelName = '';
	var modelKeys;
	var modelTypes;
	
	$(document).ready(function () {
		function renderData(modelName){
			$.getJSON('/api/'+ modelName + '/', function( data ) {
				// Data head
				modelKeys = [];
				modelTypes = {};
				var head_items = ['<th class="data-id">ID</th>'];
				$.each( data.schema.fields, function( ind, field ) {
					head_items.push( '<th class="data-' + field.id + '">' + field.title + '</th>' );
					modelKeys.push(field.id);
					modelTypes[field.id] = field.type;
				});
				$('#data thead').html(head_items.join(''));
				
				// Data content
				$("#data tbody").html('');
				$.each( data.data, function( ind, field ) {
					var items = ['<td class="data-id">' + field.id + '</td>'];
					$.each( modelKeys, function( ind, key ) {
						items.push( '<td data-field="' + key + '" class="editable data-' + key + '">' + field[key] + '</td>' );
					});
					$( "<tr/>", {
						html: items.join( "" )
					}).appendTo( "#data tbody" );
				});
				
				// Add form
				var form_items = [];
				$.each( data.schema.fields, function( ind, field ) {
					form_items.push(
						'<p>' +
							'<label for="add-' + modelName + '-' + field.id + '">' + field.title + '</label>' +
							'&nbsp;' +
							'<input name="' + field.id + '" id="add-' + modelName + '-' + field.id + '" type="text" value="" class="' + modelTypes[field.id] + '"/>' +
						'</p>' 
					);
				});
				
				$('#add-form').html(
					'<h4> Add new <strong>' + data.schema.title + '</strong></h4>' +
					'<form class="add-' + modelName + '-form" action="/api/' + modelName + '/" method="post">' +
						form_items.join( "" ) +
						'<p><input type="submit" value="Add"/></p>' +
					'</form>'
				);
				$( "#add-form input.date" ).datepicker();
			});
		};
		
		function validate(input){
			var type = modelTypes[$(input).attr('name')];
			var value =$(input).val();
			switch (type){
			case 'char':
			  return (/^.{1,512}$/.test(value));
			  break;
			case 'int':
			  return (/^[\-0-9]+$/.test(value));
			  break;
			case 'date':
			  return (/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/.test(value));
			  break;
			};
			return true;
		};
		
		function updateObject(input){
			var field = $(input).parent();
			var fieldName = $(field).attr('data-field');
			var value = $(input).val();
			var oldValue = $(field).attr('data-old-value');
			var id = $(field).parent().find('td.data-id').text();
			
			if (value == oldValue){
				$(field).html(value);
			} else {
				if (!validate(input)){
					$(input).addClass('error');
				} else {
					var params = {};
					params[fieldName] = value;
					$.post( '/api/' + modelName + '/' + id + '/', params, function( data ) {
						$(field).html(value);
					});
				};
			};
		};
		
		$('.m-select').on('click', function(){
			$('.m-select').removeClass('bold');
			$(this).addClass('bold');
			
			newModelName = $(this).attr('href').slice(1);
			if (newModelName != modelName){
				modelName = newModelName;
				renderData(modelName);
			};
		});
		
		$('#data td.editable').live('click', function(){
			if ($('input', this).length <= 0){
				var fieldName = $(this).attr('data-field');
				var fieldValue = $(this).text();
				$(this).attr('data-old-value', fieldValue);
				$(this).html('<input name="' + fieldName + '" class="edit ' + modelTypes[fieldName] + '" value="' + fieldValue + '" type="text"/>');
				
				$( "input.edit.date" ).datepicker({
					onClose: function(dateText, inst){
						updateObject(inst.input);
					}
				});
				$('input.edit', this).focus();
			};
		});
		
		$('input.edit.char, input.edit.int').live('blur', function(){
			updateObject(this);
		});
		
		$('#add-form form').live('submit', function(){
			var form = this;
			
			var errorCount = 0;
			$('input[type!=submit]', form).each(function(ind, elem){
				if (!validate(elem)){
					errorCount++;
					$(elem).addClass('error');
				} else {
					$(elem).removeClass('error');
				};
			});
			if (errorCount){
				return false;
			};
			
			$.post( $(this).attr('action'), $(this).serialize(), function( res ) {
				// Add data content
				var items = ['<td class="data-id">' + res.data.id + '</td>'];
				$.each( modelKeys, function( ind, key ) {
					items.push( '<td data-field="' + key + '" class="editable data-' + key + '">' + res.data[key] + '</td>' );
				});
				$( "<tr/>", {
					html: items.join( "" )
				}).appendTo( "#data tbody" );
				// Clean form
				$('input[type!=submit]', form).val('');
				$('input[type!=submit]:first', form).focus();
			});
			
			return false;
		});
	});
});