
// // 좋아요
// // 좋아요 비동기

// const likeBtn = document.querySelector('#like-btn')
// likeBtn.addEventListener('click', function (event) {

//     axios({
//         method: 'GET',
//         url: `/reviews/${event.target.dataset.reviewId}/like/`
//     })
//         .then(response => {
//             if (response.data.existed_user === true) {
//                 event.target.classList.add('bi-heart-fill')
//                 event.target.classList.remove('bi-heart')

//             }
//             else {
//                 event.target.classList.add('bi-heart')
//                 event.target.classList.remove('bi-heart-fill')

//             }
//             const likeCount = document.querySelector('#like-count')
//             likeCount.innerText = response.data.likeCount
//         })
// })

