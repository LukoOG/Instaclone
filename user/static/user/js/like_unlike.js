const like = document.getElementById('like');
const likeForm = document.getElementById('likeForm')
const likeBtn = document.getElementById('likeBtn')
const likeIcon = document.getElementById('likeIcon')

var pk = like.dataset.postId

function updatelike(object){
  data = object
  //const data = JSON.parse(object);
  like.innerHTML = data.likes
  console.log(data)
}


console.log(pk)
console.log(csrftoken)


likeBtn.addEventListener("click", function(event){
  let action = like.dataset.action
  event.preventDefault();
  console.log(action)
  console.log('form submitted')
  var url = `/api/like_unlike/${pk}`
  
  fetch(url, {
    method:'POST',
    headers:{
      'X-CSRFToken':csrftoken,
      'Content-Type': 'application/json'
    },
    body:JSON.stringify({action:action})
    })
  .then(response => response.json())
  
.then(updatelike)
.then(data =>{
  if (action === 'like') {
    likeIcon.classList.add('liked');
    like.dataset.action = 'unlike';
  } else if (action === 'unlike') {
    likeIcon.classList.remove('liked');
    like.dataset.action = 'like';
  }
  
  }).catch(error => {
    console.log(error)
  });
});