/**
 * Object to handle parts of the activity form
 */
const activityForm = {
    submitButtonText: '',
    imageUploadType: ['image/jpeg'],
    maxUploadImageSize: (4 * 1024 * 1024),
    checkFieldsEmpty: [
        {id: 'title', error: 'Field must be at least 4 characters long.'},
        {id: 'shortDescr', error: 'Field must be at least 4 characters long.'},
        {id: 'longDescr', error: 'Field must be at least 4 characters long.'},
        {id: 'category', error: 'At least one must be selected.'},
        {id: 'whenTodo', error: 'At least one must be selected.'}
    ],

    clearFieldError:(formFieldID) => {
        $('#' + formFieldID + '--error').addClass('d-none');
        $('#' + formFieldID).removeClass('is-invalid');
    },

    showFlashMessage: (message) => {
        // Remove any current flash message and display new message
        $('#flash--message').empty();
        $('#flash--message').prepend('<div class="flash__message-error">' + message + '</div>');
    },

    showFieldError: (formFieldID, errorMessage) => {
        // remove previous error message
        activityForm.clearFieldError(formFieldID);
        // show new error message
        $('#btn--form-update').text(activityForm.submitButtonText);
        $('#' + formFieldID + '--error').html('<span>' + errorMessage + '</span>');
        $('#' + formFieldID + '--error').removeClass('d-none');
        $('#' + formFieldID).addClass('is-invalid');
        $('#' + formFieldID).focus();
    },

    validateEmptyField: (formFieldID, errorMessage=' field error.') => {
        fieldValue = $('#' + formFieldID).val();
        if (fieldValue == '') {
            activityForm.showFieldError(formFieldID, errorMessage)
            return true;
        } else { return false; }
    },

    validateFileInput: (formFieldID, fileSize, fileType) => {
        let fileError = false;
        // clear existing file error and flash message
        activityForm.clearFieldError(formFieldID);
        $('#flash--message').empty();
        
        if (fileSize > activityForm.maxUploadImageSize) {
            let errorMessage = 'The selected file exceeds the upload file size limit';
            activityForm.showFieldError(formFieldID, errorMessage);
            fileError = true;
        } else if (!activityForm.imageUploadType.includes(fileType)) {
            let errorMessage = 'Incorrect image format, please use Jpeg';
            activityForm.showFieldError(formFieldID, errorMessage);
            fileError = true;
        }
        if (fileError) {
            activityForm.showFlashMessage('Please correct form errors below');
        }
    },

    checkForm: () => {
        console.log('JS validate form?');
        formError = false;
        activityForm.checkFieldsEmpty.forEach( (formField) => {
            console.log(`Check field ID: ${formField.id} | Msg is: ${formField.error}`);
            if (activityForm.validateEmptyField(formField.id, formField.error)) {
                formError = true;
            }
        });

        // Add message to the flash message area if there is a form error
        if (formError) {
            activityForm.showFlashMessage('Please correct form errors below');
        }
    }

};

$('form[name=register_form').submit(function(e) {

  var $form = $(this);
  var $error = $form.find('.form__error');
  var data = $form.serialize();

  $.ajax({
    url: '/user/add_user/',
    type: 'POST',
    data: data,
    dataType: 'json',
    success: function(resp) {
        window.location.href = '/user/welcome/';
    },
    error: function(resp) {
        console.log(resp);
        $error.text(resp.responseJSON.error).removeClass('form__error-hidden');
    }
  });

  e.preventDefault();
});

$('form[name=login_form').submit(function(e) {

  var $form = $(this);
  var $error = $form.find('.form__error');
  var data = $form.serialize();

  $.ajax({
    url: '/user/login_user/',
    type: 'POST',
    data: data,
    dataType: 'json',
    success: function(resp) {
        window.location.href = '/user/logged-in/';
    },
    error: function(resp) {
        console.log(resp);
        $error.text(resp.responseJSON.error).removeClass('form__error-hidden');
    }
  });

  e.preventDefault();
});


/* Show or hide the venue fields when Location is changed
*/
$('#location').change(function(e) {

    const activityLocation = $('#location' ).val();
    // const locationFields = ['name', 'postcode', 'address', 'email', 'website']
    const locationFields = ['venue-name', 'venue-postcode', 'venue-address']
    $('#venue-location').val(activityLocation);

    if (activityLocation === '2') {
        locationFields.forEach( field => {
            $('#' + field).attr('required', '');
        });
        $('#venue--header').collapse('show');
        $('#venue--details').collapse('show');
    } else {
        $('#venue--header').collapse('hide');
        $('#venue--details').collapse('hide');
        locationFields.forEach( field => {
            $('#' + field).removeAttr('required');
        });
    }
});

/* Allow the user to toggle the venue details section
*/
$('#venue--toggle').click(function(e) {
    $('#venue--details').collapse('toggle');
});

/* Activate tooltips
*/
$(function() {
    $('[data-toggle="tooltip"]').tooltip()
});

$(document).ready(function(){

    /* if on the activity_form
    */
   if( $('#title').length ) {

        /* Detect form submit to change activity button contents and
        perform basic front-end validation.
        */
        $('#btn--form-update').click(function(e) {
            image = $('#image').val();
            $('#btn--form-update').html('Processing <i class="fas fa-spinner fa-spin"></i>');
            activityForm.checkForm();
        });

        /* Set hidden venue location to the same as the activity location
        to help with form validation */
        const currentLocation = $('#location' ).val()
        $('#venue-location').val(currentLocation);

        /* re-show the venue fields if required on form-error re-display
        */
        if (currentLocation == 2) { 
            $('#venue--header').collapse('show');
            $('#venue--details').collapse('show');
        }

        /*  Reset form submit button to standard text
        */
        activityForm.submitButtonText = $('#btn--form-update').text();
        $('input, select, textarea').click(function(e) {
            $('#btn--form-update').text(activityForm.submitButtonText);
        });

        /* Validate file input field on change
        */
        $('#image').change( (e) => {
            let fileSize = e.originalEvent.target.files[0].size;
            let fileType = e.originalEvent.target.files[0].type;
            $('#image').blur(function(){
                if(!$(this).val()){
                    activityForm.clearFieldError('image');
                }
            });            
            activityForm.validateFileInput('image', fileSize, fileType);
        });

        /* Remove field error on change
        */
        activityForm.checkFieldsEmpty.forEach( (formField) => {
            $('#' + formField.id).change( () => {
                activityForm.clearFieldError(formField.id);
            });
        });
        
    }
});

