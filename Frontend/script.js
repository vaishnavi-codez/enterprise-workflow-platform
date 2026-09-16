
const API_BASE_URL = "http://127.0.0.1:8000";


// =====================================================
// STATE
// =====================================================

let accessToken = localStorage.getItem("access_token");
let currentUsername = localStorage.getItem("username");
let currentSessionId = null;

let conversations = [];


// =====================================================
// ELEMENTS
// =====================================================

const welcomeScreen = document.getElementById("welcomeScreen");
const authScreen = document.getElementById("authScreen");
const appScreen = document.getElementById("appScreen");

const registerView = document.getElementById("registerView");
const loginView = document.getElementById("loginView");

const dashboardView = document.getElementById("dashboardView");
const chatView = document.getElementById("chatView");

const loadingOverlay = document.getElementById("loadingOverlay");


// =====================================================
// AUTH ELEMENTS
// =====================================================

const registerUsername =
    document.getElementById("registerUsername");

const registerPassword =
    document.getElementById("registerPassword");

const loginUsername =
    document.getElementById("loginUsername");

const loginPassword =
    document.getElementById("loginPassword");

const registerMessage =
    document.getElementById("registerMessage");

const loginMessage =
    document.getElementById("loginMessage");


// =====================================================
// APP ELEMENTS
// =====================================================

const currentUsernameElement =
    document.getElementById("currentUsername");

const welcomeName =
    document.getElementById("welcomeName");

const userAvatar =
    document.getElementById("userAvatar");

const conversationList =
    document.getElementById("conversationList");

const dashboardQuestion =
    document.getElementById("dashboardQuestion");

const chatQuestion =
    document.getElementById("chatQuestion");

const chatMessages =
    document.getElementById("chatMessages");


// =====================================================
// USER-SPECIFIC CONVERSATION STORAGE
// =====================================================

function getConversationStorageKey(username) {

    if (!username) {
        return null;
    }

    return `conversations_${username.trim().toLowerCase()}`;
}


function loadUserConversations() {

    if (!currentUsername) {

        conversations = [];

        return;
    }

    const storageKey =
        getConversationStorageKey(currentUsername);

    try {

        conversations =
            JSON.parse(
                localStorage.getItem(storageKey) || "[]"
            );

        if (!Array.isArray(conversations)) {
            conversations = [];
        }

    } catch (error) {

        conversations = [];
    }
}


function saveUserConversations() {

    if (!currentUsername) {
        return;
    }

    const storageKey =
        getConversationStorageKey(currentUsername);

    localStorage.setItem(
        storageKey,
        JSON.stringify(conversations)
    );
}


// =====================================================
// SCREEN FUNCTIONS
// =====================================================

function showWelcome() {

    welcomeScreen.classList.remove("hidden");
    authScreen.classList.add("hidden");
    appScreen.classList.add("hidden");
}


function showAuth() {

    welcomeScreen.classList.add("hidden");
    authScreen.classList.remove("hidden");
    appScreen.classList.add("hidden");
}


function showApp() {

    welcomeScreen.classList.add("hidden");
    authScreen.classList.add("hidden");
    appScreen.classList.remove("hidden");

    currentUsernameElement.textContent =
        currentUsername || "User";

    welcomeName.textContent =
        currentUsername || "Welcome";

    userAvatar.textContent =
        (currentUsername || "U")
        .charAt(0)
        .toUpperCase();

    // Load only this user's conversations
    loadUserConversations();

    showDashboard();

    renderConversations();
}


function showDashboard() {

    dashboardView.classList.remove("hidden");
    chatView.classList.add("hidden");
}


function showChat() {

    dashboardView.classList.add("hidden");
    chatView.classList.remove("hidden");

    chatQuestion.focus();
}


// =====================================================
// INITIAL STATE
// =====================================================

if (accessToken && currentUsername) {

    showApp();

} else {

    showWelcome();
}


// =====================================================
// GET STARTED
// =====================================================

