const messageInput = document.getElementById('dmmessage')
const messageBtn = document.getElementById('messageBtn')
var profile = messageInput.dataset.profile
var base_url = window.location.host
console.log(csrftoken)
console.log(profile)
console.log(base_url)


//machine learning model will pass through here

function retrieveHome(){
  url = ``
  fetch(url)
  .then(response => response.json())
  .then(renderHome)
  .catch(error => {
    console.log(error)
  })
}

function formatDate(dateString) {
  const date = new Date(dateString);
  const options = { hour: 'numeric', minute: 'numeric', hour12: true };
  const formattedDate = date.toLocaleString('en-US', options);
  return formattedDate;
}

function renderHome(messages) {
  console.log(messages)

}
