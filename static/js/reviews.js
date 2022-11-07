const likeBtn = document.querySelector('#like-btn')
likeBtn.addEventListener('click', function (event) {
    axios({
        method: 'GET',
        url: `/reviews/${event.target.dataset.reviewId}/like/`
    })

        .then(response => {
            if (response.data.existed_user === true) {
                event.target.style.color = "red";

            }
            else {
                event.target.style.color = "black";

            }
            const likeCount = document.querySelector('#like-count')
            likeCount.innerText = response.data.likeCount
        })
})
