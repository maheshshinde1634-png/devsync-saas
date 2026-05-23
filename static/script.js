// 1. Sticky Navigation Effect
const navbar = document.getElementById("navbar");
window.addEventListener("scroll", () => {
  if (window.scrollY > 50) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
});

// 2. Toast Notification System
const toastContainer = document.getElementById("toastContainer");
function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerText = message;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.4s ease";
    setTimeout(() => toast.remove(), 400);
  }, 4000);
}

// 3. MySQL Database Async Form Submission
const leadForm = document.getElementById("leadForm");
const emailInput = document.getElementById("heroEmail");
const submitBtn = document.getElementById("submitBtn");
const btnSpinner = document.getElementById("btnSpinner");

leadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const emailValue = emailInput.value.trim();
  if (!emailValue) return;

  submitBtn.disabled = true;
  btnSpinner.classList.remove("hidden");

  try {
    const response = await fetch("/api/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: emailValue }),
    });

    const data = await response.json();
    if (response.ok) {
      showToast(data.message, "success");
      leadForm.reset();
      // Add custom success log to the terminal mockup
      addTerminalLine(
        `> User ${emailValue} added to MySQL DB.`,
        "terminal-success",
      );
    } else {
      showToast(data.message, "error");
      addTerminalLine(`> Error: ${data.message}`, "terminal-warning");
    }
  } catch (error) {
    showToast("Unable to reach the server.", "error");
  } finally {
    submitBtn.disabled = false;
    btnSpinner.classList.add("hidden");
  }
});

// 4. Dynamic Python Terminal Animation
const terminalLogs = [
  "$ python manage.py runserver",
  " * Serving Flask app 'DevSync'",
  " * Debug mode: on",
  " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)",
  "> Checking MySQL Connection...",
  "<span class='terminal-success'>> Connected to devsync_db successfully.</span>",
  "> Awaiting connections...",
];

const terminalContainer = document.getElementById("pythonTerminal");
let logIndex = 0;

function addTerminalLine(text, customClass = "") {
  // Remove existing cursor
  const oldCursor = document.querySelector(".cursor");
  if (oldCursor) oldCursor.remove();

  const line = document.createElement("div");
  line.className = `terminal-line ${customClass}`;
  line.innerHTML = text;
  terminalContainer.appendChild(line);

  // Add cursor to the new line
  const cursor = document.createElement("span");
  cursor.className = "cursor";
  terminalContainer.appendChild(cursor);

  // Auto scroll to bottom
  terminalContainer.scrollTop = terminalContainer.scrollHeight;
}

function typeTerminal() {
  if (logIndex < terminalLogs.length) {
    addTerminalLine(terminalLogs[logIndex]);
    logIndex++;
    // Random delay between 400ms and 1200ms for realistic typing feel
    setTimeout(typeTerminal, Math.random() * 800 + 400);
  }
}

// Start terminal animation after 500ms
setTimeout(typeTerminal, 500);
