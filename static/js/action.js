$('#outputText').scroll( function() {
	scroll_1 = $('#inputText').scrollTop()
	scroll_2 = $('#outputText').scrollTop()
	if (scroll_1 != scroll_2) $('#inputText').scrollTop(scroll_2);
});

$('#inputText').scroll( function() {
	scroll_1 = $('#inputText').scrollTop()
	scroll_2 = $('#outputText').scrollTop()
	if (scroll_1 != scroll_2) $('#outputText').scrollTop(scroll_1);
});

$('#clearInputText').click(function () {
	$('#inputText').val('');
});

$('#copyInputText').click(function () {
	$('#inputText').select();
	document.execCommand('copy');
});

$('#copyOutputText').click(function () {
	var copytext = document.createElement('textarea');
    $(copytext).val($('#outputText').val());
	document.body.appendChild(copytext);
	copytext.select();
	document.execCommand('copy');
	document.body.removeChild(copytext);
});

$('#inputGroupSelectLanguageFrom').change(function() {
	value_from = $("#inputGroupSelectLanguageFrom").val();
	value_to = $("#inputGroupSelectLanguageTo").val();
	$("#inputGroupSelectLanguageTo").empty();
	if (dir_traslates[value_from].indexOf('ru') != -1) {
		$("#inputGroupSelectLanguageTo").append( $('<option value="ru">Русский</option>'));
	}
	if (dir_traslates[value_from].indexOf('en') != -1) {
		$("#inputGroupSelectLanguageTo").append( $('<option value="en">Английский</option>'));
	}
	$.each(langs_traslates, function(key, value) {
		if (key != 'ru' && key != 'en' && dir_traslates[value_from].indexOf(key) != -1) {
			$("#inputGroupSelectLanguageTo").append( $('<option value="' + key + '">' + value + '</option>'));
		}
	});
	$("#inputGroupSelectLanguageTo option[value=" + value_to + "]").attr("selected", "selected");
});

$('#downloadOutputText').click(function () {
	$('#hidden_download').val('true');
	$('#translate_btn').click();
	$('#hidden_download').val('false');
});

function getUploadFileName (str){
    if (str.lastIndexOf('\\')){
        var i = str.lastIndexOf('\\')+1;
    }
    else{
        var i = str.lastIndexOf('/')+1;
    }
    var filename = str.slice(i);
    $('#visible_file_name').val(filename);
}
