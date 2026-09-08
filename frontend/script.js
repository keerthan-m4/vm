const API = "https://virtual-mouse-backend-1qfe.onrender.com";

async function startMouse() {
    try {
        const response = await fetch(`${API}/start`, {
            method: "POST"
        });

        const data = await response.json();

        document.getElementById("status").innerText = "Running 🟢";

    } catch (error) {
        document.getElementById("status").innerText =
            "Python Agent Offline 🔴";
    }
}

async function stopMouse() {
    try {
        const response = await fetch(`${API}/stop`, {
            method: "POST"
        });

        const data = await response.json();

        document.getElementById("status").innerText = "Stopped 🔴";

    } catch (error) {
        document.getElementById("status").innerText =
            "Python Agent Offline 🔴";
    }
}

async function checkStatus() {
    try {
        const response = await fetch(`${API}/status`);
        const data = await response.json();

        document.getElementById("status").innerText =
            data.running ? "Running 🟢" : "Stopped 🔴";

    } catch (error) {
        document.getElementById("status").innerText =
            "Python Agent Offline 🔴";
    }
}

setInterval(checkStatus, 2000);

checkStatus();