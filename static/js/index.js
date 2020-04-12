$(document).ready(function() {

    $('.dashboard--post-container').on('click', function() {
        $('.backdrop').css('visibility', 'visible');
        let post_id = $(this).attr('post_id');
        $.get('/play/'+post_id, (response) => {
            $('.backdrop').append(response);
        });
    });

    $('.video-backdrop').click(function() {
        $(this).css('visibility', 'hidden');
        $(this).empty();
    });

    $('.dashboard--toolbar-add-post').click(function() {
        $('.backdrop').css('visibility', 'visible');
        $.get('/add_post/', (response) => {
            $('.backdrop').append(response);
        });
    })

    $('.backdrop').click(function() {
        $(this).css('visibility', 'hidden');
        $(this).empty();
    });

});
