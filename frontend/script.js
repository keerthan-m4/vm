const API = "http://127.0.0.1:5000";

async function startMouse() {
    try {
        await fetch(`${API}/start`, {
            method: "POST"
        });

        checkStatus();
    } catch (error) {
        document.getElementById("status").innerText =
            "Python Agent Offline 🔴";
    }
}

async function stopMouse() {
    try {
        await fetch(`${API}/stop`, {
            method: "POST"
        });

        checkStatus();
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