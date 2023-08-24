const messageInput = document.getElementById('dmmessage')
const messageBtn = document.getElementById('messageBtn')
var profile = messageInput.dataset.profile
var base_url = window.location.host
console.log(csrftoken)
console.log(profile)
console.log(base_url)

const chat = document.getElementById('dmmessagelist')
chat.scrollTop = chat.scrollHeight;

function retrieveDM(){
  url = `/api/dm_messages/${profile}`
  fetch(url)
  .then(response => response.json())
  .then(renderDM)
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

function renderDM(messages) {
  console.log(messages)
  const dmmessagelist = document.getElementById('dmmessagelist');
  dmmessagelist.innerHTML = '';
  messages.dm_messages.forEach(function(message) {
    const item = document.createElement('div');
    item.classList.add('columns');
    item.classList.add('is-vcentered');
    var messagediv = `
       <div class="column is-2">
          <figure class="image is-square">
            <img class="is-rounded" src="/static/${message.profile_pic}">
          </figure>
        </div>
        <div class="column">
          <span class="subtitle is-6">${message.profile} <span class='subtitle is-6'>${formatDate(message.date)}</span></span>
          <br>
          <span>${message.message}</span>
        </div>
    `;
    item.innerHTML = messagediv;
    dmmessagelist.appendChild(item);
  });
  dmmessagelist.scrollTop = dmmessagelist.scrollHeight;
}

retrieveDM()