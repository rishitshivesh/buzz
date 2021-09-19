document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.likebutton').forEach(button => {
        button.onclick = () => {
            const id = button.dataset.postid;
            var state = button.dataset.state;
            toggle_archive(id, state);
        };
    })
    document.querySelectorAll('.editbutton').forEach(button => {
        button.onclick = () => {
            const id = button.dataset.editid;
            edittoggle(id);
        };
    })



});

function edittoggle(id) {
    console.log('Toggle Button clicked');
    fetch(`/posts/getpost/${id}`)
        .then((response) => response.json())
        .then((post) => {
            document.querySelector(`#bodyofpost${id}`).innerHTML = `  
            
            <div class="form-group mx-auto">
                <textarea class="form-control entertext" style="min-height: 20px;" id="bodyoftext${id}" columns="5" maxlength='500' name="tbody" required>${post.body}</textarea>
            </div>

            <button class="btn btn-success mr-auto" id="buttonedit${post.id}">Edit</button>
            <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#delete">Delete</button>

            <div class="" id="circle">
                <span id="circlet"></span>
                <div class="slice">
                    <div class="bar"></div>
                    <div class="fill"></div>
                </div>
            </div>
       
    </div>
    <!-- Modal DELETE -->
    <div class="modal fade" id="delete" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true" style="color:black;">
        <div class="modal-dialog modal-dialog" role="document">
            <div class="modal-content new-post-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLongTitle">Delete Post</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
                </div>
                <div class="modal-body">
                    <p>Are you sure you want to delete this post?</p>
                    <div class="modal-footer">
                        <form action="/${post.id}/delete">
                            <button class="btn btn-outline-danger save" type="submit" value="Delete"><i class="fa fa-check-square-o"></i> Delete</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
            `;
            document.querySelector(`#buttonedit${id}`).onclick = () => {
                const bodyt = document.querySelector(`#bodyoftext${id}`).value;
                if (bodyt.length != 0) {
                    editfunction(id, bodyt);
                } else {
                    console.log('This Field Cannot be empty!');
                }
            };
        });

}

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

function editfunction(id, bodyt) {
    fetch(`/posts/${id}/edit`, {
            method: "PUT",
            body: JSON.stringify({
                bodytext: bodyt,
            })
        })
        .then((response) => response.json())
        .then((post) => {
            document.querySelector(`#bodyofpost${id}`).innerHTML = `  
            <h4>
            <p class="card-text" style="color: black;">${post.body}</p>
        </h4>
        <h6 class="card-subtitle mb-2 text-muted" align="right">-${post.time}(Edited)</h6>    
            
            `;
        });

}