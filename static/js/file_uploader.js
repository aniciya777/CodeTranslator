+ function($) {
    'use strict';

    // UPLOAD CLASS DEFINITION
    // ======================

    var dropZone = document.getElementById('drop-zone');
    var uploadForm = document.getElementById('js-upload-form');

    var startUpload = function(files) {
        $('#hidden_file_name').val(files[0].name);
        document.getElementById('js-upload-files').files = files;
        $('#translate_btn').click();
    };

    // uploadForm.addEventListener('submit', function(e) {
    //     var uploadFiles = document.getElementById('js-upload-files').files;
    //     if (uploadFiles.length > 0) {
    //         e.preventDefault();
    //
    //         startUpload(uploadFiles)
    //     }
    // });

    dropZone.ondrop = function(e) {
        e.preventDefault();
        this.className = 'upload-drop-zone';

        startUpload(e.dataTransfer.files)
    };

    dropZone.ondragover = function() {
        this.className = 'upload-drop-zone drop';
        return false;
    };

    dropZone.ondragleave = function() {
        this.className = 'upload-drop-zone';
        return false;
    };

}(jQuery);