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

$('form[name=submit_activity_form').submit(function(e) {

  var $form = $(this);
  var $error = $form.find('.form__error');
  var data = $form.serialize();

  $.ajax({
    url: '/activity/add/',
    type: 'POST',
    data: data,
    dataType: 'json',
    success: function(resp) {
        // console.log(resp);
        activityTitle = resp.title;
        window.location.href = '/activity/thankyou/' + activityTitle + '/';
    },
    error: function(resp) {
        console.log(resp);
        $error.text(resp.responseJSON.error).removeClass('form__error-hidden');
    }
  });

  e.preventDefault();
});

// $('#venue--details').collapse({
//   toggle: false
// });

/* Show or hide the venue fields when Location is changed
*/
$('#location').change(function(e) {

    const activityLocation = $('#location' ).val();
    const locationFields = ['name', 'postcode', 'address', 'email', 'website']

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


