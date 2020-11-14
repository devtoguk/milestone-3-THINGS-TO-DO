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
    console.log('Location: ', activityLocation);
    if (activityLocation === '2') {
        $('#venue--details').collapse('show');
    } else {
        $('#venue--details').collapse('hide');
    }

});

