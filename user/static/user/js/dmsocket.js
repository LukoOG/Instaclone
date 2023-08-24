let dm = document.getElementById('dm').value
console.log(dm)
let url = `ws://${window.location.host}/dm/${dm}`


const chatSocket = new WebSocket(url)
console.log('loaded')
console.log(url)

function formatDate(dateString) {
  const date = new Date(dateString);
  const options = { hour: 'numeric', minute: 'numeric', hour12: true };
  const formattedDate = date.toLocaleString('en-US', options);
  return formattedDate;
}

function addMessage(message){
  messageInput.value = ''
  const dmmessagelist = document.getElementById('dmmessagelist')
  const item = document.createElement('div')
  item.classList.add('columns')
  item.classList.add('is-vcentered')
  const date = new Date(message.date);
  const formattedDate = formatDate(date);
  var messagediv = `
       <div class="column is-2">
          <figure class="image is-square">
            <img class="is-rounded" src="/static${message.profile_pic}">
          </figure>
        </div>
        <div class="column">
          <span class="subtitle is-6">${message.profile} <span class='subtitle is-6'>${formattedDate}</span></span>
          <br>
          <span>${message.message}</span>
        </div>
  `
  item.innerHTML = messagediv
  dmmessagelist.appendChild(item)
  dmmessagelist.scrollTop = dmmessagelist.scrollHeight;
  console.log(message)
}


chatSocket.onmessage = function(e){
  let data = JSON.parse(e.data)
  console.log('DATA:', data)
  
  if (data.type === 'dm'){
    console.log('broadcasting dm message', data)
    addMessage(data.message)
  }
}

messageInput.addEventListener('keydown', function(event){
  if (event.keyCode === 13){
    console.log('received.')
    event.preventDefault();
    const message = messageInput.value
    var url = `/api/createdmmessage/${profile}`
    console.log(message)
     fetch(url, {
        method: 'POST',
        headers:{
          'X-CSRFToken':csrftoken,
          'Content-Type': 'application/json'
        },
        body:JSON.stringify({message:message}),
      }).then(response => response.json())
      .then(data => {
        chatSocket.send(JSON.stringify({
        'type':'dm',
        'message':data
      }))
      })
      .catch(error => {
      console.log(error)
    }); 
  }
  });  

messageBtn.addEventListener('click', function(event){
    console.log('received..')
    event.preventDefault();
    const message = messageInput.value
    let url = `/api/createdmmessage/${profile}`
    console.log(message)
	console.log(url)
    fetch(url, {
      method: 'POST',
      headers:{
        'X-CSRFToken':csrftoken,
        'Content-Type': 'application/json'
      },
      body:JSON.stringify({message:message}),
    }).then(response => response.json())
    .then(data => {
      chatSocket.send(JSON.stringify({
      'type':'dm',
      'message':data
    }))
    })
    .catch(error => {
    console.log(error)
  }); 

  });  