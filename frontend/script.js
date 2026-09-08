const API = "http://127.0.0.1:5000";
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