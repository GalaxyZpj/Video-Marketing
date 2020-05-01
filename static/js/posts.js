$(document).ready(function() {
    
    $(document).on('click', '.backdrop-close', function() {
        $('.backdrop').css('visibility', 'hidden');
        $('.backdrop').empty();
    });

    $(document).on('click', '.post-container', function() {
        $('.backdrop').css('visibility', 'visible');
        let post_id = $(this).attr('post_id');
        $.get('/visitor/'+post_id, response => {
            $('.backdrop').append(response);
        });
    });
    
    $(document).on('submit', '#visitorForm', function(e) {
        e.preventDefault();
        
        let postId = $('#postId').val();
        let formData = {
            company_agent: $('input[name=company_agent]').val(),
            first_name: $('input[name=first_name]').val(),
            last_name: $('input[name=last_name]').val(),
            email: $('input[name=email]').val(),
            mobile: $('input[name=mobile]').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        }

        const url = '/visitor/' + postId;
        $.ajax({
            type:'POST',
            url: url,
            data: formData,
            success: function(response) {
                $('.backdrop').empty();
                $('.backdrop').append(response);
            }
        });

    });

    $('#createPost, #createPostCollapsed, .add-post').click(function() {
        $('.backdrop').css('visibility', 'visible');
        $.get('/add_post/', (response) => {
            $('.backdrop').append(response);
        });
    });

    $(document).on('change', '#type', function() {
        if ($(this).val() === 'upcoming') {
            $('#dateFormGroup').show();
        }
        else {
            $('#dateFormGroup').hide();
        }
    });

    $(document).on('change', '#category', function() {
        let category_id = $(this).val();
        $.ajax({
            method: 'GET',
            url: '/sub_category/?category_id='+category_id,
            success: response => {
                $('#subCategory').empty()
                $('#subCategory').append(response); 
            },
            error: error => {
                console.log(error);
            }
        });
    });

    $(document).on('mouseleave', '.filter-dropdown-menu', function() {
        $('.subcat-container').hide();
        $('.subcat-container').empty();
    });

    $(document).on('mouseenter', '.cat-name', function() {
        $('.subcat-container').empty();
        let categoryId = $(this).attr('value');
        $.get('/sub_category/?filter=yes&category_id=' + categoryId, response => {
            $('.subcat-container').append(response);
            let height = $('.filter-dropdown-menu').innerHeight()
            $('.subcat-container').css("height", height);
            $('.subcat-container').css('display', 'flex');
        });
    });

    $(document).on('mouseleave', '.subcat-container', function() {
        $('.subcat-container').hide();
        $('.subcat-container').empty();
    });

    $(document).on('click', '.sort-dropdown-menu-btn', function() {
        let sortByValue = $(this).attr('value');
        $('#sortHiddenInput').attr('value', sortByValue);
        $('#toolbar-form').submit();
    });

    $(document).on('click', '.subcat-name', function() {
        let subCategoryValue = $(this).attr('value');
        $('#subcategoryHiddenInput').attr('value', subCategoryValue);
        $('#toolbar-form').submit();
    });

});
