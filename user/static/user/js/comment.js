const commentInput = document.getElementById('commentInput')

var pk = commentInput.dataset.postId

function addComment(comment){
  console.log(comment)
  var commentlist = document.getElementById("commentlist");
  
  commentInput.value = ''
  const item = document.createElement('div')
  item.classList.add('block')
  item.classList.add('post')
  var commentdiv = `
      <p class='subtitle is-6'>
      <img class='img_comment' src="/static${comment.profile_pic}">${comment.profile}: ${comment.message}
      <span><a href=/delete-comment/${comment.id}><i class="fa-solid fa-trash"></i></a></span>
      </p>
    `
  item.innerHTML = commentdiv
  commentlist.insertBefore(item, commentlist.lastChild);
  console.log(item, commentlist)
}

commentInput.addEventListener('keydown', function(event){
  if (event.keyCode === 13){
    event.preventDefault();
    const message = commentInput.value;
    var url = `/api/createcomment/${pk}`;
    console.log('form submitted')
    console.log(message)
    fetch(url, {
      method: 'POST',
      headers:{
        'X-CSRFToken':csrftoken,
        'Content-Type': 'application/json'
      },
      body:JSON.stringify({message:message}),
    })
    .then(response => response.json())
    .then(addComment).catch(error => {
    console.log(error)
  });
  }
})