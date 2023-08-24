document.addEventListener('DOMContentLoaded', () => {
  // Functions to open and close a modal
  function openModal($el) {
    $el.classList.add('is-active');
  }

  function closeModal($el) {
    $el.classList.remove('is-active');
  }

  function closeAllModals() {
    (document.querySelectorAll('.modal') || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  // Add a click event on buttons to open a specific modal
  (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);

    $trigger.addEventListener('click', () => {
      openModal($target);
    });
  });

  // Add a click event on various child elements to close the parent modal
  (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
    const $target = $close.closest('.modal');

    $close.addEventListener('click', () => {
      closeModal($target);
    });
  });

  // Add a keyboard event to close all modals
  document.addEventListener('keydown', (event) => {
    const e = event || window.event;

    if (e.keyCode === 27) { // Escape key
      closeAllModals();
    }
  });
});

const base_url = window.location.host //'http://127.0.0.1:8000'
window.addEventListener('pageshow', function(event) {
  if (event.persisted) {
    window.location.reload();
  }
});

//had to refactor it, after I found out the issue with wrapping the box post div in a tags
function addPost(post){
  var postlist = document.getElementById("postlist");
  // var item = document.createElement('a');
  // item.href =  `/post/${post.id}`;
  const item = document.createElement('div')
  item.classList.add('box')
  item.classList.add('post')
  var postdiv = `
  
    <a href=/post/${post.id}>
    <figure class="image is-96x96">
      <img class='profile-pic' src="static${post.profile_pic}">
    </figure>
    ${post.message ? `<p class='subtitle is-4'>${post.message}</p>` : ""}
    <div>
      ${post.media ? `<figure><img class='media' src="/static${post.media}"></figure>` : ""}
      <span class="is-small has-text-grey-light">
        posted by ${post.profile} on ${new Date(post.date).toLocaleString()}
      </span>
    </a>
  
  `;
  // const newItem = document.createElement('div')
  // newItem.innerHTML = postdiv
  // item.appendChild(newItem)
  item.innerHTML = postdiv
  postlist.insertBefore(item, postlist.firstChild);
  console.log(item, post)
}


var base_api_url = `/api`
const modal = document.getElementById("Modal");
const btn = document.getElementById("ModalBtn");

// When the user clicks the button, open the modal
btn.addEventListener("click", function(){
  modal.classList.add('is-active');
});

//csrftoken generator
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// const csrftoken = getCookie('csrftoken');

// let csrftoken;
// fetch(`${base_url}/get_csrf_token`)
//     .then(response => response.json())
//     .then(data => {
//         // store the CSRF token in a variable
//         window.csrftoken = data.csrf_token;
//         console.log(csrftoken); // check if the variable is defined
//     });

    
// When the user submits the form, close the modal
const form = document.getElementById("ModalForm");
console.log(csrftoken)
form.addEventListener("submit", function(event) {
  event.preventDefault();
  modal.classList.remove('is-active')
  console.log('form submitted')
  var url = `${base_api_url}/createpost`
  const formData = new FormData(form);
  
  for (var pair of formData.entries()) {
  console.log(pair[0]+ ', ' + pair[1]); 
}
  
  fetch(url, {
    method:'POST',
    headers:{
      'X-CSRFToken':csrftoken
    },
    body:formData
  })
  .then(response => response.json())
.then(addPost).catch(error => {
    console.log(error)
  });
});