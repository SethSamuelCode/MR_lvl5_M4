"use strict";

// console.log("hello world");

const BACKEND_SERVER = "http://localhost:8000";

// Get references to DOM elements
const conversationArea = document.querySelector("#convoDisplayArea");
const userInputForm = document.querySelector("#userInputForm");
const userTextInputArea = document.querySelector("#userInput");
const sendButton = document.querySelector("#sendButton");
userInputForm.addEventListener("submit", sendViaWebsocket); // Attach form submit handler

let websocket;

window.onload = async () => {
  // Fetch a new UUID from the backend and store it in SESSION_UUID
  // const uuidResp = await fetch(`${BACKEND_SERVER}/api/uuid`);
  // const uuidFromServer = await uuidResp.json();
  // console.log(uuidFromServer)
  //   console.log("UUID2",SESSION_UUID)
  
  websocket = new WebSocket(`${BACKEND_SERVER}/ws`);
  websocket.onmessage = (event) => {
    console.log(JSON.parse(event.data));
    const incomingMessage = JSON.parse(event.data);
          sendButton.removeAttribute("disabled"); // Enable send button after first message
      const aiResponseElement = document.createElement("p");
      aiResponseElement.classList.add("aiResponseBubble");
      aiResponseElement.classList.add("bubble");
      aiResponseElement.insertAdjacentText("afterbegin", incomingMessage.message);
      conversationArea.append(aiResponseElement);
      
    };
    
    console.log("running");
  // sendToAI()
};

// Handle form submission: send user input and job description to backend, display conversation
async function sendToAI(e) {
  //first time this func is executed there is no event to opperate on
  if (e) {
    e.preventDefault();
  }
  const userInput = userTextInputArea.value || " ";
  console.log(userInput);
  userTextInputArea.value = "";

  // Prepare fetch options for POST request
  const fetchOptions = {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      uuid: SESSION_UUID.value, // Use the stored UUID
      message: userInput,
    }),
  };

  //do not display user bubble on the first message
  if (e) {
    // Display user's message in the conversation area
    const userInputElement = document.createElement("p");
    userInputElement.classList.add("userInputBubble");
    userInputElement.classList.add("bubble");
    userInputElement.insertAdjacentText("afterbegin", userInput);
    conversationArea.append(userInputElement);
  }

  // Send request to backend and display AI's response
  const aiResponse = await fetch(`${BACKEND_SERVER}/api/chat`, fetchOptions);
  const aiText = await aiResponse.json();
  console.log(aiText);

  const aiResponseElement = document.createElement("p");
  aiResponseElement.classList.add("aiResponseBubble");
  aiResponseElement.classList.add("bubble");
  aiResponseElement.insertAdjacentText("afterbegin", aiText);
  conversationArea.append(aiResponseElement);
}

async function sendViaWebsocket(e) {
  e.preventDefault();
  const userInput = userTextInputArea.value || " ";
  userTextInputArea.value = "";
  const userInputElement = document.createElement("p");
  userInputElement.classList.add("userInputBubble");
  userInputElement.classList.add("bubble");
  userInputElement.insertAdjacentText("afterbegin", userInput);
  conversationArea.append(userInputElement);
  websocket.send(userInput);
}
