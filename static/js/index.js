$(document).ready(function() {
    
    $(document).on('click', '.backdrop-close', function() {
        $('.backdrop').css('visibility', 'hidden');
        $('.backdrop').empty();
    });

    $(document).on('click', '.post-video-frame', function() {
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
});
    // $(document).on('click', '#login', function() {
    //     console.log('VISIBLE');
    //     $('.backdrop').css('visibility', 'visible');
    //     $.get('/login/?backdrop=true', (response) => {
    //         $('.backdrop').append(response);
    //     });
    // });

    // $(document).on('change', '#category', function() {
    //     console.log('Button Clicked');
    //     let category_id = $(this).val();
    //     console.log('Category Selected ' + category_id);
    //     $.ajax({
    //         method: 'GET',
    //         url: '/sub_category/?category_id='+category_id,
    //         success: response => {
    //             console.log(response);
    //             $('#subCategory').empty()
    //             $('#subCategory').append(response); 
    //         },
    //         error: error => {
    //             console.error(error);
    //         }
    //     });
    // });

    // $('#filter-posts').click(function() {
    //     $('.backdrop').css('visibility', 'visible');
    //     // var urlParams = new URLSearchParams(window.location.search);
    //     // let post_type = urlParams.get('type');
    //     let postTypeArr = window.location.pathname.split('/');
    //     let postType = postTypeArr[(postTypeArr.length)-2]
    //     console.log(postType);
    //     $.get('/filter_videos/'+postType, (response) => {
    //         $('.backdrop').append(response);
    //     });
    // });
    

// POSTS TEMPLATE SCRIPTS
// <!-- <script src="{% static 'js/jquery.waypoints.min.js' %}"></script>
// <script src="{% static 'js/infinite.min.js' %}"></script>
// <script>
//     var categories = {{ categories|safe }}
//     var subCategories = {{ sub_categories|safe }}
//     console.log(categories);
//     console.log(subCategories);
    
//     var cats = document.querySelectorAll('.category-choices');
//     for (let cat of cats) {
//         cat.addEventListener('click', function() {
//             let category_id = cat.getAttribute('value');
//             console.log(category_id);
//             $.get('/sub_categories/'+category_id, (response) => {
//                 subCategories = response;
//                 console.log(subCategories);
//                 $('.sub-category-filterbox--options').empty()
//                 $('.sub-category-filterbox--options').append(response);
//             });
//         });
//     }

// </script>
// <script>
//     function chk_scroll(e) {
//         var elem = $(e.currentTarget);
//         if (elem[0].scrollHeight - elem.scrollTop() == elem.outerHeight()) {
//             console.log("bottom");
//             return 0;
//         }
//     }
//     var infinite = new Waypoint.Infinite({
//         // element: $('.infinite-container')[0],
//         element: document.getElementById('post-grid'),
//         handler: function(direction) {
//             alert('Bottom Hit');
//         },
//         onBeforePageLoad: function () {
//           $('.loading').show();
//         },
//         onAfterPageLoad: function ($items) {
//           $('.loading').hide();
//         },
//         // offset: function() {
//         //     return -this.element.clientHeight
//         // }
//         // offset: '-0.00000000000001%'
//         // offset: -30
//         offset: 'bottom-in-view'
//       });
// </script> -->