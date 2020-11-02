$("form[name=register_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/add_user/",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
        window.location.href = "/dbtest/";
    },
    error: function(resp) {
        console.log(resp);
        $error.text(resp.responseJSON.error).removeClass("error__hidden");
    }
  });

  e.preventDefault();
});

$("form[name=login_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/login_user/",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
        window.location.href = "/activity/";
    },
    error: function(resp) {
        console.log(resp);
        $error.text(resp.responseJSON.error).removeClass("error__hidden");
    }
  });

  e.preventDefault();
});
