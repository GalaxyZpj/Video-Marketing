$(document).ready(function() {
    
    $(document).on('click', '.backdrop-close', function() {
        $('.backdrop').css('visibility', 'hidden');
        $('.backdrop').empty();
    });

    $(document).on('click', '.post-container', function() {
        $('.backdrop').css('visibility', 'visible');
        let post_id = $(this).attr('post_id');
        $.get('/play/'+post_id, (response) => {
            $('.backdrop').append(response);
        });
    });

    $('#createPost, #createPostCollapsed').click(function() {
        $('.backdrop').css('visibility', 'visible');
        $.get('/add_post/', (response) => {
            $('.backdrop').append(response);
        });
    });

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

});
