/*
 * Object to handle client-side activity form validation
 */
const activityForm = {
    submitButtonText: '',
    imageUploadType: ['image/jpeg'],
    maxUploadImageSize: (4 * 1024 * 1024),
    // Define fields to check and their error message
    checkFieldsEmpty: [
        {id: 'title', error: 'Field must be at least 4 characters long.'},
        {id: 'shortDescr', error: 'Field must be at least 4 characters long.'},
        {id: 'longDescr', error: 'Field must be at least 200 characters long.'},
        {id: 'location', error: 'Please select an option.'},
        {id: 'ageRange', error: 'Enter age range ie. 3-99  10-14  etc'},
        {id: 'online', error: 'Please select an option.'},
        {id: 'freeTodo', error: 'Please select an option.'},
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
        // Remove previous error message
        activityForm.clearFieldError(formFieldID);
        // Show new error message
        $('#btn--form-update').text(activityForm.submitButtonText);
        $('#' + formFieldID + '--error').html('<span>' + errorMessage + '</span>');
        $('#' + formFieldID + '--error').removeClass('d-none');
        $('#' + formFieldID).addClass('is-invalid');
        $('#' + formFieldID).focus();
    },

    validateEmptyField: (formFieldID, errorMessage=' field error.') => {
        const fieldValue = $('#' + formFieldID).val();
        // Check if field value blank or no selection made
        if (fieldValue == '' || fieldValue == 0) {
            activityForm.showFieldError(formFieldID, errorMessage);
            return true;
        } else { 
            return false;
        }
    },

    validateFileInput: (formFieldID, fileSize, fileType) => {
        let fileError = false;
        // Clear existing file error and flash message
        activityForm.clearFieldError(formFieldID);
        $('#flash--message').empty();
        // Check upload image size and type
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
        let formError = false;
        activityForm.checkFieldsEmpty.forEach( (formField) => {
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

// Check for user registration form submitted
$('form[name=register_form').submit(function(e) {
    e.preventDefault();
    let $form = $(this);
    let $error = $form.find('.form__error');
    let data = $form.serialize();
    $.ajax({
        url: '/user/add_user/',
        type: 'POST',
        data: data,
        dataType: 'json',
        success: function(resp) {
            window.location.href = '/user/welcome/N/';
        },
        error: function(resp) {
            $error.text(resp.responseJSON.error).removeClass('form__error-hidden');
        }
    });
});

// Check for user login form submitted
$('form[name=login_form').submit(function(e) {
    e.preventDefault();
    let $form = $(this);
    let $error = $form.find('.form__error');
    let data = $form.serialize();
    $.ajax({
        url: '/user/login_user/',
        type: 'POST',
        data: data,
        dataType: 'json',
        success: function(resp) {
            window.location.href = '/user/welcome/R/';
        },
        error: function(resp) {
            $error.text(resp.responseJSON.error).removeClass('form__error-hidden');
        }
    });
});

/*
 * Function to setup event listeners on add/edit activity form
 */
function activityFormEventListeners() {
    // Show or hide the venue fields when Location is changed
    $('#location').change(function(e) {
        const activityLocation = $('#location' ).val();
        const locationFields = ['venue-name', 'venue-postcode', 'venue-address'];
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

    // Allow the user to toggle the venue details section
    $('#venue--toggle').click(function(e) {
        $('#venue--details').collapse('toggle');
    });

    /* Detect form submit to change activity button contents and
    perform basic front-end validation. */
    $('#btn--form-update').click(function(e) {
        $('#btn--form-update').html('Processing <i class="fas fa-spinner fa-spin"></i>');
        activityForm.checkForm();
    });

    // Reset form submit button to standard text
    activityForm.submitButtonText = $('#btn--form-update').text();
    $('input, select, textarea').click(function(e) {
        $('#btn--form-update').text(activityForm.submitButtonText);
    });

    // Validate file input field on change
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

    // Remove field error on change
    activityForm.checkFieldsEmpty.forEach( (formField) => {
        $('#' + formField.id).change( () => {
            activityForm.clearFieldError(formField.id);
        });
    });
}

$(document).ready(function(){

    // If on the activity_form
    if( $('#title').length ) {

        // Activate tooltips
        $('[data-toggle="tooltip"]').tooltip();

        /* Set hidden venue location to the same as the activity location
        to help with form validation */
        const currentLocation = $('#location' ).val();
        $('#venue-location').val(currentLocation);

        // Re-show the venue fields if required on form-error re-display
        if (currentLocation == 2) { 
            $('#venue--header').collapse('show');
            $('#venue--details').collapse('show');
        }

        activityFormEventListeners();
    }

});
