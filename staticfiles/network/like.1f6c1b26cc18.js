document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.likebutton').forEach(button => {
        button.onclick = () => {
            const id = button.dataset.postid;
            var state = button.dataset.state;
            toggle_archive(id, state);
        };
    })



});

function toggle_archive(id, state) {
    fetch(`/posts/like/${id}`, {
            method: "PUT",
            body: JSON.stringify({
                like: !state,
            })
        })
        .then((response) => response.json())
        .then((post) => {
            const color = document.querySelector(`#b${id}`).style.color;
            if (color == 'red') {
                document.querySelector(`#b${id}`).style.color = 'black';
            } else if (color == 'black') {
                document.querySelector(`#b${id}`).style.color = 'red';
            }
            document.querySelector(`#l${id}`).innerHTML = `Likes: ${post.likes}`;
        });

}