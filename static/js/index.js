$(document).ready(function() {
    
    // $(document).on('click', '#login', function() {
    //     console.log('VISIBLE');
    //     $('.backdrop').css('visibility', 'visible');
    //     $.get('/login/?backdrop=true', (response) => {
    //         $('.backdrop').append(response);
    //     });
    // });

    $(document).on('click', '.backdrop-close', function() {
        $('.backdrop').css('visibility', 'hidden');
        $('.backdrop').empty();
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

    $(document).on('click', '.dashboard--post-container', function() {
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
        var urlParams = new URLSearchParams(window.location.search);
        let post_type = urlParams.get('type');
        $.get('/filter_videos/?type='+post_type, (response) => {
            $('.backdrop').append(response);
        });
    });
    
});
