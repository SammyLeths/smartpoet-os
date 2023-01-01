// JQUERY START

$(document).ready(function(){

    // FOLLOW BUTTON

    follow_btn = document.querySelectorAll(".follow-btn");

    follow_btn.forEach((element) => {
        follow_handeler(element);
    });

    // LIKE AND UNLIKE ICON BUTTON

    like = document.querySelectorAll(".liked");

    like.forEach((element) => {
        like_handeler(element);
    });



    // BOOKMARK/SAVE AND UNSAVE ICON BUTTON

    bookmark = document.querySelectorAll(".bookmarked");

    bookmark.forEach((element) => {
        bookmark_handeler(element);
    });



    // DOWNVOTE ICON BUTTON

    downvote = document.querySelectorAll(".downvoted");

    downvote.forEach((element) => {
        downvote_handeler(element);
    });



    // UPVOTE ICON BUTTON

    upvote = document.querySelectorAll(".upvoted");

    upvote.forEach((element) => {
        upvote_handeler(element);
    });



    // MOBILE SIDEBAR NAV TOGGLE

    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    $('#dismiss, .overlay').on('click', function () {
        // hide sidebar
        $('#sidebar').removeClass('active');
        // hide overlay
        $('.overlay').removeClass('active');
    });

    $('#sidebarCollapse').on('click', function () {
        // open sidebar
        $('#sidebar').addClass('active');
        // fade in the overlay
        $('.overlay').addClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });



    // Process the forgot password form on login page (NOT IN USE)

    /*
    $('#form_lp').on('submit', function(event)
    {
      var value = $("#lpemail_id").val();
      var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
      if (value == '')
      {
        var message='Please enter your email address';
        $('#alert').html(message).addClass('alert alert-danger alert-dismissable');
      }
      else if(!emailReg.test(value))
      {
        var message='Please enter a valid email address';
        $('#alert').html(message).addClass('alert alert-danger alert-dismissable');
      }
      else
      {
        $.ajax({
          data : {
            email : $('#lpemail_id').val()
          },
          type : 'POST',
          url : '/reset-password'
        })
        .done(function(data) {
          if (data.error)
          {
            $('#alert').html(data.error).toggleClass().addClass('alert alert-danger alert-dismissable');
          }
          else
          {
            $('#alert').html(data.success).toggleClass().addClass('alert alert-success alert-dismissable');
            $('#form_lp')[0].reset(); //To reset form fields
          }
        });
      }
      event.preventDefault();
    });
    */

    // Clears out forgot password form data onclick of reset (NOT IN USE)

    /*
    $(".reset_lpform").click(function(e) {
          $('#alert').html(message='').removeClass();
    });
    */


    // END - BEGIN


    // Add down arrow icon for collapse element which is open by default

    $(".collapse.show").each(function(){
      $(this).prev(".card-header").find(".fa").addClass("fa-angle-down").removeClass("fa-angle-right");
    });

    // Toggle right and down arrow icon on show hide of collapse element

    $(".collapse").on('show.bs.collapse', function(){
      $(this).prev(".card-header").find(".fa").removeClass("fa-angle-right").addClass("fa-angle-down");
    }).on('hide.bs.collapse', function(){
      $(this).prev(".card-header").find(".fa").removeClass("fa-angle-down").addClass("fa-angle-right");
    });

    // Disable all manage account form fields on load_user

    $("#personalInfoForm :input").prop("disabled", true);
    $("#edHistoryForm :input").prop("disabled", true);
    $("#socialProfileForm :input").prop("disabled", true);
    //$("#changePasswordForm :input").prop("disabled", true);
    $("#userSettingsForm :input").prop("disabled", true);

    // END - BEGIN


    // CONTROLS CHECKBOX SELECTION ON DATA TABLE

    // Controls master checkbox to check all others

    $('.select_allbox').each(function(){
       $(this).attr('id');
    }).on('click', function(){
       boxid = $(this).attr('id');
       if(this.checked){
           $('.checkbox'+'#'+boxid).each(function(){
               this.checked = true;
           });
       }else{
           $('.checkbox'+'#'+boxid).each(function(){
               this.checked = false;
           });
       }
    });

    // Controls individual checkbox and checks master when all individual has been checked

    $('.checkbox').each(function(){
       $(this).attr('id');
    }).on('click', function(){
       checkid = $(this).attr('id');
       if($('.checkbox'+'#'+checkid+':'+'checked').length == $('.checkbox'+'#'+checkid).length){
           $('.select_allbox'+'#'+checkid).prop('checked', true);
       }else{
           $('.select_allbox'+'#'+checkid).prop('checked', false);
       }
    });

    // Controls Dependent/Chained Post Category (Category and Sub Category) Dropdown List (OLD METHOD)

    /*category_select = document.getElementById('category');
    sub_category_select = document.getElementById('sub_category');

    category_select.onchange = function(){

      category = category_select.value;

      fetch('sub_category/' + category).then(function(response){
        response.json().then(function(data) {
          optionHTML = '';
          for (sub_category of data.sub_categorycategory) {
            optionHTML += '<option value=' + sub_category.id +'>' + sub_category.name + '</option>'
          }
          sub_category_select.innerHTML = optionHTML;
        });
      });
    }*/


    // END -BEGIN

    // Controls Dependent/Chained Post Category (Category and Sub Category) Dropdown List (NEW METHOD)

    $("#pf5").change(function () {

      var url = $("#PostForm").attr("data-subcat-url");  // get the url of the `load_subcategory` view
      var catId = $(this).val();  // get the selected category ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-sub-category)
        data: {
          'category': catId       // add the category id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_subcategory` view function
          $("#pf6").html(data);  // replace the contents of the sub_category input with the data that came from the server
        }
      });

    });


    // end  -  begin

    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl);
    })


    // end - begin CONTROLS TOOLTIP

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    })



});