document
    .getElementById("getStartedBtn")
    .addEventListener("click", () => {

        showAuth();

        registerView.classList.remove("hidden");
        loginView.classList.add("hidden");

    });


// =====================================================
// SWITCH REGISTER / LOGIN
// =====================================================

document
    .getElementById("showLoginBtn")
    .addEventListener("click", () => {

        registerView.classList.add("hidden");
        loginView.classList.remove("hidden");

        loginUsername.focus();
    });


document
    .getElementById("showRegisterBtn")
    .addEventListener("click", () => {

        loginView.classList.add("hidden");
        registerView.classList.remove("hidden");

        registerUsername.focus();
    });


// =====================================================
// REGISTER
// =====================================================

document
    .getElementById("registerBtn")
    .addEventListener("click", async () => {

        const username =
            registerUsername.value.trim();

        const password =
            registerPassword.value;

        registerMessage.textContent = "";

        if (!username || !password) {

            registerMessage.textContent =
                "Please enter a username and password.";

            return;
        }

        try {

            const response = await fetch(
                `${API_BASE_URL}/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        username,
                        password
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail || "Registration failed."
                );
            }

            loginUsername.value = username;

            registerMessage.textContent =
                "Account created successfully.";

            setTimeout(() => {

                registerView.classList.add("hidden");
                loginView.classList.remove("hidden");

                loginUsername.focus();

            }, 600);

        } catch (error) {

            registerMessage.textContent =
                error.message;
        }
    });


// =====================================================
// LOGIN
// =====================================================

document
    .getElementById("loginBtn")
    .addEventListener("click", async () => {

        const username =
            loginUsername.value.trim();

        const password =
            loginPassword.value;

        loginMessage.textContent = "";

        if (!username || !password) {

            loginMessage.textContent =
                "Please enter a username and password.";

            return;
        }

        try {

            const response = await fetch(
                `${API_BASE_URL}/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        username,
                        password
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail || "Login failed."
                );
            }

            accessToken =
                data.access_token;

            currentUsername =
                username;

            localStorage.setItem(
                "access_token",
                accessToken
            );

            localStorage.setItem(
                "username",
                currentUsername
            );

            // Load only the logged-in user's conversations
            loadUserConversations();

            // Always start with a fresh frontend session
            currentSessionId = null;

            loginPassword.value = "";

            showApp();

        } catch (error) {

            loginMessage.textContent =
                error.message;
        }
    });


// =====================================================
// LOGOUT
// =====================================================

document
    .getElementById("logoutBtn")
    .addEventListener("click", () => {

        localStorage.removeItem("access_token");
        localStorage.removeItem("username");

        accessToken = null;
        currentUsername = null;
        currentSessionId = null;

        // Clear the current user's conversations from memory
        conversations = [];

        showWelcome();
    });


// =====================================================
// START NEW CHAT
// =====================================================

function startNewChat() {

    currentSessionId = null;

    chatMessages.innerHTML = `
        <div class="empty-chat">

            <div class="empty-chat-mark">
                AD
            </div>

            <h2>How can I help you?</h2>

            <p>
                Ask a question and let the multi-agent system
                research, analyze and make a decision.
            </p>

        </div>
    `;

    chatQuestion.value = "";

    showChat();
}


document
    .getElementById("newChatBtn")
    .addEventListener("click", startNewChat);


document
    .getElementById("chatNewBtn")
    .addEventListener("click", startNewChat);


// =====================================================
// DASHBOARD ASK
// =====================================================

document
    .getElementById("dashboardAskBtn")
    .addEventListener("click", () => {

        const question =
            dashboardQuestion.value.trim();

        if (!question) {

            dashboardQuestion.focus();

            return;
        }

        startNewChat();

        chatQuestion.value = question;

        sendQuestion();

    });


// =====================================================
// SUGGESTION CARDS
// =====================================================

document
    .querySelectorAll(".suggestion-card")
    .forEach(card => {

        card.addEventListener("click", () => {

            const question =
                card.dataset.question;

            startNewChat();

            chatQuestion.value =
                question;

            sendQuestion();
        });
    });


