$(document).ready(function() {

    var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        onBeforePageLoad: function () {
          $('.loading').show();
        },
        onAfterPageLoad: function ($items) {
          $('.loading').hide();
        }
      });
    
    // FOR DYNAMICALLY LOADED TEMPLATE
    $(document).on('click', '.backdrop-close', function() {
        $('.backdrop').css('visibility', 'hidden');
        $('.backdrop').empty();
    });

    // FOR DYNAMICALLY LOADED TEMPLATE
    $(document).on('change', '#category', function() {
        console.log('Button Clicked');
        let category_id = $(this).val();
        console.log('Category Selected ' + category_id);
        $.ajax({
            method: 'GET',
            url: '/sub_category/?category_id='+category_id,
            success: response => {
                console.log(response);
                $('#subCategory').empty()
                $('#subCategory').append(response); 
            },
            error: error => {
                console.error(error);
            }
        });
    });

    $('.dashboard--post-container').on('click', function() {
        $('.backdrop').css('visibility', 'visible');
        let post_id = $(this).attr('post_id');
        $.get('/play/'+post_id, (response) => {
            $('.backdrop').append(response);
        });
    });

    $('#add-post-btn').click(function() {
        $('.backdrop').css('visibility', 'visible');
        $.get('/add_post/', (response) => {
            $('.backdrop').append(response);
        });
    })

    $('#filter-posts').click(function() {
        $('.backdrop').css('visibility', 'visible');
        $.get('/filter_videos/', (response) => {
            $('.backdrop').append(response);
        });
    });
    
});