// END - BEGIN

// DISQUSWIDGETS.getCount({reset: true});

// Enables personalInfoForm onClick of Edit

$("#editPI").click(function(e){
  $("#personalInfoForm :input").prop("disabled", false);
  $(this).hide();
});

// Enables edHistoryForm onClick of Edit

$("#editEH").click(function(e){
  $("#edHistoryForm :input").prop("disabled", false);
  $(this).hide();
});

// Enables socialProfileForm onClick of Edit

$("#editSP").click(function(e){
  $("#socialProfileForm :input").prop("disabled", false);
  $(this).hide();
});

// Enables changePasswordForm onClick of Edit

$("#editCP").click(function(e){
  $("#changePasswordForm :input").prop("disabled", false);
  $(this).hide();
});

// Enables userSettingsForm onClick of Edit

$("#editUS").click(function(e){
  $("#userSettingsForm :input").prop("disabled", false);
  $(this).hide();
});


// END - BEGIN

//

function delete_confirm(selid){
    if($('.checkbox'+'#'+selid+':'+'checked').length < 1){
        var result = confirm("Please select at least one record");
    }else{
        var result = confirm("Are you sure you want to perform selected action?");
    }
    return(result);
}



// END - BEGIN


// LIKE / UNLIKE FUNCTION


function like_handeler(element) {

    element.addEventListener("click", () => {

      id = element.getAttribute("data-id");
      is_liked = element.getAttribute("data-is_liked");
      icon = document.querySelector(`#post-like-${id}`);
      count = document.querySelector(`#post-count-${id}`);

      form = new FormData();
      form.append("id", id);
      form.append("is_liked", is_liked);
      fetch("/like/", {
        method: "POST",
        body: form
      })
        .then((res) => res.json())
        .then((res) => {
            if (res.logged == false) {
                if (confirm("Please log in before you can like or unlike a poem. Proceed to login?")) {
                    window.location.href = "/accounts/login/";
                }
            } else {
                if (res.status == 201) {
                    if (res.is_liked === "yes") {
                        icon.classList.add("fas")
                        icon.classList.remove("far")
                        element.setAttribute("data-is_liked", "yes");
                    } else {
                        icon.classList.add("far")
                        icon.classList.remove("fas")
                        element.setAttribute("data-is_liked", "no");
                    }
                    count.textContent = res.like_count;
                }
            }
        })
        .catch(function (res) {
          alert("Network Error. Please Check your connection.");
        });
    });
  }




// END - BEGIN


// BOOKMARK / UNSAVE FUNCTION