// =====================================================
// BACK TO DASHBOARD
// =====================================================

document
    .getElementById("backToDashboardBtn")
    .addEventListener("click", () => {

        showDashboard();
    });


// =====================================================
// SEND CHAT MESSAGE
// =====================================================

document
    .getElementById("sendChatBtn")
    .addEventListener("click", sendQuestion);


chatQuestion.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendQuestion();
        }
    }
);


// =====================================================
// SEND QUESTION TO FASTAPI
// =====================================================

async function sendQuestion() {

    const question =
        chatQuestion.value.trim();

    if (!question) {
        return;
    }

    if (!accessToken) {

        showAuth();

        return;
    }

    addUserMessage(question);

    chatQuestion.value = "";

    showLoading(true);

    try {

        const response = await fetch(
            `${API_BASE_URL}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",

                    "Authorization":
                        `Bearer ${accessToken}`
                },

                body: JSON.stringify({

                    question: question,

                    session_id:
                        currentSessionId
                })
            }
        );

        const data =
            await response.json();

        if (!response.ok) {

            if (response.status === 401) {

                localStorage.removeItem(
                    "access_token"
                );

                accessToken = null;

                currentSessionId = null;

                throw new Error(
                    "Your session has expired. Please sign in again."
                );
            }

            throw new Error(
                data.detail ||
                "Unable to process your request."
            );
        }

        currentSessionId =
            data.session_id;

        addAIMessage(data.response);

        saveConversation(question);

    } catch (error) {

        addAIMessage(
            `Unable to complete the request.\n\n${error.message}`
        );

    } finally {

        showLoading(false);
    }
}


// =====================================================
// CHAT MESSAGES
// =====================================================

function addUserMessage(message) {

    removeEmptyChat();

    const wrapper =
        document.createElement("div");

    wrapper.className =
        "message-row user-message";

    wrapper.innerHTML = `
        <div class="message-label">
            YOU
        </div>

        <div class="message-content">
            ${escapeHTML(message)}
        </div>
    `;

    chatMessages.appendChild(wrapper);

    scrollChatToBottom();
}


function addAIMessage(message) {

    removeEmptyChat();

    const wrapper =
        document.createElement("div");

    wrapper.className =
        "message-row ai-message";

    wrapper.innerHTML = `
        <div class="message-label">
            AI AGENT
        </div>

        <div class="message-content">
            ${escapeHTML(message)}
        </div>
    `;

    chatMessages.appendChild(wrapper);

    scrollChatToBottom();
}


function removeEmptyChat() {

    const empty =
        chatMessages.querySelector(
            ".empty-chat"
        );

    if (empty) {
        empty.remove();
    }
}


function scrollChatToBottom() {

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// =====================================================
// CONVERSATION LIST
// =====================================================

function saveConversation(question) {

    if (!currentUsername) {
        return;
    }

    conversations.unshift({

        question: question,

        sessionId: currentSessionId,

        createdAt:
            new Date().toLocaleString()

    });

    conversations =
        conversations.slice(0, 8);

    // Save only under the currently logged-in user
    saveUserConversations();

    renderConversations();
}


function renderConversations() {

    if (!conversations.length) {

        conversationList.innerHTML = `
            <div class="empty-conversations">
                No conversations yet
            </div>
        `;

        return;
    }

    conversationList.innerHTML = "";

    conversations.forEach(item => {

        const element =
            document.createElement("div");

        element.className =
            "conversation-item";

        element.textContent =
            item.question;

        element.title =
            item.question;

        conversationList.appendChild(element);
    });
}


// =====================================================
// LOADING
// =====================================================

function showLoading(show) {

    if (show) {

        loadingOverlay.classList.remove(
            "hidden"
        );

    } else {

        loadingOverlay.classList.add(
            "hidden"
        );
    }
}


// =====================================================
// SECURITY
// =====================================================

function escapeHTML(value) {

    return value
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
