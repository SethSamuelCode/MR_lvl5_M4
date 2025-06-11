"use strict";

// Backend server URL for API endpoints
const BACKEND_SERVER = "http://localhost:8000";

// Get references to DOM elements for user interaction
const conversationArea = document.querySelector("#convoDisplayArea");
const userInputForm = document.querySelector("#userInputForm");
const userTextInputArea = document.querySelector("#userInput");
const sendButton = document.querySelector("#sendButton");
const loadingDot = document.querySelector("#loadingDot")

// Set up WebSocket communication handler
userInputForm.addEventListener("submit", sendViaWebsocket);

// Global WebSocket connection variable
let websocket;

// Initialize the application when the window loads
window.onload = async () => {
    // Initialize WebSocket connection to backend server
    websocket = new WebSocket(`${BACKEND_SERVER}/ws`);
    
    // Handle incoming messages from the WebSocket server
    websocket.onmessage = (event) => {
        console.log(JSON.parse(event.data));
        const incomingMessage = JSON.parse(event.data);
        
        // Enable the send button after receiving first message (Tina's introduction)
        sendButton.removeAttribute("disabled");
        
        // Create and style AI response message bubble
        const aiResponseElement = document.createElement("p");
        aiResponseElement.classList.add("aiResponseBubble", "bubble");
        aiResponseElement.insertAdjacentText("afterbegin", incomingMessage.message);
        conversationArea.append(aiResponseElement);
        waitAnimationHide()
    };
    
    console.log("WebSocket connection initialized");
};

// Legacy HTTP POST-based chat function (currently unused)
async function sendToAI(e) {
  //first time this func is executed there is no event to opperate on
  if (e) {
    e.preventDefault();
  }
  // Get user input and clear the input field
  const userInput = userTextInputArea.value || " ";
  console.log(userInput);
  userTextInputArea.value = "";

    // Configure HTTP POST request options
    const fetchOptions = {
        method: "post",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            uuid: SESSION_UUID.value,
            message: userInput,
        }),
    };

    // Only display user message bubble if not the first message
    if (e) {
        const userInputElement = document.createElement("p");
        userInputElement.classList.add("userInputBubble", "bubble");
        userInputElement.insertAdjacentText("afterbegin", userInput);
        conversationArea.append(userInputElement);
    }

    // Send request to backend and handle AI response
    const aiResponse = await fetch(`${BACKEND_SERVER}/api/chat`, fetchOptions);
    const aiText = await aiResponse.json();
    console.log(aiText);

    // Create and display AI response bubble
    const aiResponseElement = document.createElement("p");
    aiResponseElement.classList.add("aiResponseBubble", "bubble");
    aiResponseElement.insertAdjacentText("afterbegin", aiText);
    conversationArea.append(aiResponseElement);
}

// Handle WebSocket-based message sending
async function sendViaWebsocket(e) {
    // Prevent default form submission
    e.preventDefault();
    
    // Get user input and clear the input field
    const userInput = userTextInputArea.value || " ";
    userTextInputArea.value = "";
    
    // Create and display user message bubble
    const userInputElement = document.createElement("p");
    userInputElement.classList.add("userInputBubble", "bubble");
    userInputElement.insertAdjacentText("afterbegin", userInput);
    conversationArea.append(userInputElement);
    
    // Send message through WebSocket connection
    websocket.send(userInput);
    waitAnimationShow()
}

function waitAnimationHide(){
  loadingDot.style.opacity=0;
}
function waitAnimationShow(){
  loadingDot.style.opacity=1;

}