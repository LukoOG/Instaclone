

// function addPost(post){
//   var postlist = document.getElementById("postlist");
//   var item = document.createElement('a');
//   item.href =  `{% url "user:postpage" ${post.id} %}`;
//   var postdiv = `
//   <div class="box post">
//     <figure class="image is-96x96">
//       <img class='profile-pic' src={% static post.profile.profile_pic %}>
//     </figure>

//     {% if post.message %}
//     <p class='subtitle is-4'>${post.message}</p>
//     {% endif %}
//     <div>
//       {% if post.media %}
//         <figure >
//          <img class='media' src="{% static post.media %}"/>
//         </figure>
//       {% endif %}
//       <span class="is-small has-text-grey-light">
//         posted by ${post.profile} on ${post.date}
//       </span>
//     </div>
//     `;
//   const newItem = document.createElement('div')
//   newItem.innerHTML = postdiv
//   item.appendChild(newItem)
//   postlist.insertBefore(item, postlist.firstChild);
  
// }
