function display(value, name) {
  document.getElementById("beforenotes").style.display="none";
  
  // console.log(value)
  if (name != undefined) {
    document.getElementById("professor").innerHTML = `Professor :- `;
    document.getElementById("professorn").innerHTML = `Name of professor`;
    document.getElementById("display_n_yr1").setAttribute("src", value);
  }
  else{
    document.getElementById("professor").innerHTML = ``;
    document.getElementById("professorn").innerHTML = ``;
    document.getElementById("display_n_yr1").setAttribute("src", value);
  }
  
}
let carticon = document.querySelector("#nav-cart");
let cart = document.querySelector(".cart");
let cartclose = document.querySelector("#close-cart");

carticon.onclick = () => {
  cart.classList.add("active");
};

cartclose.onclick = () => {
  cart.classList.remove("active");
};
let menu = document.querySelector("#menu-icon");
let navbar = document.querySelector(".navbar");

menu.onclick = () => {
  navbar.classList.toggle("active");
};

window.onscroll = () => {
  navbar.classList.remove("active");
};

const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatcontainer = document.querySelector(".chat-container");

let userText = null;

const createElement = (html, className) => {
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);
    chatDiv.innerHTML = html;
    return chatDiv;
};

const showtypingdot = () => {
    const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="static/image/logomyapp.png" alt="sys-img">
                        <div class="typing-animation">
                            <div class="typing-dot"style="--delay:0.2s"></div>
                            <div class="typing-dot"style="--delay:0.3s"></div>
                            <div class="typing-dot"style="--delay:0.4s"></div>
                        </div>
                    </div>
                </div>`;
    const outgoingChatDiv = createElement(html, "incoming");
    chatcontainer.appendChild(outgoingChatDiv);
    // Assuming getChatResponse is a function you've defined elsewhere
    // getChatResponse();
};

const handleOutgoingChat = () => {
  userText = chatInput.value.trim();
  const html = `<div class="chat-content">
                  <div class="chat-details">
                      <img src="static/image/default-profile.png" alt="user-img">
                      <p>${userText}</p>
                  </div>
              </div>`;
  const outgoingChatDiv = createElement(html, "outgoing");
  chatcontainer.appendChild(outgoingChatDiv);
  setTimeout(showtypingdot, 20);

  // Using AJAX to send data to Flask server
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/process_input', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
          // Clear typing dots
          chatcontainer.innerHTML = '';

          if (xhr.status === 200) {
              var response = JSON.parse(xhr.responseText);
              console.log("Server response:", response);

              // Process the response as needed
              if (response.success) {
                  const systemResponse = response.completion;
                  // Update your UI to display the system's response
                  const systemHtml = `<div class="chat-content">
                                          <div class="chat-details">
                                              <img src="static/image/logomyapp.png" alt="sys-img">
                                              <p>${systemResponse}</p>
                                          </div>
                                      </div>`;
                  const incomingChatDiv = createElement(systemHtml, "incoming");
                  chatcontainer.appendChild(incomingChatDiv);
              } else {
                  // Handle server error
                  console.error("Server error:", response.error);
              }
          } else {
              // Handle AJAX error
              console.error("AJAX error:", xhr.statusText);
          }
      }
  };
  xhr.send('user_input=' + userText);
};

sendButton.addEventListener("click", handleOutgoingChat);
