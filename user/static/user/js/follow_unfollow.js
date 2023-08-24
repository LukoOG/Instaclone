const followBtn = document.getElementById("followBtn")
const follow = document.getElementById('follow')
//const totalFollowers = 
const totalFollowers = document.getElementById('total_followers')


var pk = follow.dataset.profileId

console.log(pk)
console.log(csrftoken)

function updateFollowers(object){
  data = object
  console.log(data)
  totalFollowers.innerHTML = data.total_followed
}

followBtn.addEventListener('click', function(event){
  event.preventDefault();
  let action = follow.dataset.action
  console.log('form submitted')
  console.log(action)
  var url = `/api/follow_unfollow/${pk}`
  fetch(url, {
    method:'POST',
    headers:{
      'X-CSRFToken':csrftoken,
      'Content-Type': 'application/json'
    },
    body:JSON.stringify({action:action})
    })
    .then(response => response.json())
    .then(updateFollowers)
  .then(data => {
   if (action === 'follow') {
    followBtn.innerHTML = 'unfollow'
    followBtn.classList.remove('is-success');
    followBtn.classList.add('is-danger');
    follow.dataset.action = 'unfollow';
  } else if (action === 'unfollow') {
    followBtn.innerHTML = 'follow'
    followBtn.classList.remove('is-danger');
    followBtn.classList.add('is-success');
    follow.dataset.action = 'follow';
  }
  }).catch(error => {
    console.log(error)
  })
})