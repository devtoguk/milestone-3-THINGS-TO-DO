/**
 * Object to handle parts of the activity form
 */
const activityForm = {
    submitButtonText: '',

    validateEmptyField: (formFieldID, errorMessage=' field error.') => {
        fieldValue = $('#' + formFieldID).val();
        $('#' + formFieldID + '--error').addClass('d-none');
        $('#' + formFieldID).removeClass('is-invalid');
        console.log('Field is: ', formFieldID);
        console.log('Value is: [', fieldValue + ']');
        if (fieldValue == '') {
            console.log("must be 4 characters or more. ", formFieldID);
            $('#btn--form-update').text(activityForm.submitButtonText);
            $('#' + formFieldID + '--error').html('<span>' + errorMessage + '</span>');
            $('#' + formFieldID + '--error').removeClass('d-none');
            $('#' + formFieldID).addClass('is-invalid');
            $('#' + formFieldID).focus();
            console.log('Original button text is: ', activityForm.submitButtonText);
        return false;
        }
    },

    validateSelectField: (formFieldID, errorMessage=' select error.') => {
        fieldValue = $('#' + formFieldID).val();
        console.log(`${formFieldID} value is: ${fieldValue}`);
        // $('#' + formFieldID + '--error').addClass('d-none');
        // $('#' + formFieldID).removeClass('is-invalid');
        // console.log('Field is: ', formFieldID);
        // console.log('Value is: [', fieldValue + ']');
        // if (fieldValue == '') {
        //     console.log("must be 4 characters or more. ", formFieldID);
        //     $('#btn--form-update').text(activityForm.submitButtonText);
        //     $('#' + formFieldID + '--error').html('<span>' + errorMessage + '</span>');
        //     $('#' + formFieldID + '--error').removeClass('d-none');
        //     $('#' + formFieldID).addClass('is-invalid');
        //     $('#' + formFieldID).focus();
        //     console.log('Original button text is: ', activityForm.submitButtonText);
        // return false;
        // }
    },

    checkForm: () => {
        console.log('JS validate form?');
        // Remove any current flash messages
        $('#flash--message').empty();
        if (activityForm.validateEmptyField('title', 'Field must be at least 4 characters long.')) {
            formStatus = true;
        } else { formStatus = false; }

        if (activityForm.validateEmptyField('shortDescr', 'Field must be at least 4 characters long.')) {
            formStatus = true;
        } else { formStatus = false; }
        
        if (activityForm.validateEmptyField('longDescr', 'Field must be at least 4 characters long.')) {
            formStatus = true;
        } else { formStatus = false; }

        if (activityForm.validateEmptyField('category', 'At least one must be selected.')) {
            formStatus = true;
        } else { formStatus = false; }

        if (activityForm.validateEmptyField('whenTodo', 'At least one must be selected.')) {
            formStatus = true;
        } else { formStatus = false; }

        // Add message to the flash message area if there is a form error
        if (!formStatus) { 
            $('#flash--message').prepend('<div class="flash__message-error">Please correct form errors below</div>');
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
        window.location.href = '/dbtest/';
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
        window.location.href = '/activity/';
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

// function validateForm() {
//     console.log('JS validate form?')
//     var x = $('#title').val();
//     console.log('Title value is: ', x)
//     if (x == '') {
//         console.log("Title must be filled out");
//         $('#btn--form-update').text(activityForm.submitButtonText);
//         console.log('Original button text is: ', activityForm.submitButtonText);
//     return false;
//     }
// }

$(document).ready(function(){

    /* if on the activity_form
    */
   if( $('#title').length ) {

        /* Detect form submit to change activity button contents and
        perform basic front-end validation.
        */
        $('#btn--form-update').click(function(e) {
            image = $('#image').val();
            console.log('Image is: ', image)
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

        activityForm.submitButtonText = $('#btn--form-update').text();
        console.log('OBJ Button is: ', activityForm.submitButtonText);
        // $(window).onunload(function(){
        console.log('On a form page');
        $('input, select, textarea').click(function(e) {
            console.log('Clicked: ', e.target.id)
            $('#btn--form-update').text(activityForm.submitButtonText);
        });       
    }

});

