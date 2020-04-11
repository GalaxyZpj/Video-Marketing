// var backdrop = document.querySelector('.backdrop');
// var videoBackdrop = document.querySelector('.video-backdrop')
// var addPost = document.querySelector('.dashboard--toolbar-add-post')
// var posts = document.querySelectorAll('.dashboard--post-container')


// addPost.addEventListener('click', () => {
//     backdrop.style.visibility = 'visible';
// })

$(document).ready(function() {
    $('.dashboard--post-container').on('click', function() {
        $('.video-backdrop').css('visibility', 'visible');
        let post_id = $(this).attr('post_id');
        console.log('UNDER PROCESS '+post_id);
        $.get('/play/'+post_id, (response, status) => {
            // console.log(response);
            // console.log(status);
            $('.video-player').append(response);
        });
    });
    $('.video-backdrop').click(function() {
        $(this).css('visibility', 'hidden');
        $('.video-player').empty();
    })
    $('.dashboard--toolbar-add-post').click(function() {
        $('.backdrop').css('visibility', 'visible');
    })
    $('.backdrop').click(function() {
        $(this).css('visibility', 'hidden');
    });
});