function bookmark_handeler(element) {

    element.addEventListener("click", () => {

      id = element.getAttribute("data-id");
      is_bookmarked = element.getAttribute("data-is_bookmarked");
      icon = document.querySelector(`#post-bookmark-${id}`);
      count = document.querySelector(`#post-bookmark-count-${id}`);

      form = new FormData();
      form.append("id", id);
      form.append("is_bookmarked", is_bookmarked);
      fetch("/bookmark/", {
        method: "POST",
        body: form
      })
        .then((res) => res.json())
        .then((res) => {
            if (res.logged == false) {
                if (confirm("Please log in before you can bookmark or save a poem. Proceed to login?")) {
                    window.location.href = "/accounts/login/";
                }
            } else {
                if (res.status == 201) {
                    if (res.is_bookmarked === "yes") {
                        icon.classList.add("fas")
                        icon.classList.remove("far")
                        element.setAttribute("data-is_bookmarked", "yes");
                    } else {
                        icon.classList.add("far")
                        icon.classList.remove("fas")
                        element.setAttribute("data-is_bookmarked", "no");
                    }
                    count.textContent = res.bookmark_count;
                }
            }
        })
        .catch(function (res) {
          alert("Network Error. Please Check your connection.");
        });
    });
  }




// END - BEGIN


// DOWNVOTE FUNCTION


function downvote_handeler(element) {

    element.addEventListener("click", () => {

      id = element.getAttribute("data-id");
      is_downvoted = element.getAttribute("data-is_downvoted");
      icon = document.querySelector(`#post-downvote-${id}`);
      count = document.querySelector(`#post-downvote-count-${id}`);

      form = new FormData();
      form.append("id", id);
      form.append("is_downvoted", is_downvoted);
      fetch("/downvote/", {
        method: "POST",
        body: form
      })
        .then((res) => res.json())
        .then((res) => {
            if (res.logged == false) {
                if (confirm("Please log in before you can downvote a poem. Proceed to login?")) {
                    window.location.href = "/accounts/login/";
                }
            } else {
                if (res.status == 201) {
                    if (res.is_downvoted === "yes") {
                        icon.classList.add("fas")
                        icon.classList.remove("far")
                        element.setAttribute("data-is_downvoted", "yes");
                    } else {
                        icon.classList.add("far")
                        icon.classList.remove("fas")
                        element.setAttribute("data-is_downvoted", "no");
                    }
                    count.textContent = res.downvote_count;
                }
            }
        })
        .catch(function (res) {
          alert("Network Error. Please Check your connection.");
        });
    });
  }





// END - BEGIN


// UPVOTE FUNCTION


function upvote_handeler(element) {

    element.addEventListener("click", () => {

      id = element.getAttribute("data-id");
      is_upvoted = element.getAttribute("data-is_upvoted");
      icon = document.querySelector(`#post-upvote-${id}`);
      count = document.querySelector(`#post-upvote-count-${id}`);

      form = new FormData();
      form.append("id", id);
      form.append("is_upvoted", is_upvoted);
      fetch("/upvote/", {
        method: "POST",
        body: form
      })
        .then((res) => res.json())
        .then((res) => {
            if (res.logged == false) {
                if (confirm("Please log in before you can upvote a poem. Proceed to login?")) {
                    window.location.href = "/accounts/login/";
                }
            } else {
                if (res.status == 201) {
                    if (res.is_upvoted === "yes") {
                        icon.classList.add("fas")
                        icon.classList.remove("far")
                        element.setAttribute("data-is_upvoted", "yes");
                    } else {
                        icon.classList.add("far")
                        icon.classList.remove("fas")
                        element.setAttribute("data-is_upvoted", "no");
                    }
                    count.textContent = res.upvote_count;
                }
            }
        })
        .catch(function (res) {
          alert("Network Error. Please Check your connection.");
        });
    });
  }


function follow_handeler(element) {

    element.addEventListener("click", (e) => {

        user = element.getAttribute("data-user");
        action = element.textContent.trim();

        if (action == 'Unfollow') {

            if (confirm('Are you sure you want to unfollow '+user+' ?')) {

                form = new FormData();
                form.append("user", user);
                form.append("action", action);
                fetch("/follow/", {
                    method: "POST",
                    body: form,
                })
                    .then((res) => res.json())
                    .then((res) => {
                    if (res.status == 201) {
                        element.textContent = res.action;
                        document.querySelector("#follower").textContent = `${res.follower_count}`;
                    }
                });
            }

        } else {

            if (confirm('Are you sure you want to follow '+user+' ?')) {

                form = new FormData();
                form.append("user", user);
                form.append("action", action);
                fetch("/follow/", {
                    method: "POST",
                    body: form,
                })
                    .then((res) => res.json())
                    .then((res) => {
                    if (res.status == 201) {
                        element.textContent = res.action;
                        document.querySelector("#follower").textContent = `${res.follower_count}`;
                    }
                });

            }

        }
    });

}