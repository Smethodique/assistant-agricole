const backendUrl = '/api';

console.log("App.js loaded. Backend URL:", backendUrl);

// Helper to update UI
function updateElement(id, html) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = html;
    else console.error(`Element with id ${id} not found`);
}

// Fetch Weather Data
async function fetchWeather() {
    console.log("Fetching weather...");
    try {
        const response = await fetch(`${backendUrl}/predict/weather?lat=34.68&lon=-1.91`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        console.log("Weather data received:", data);
        
        const html = `
            <div style="font-size: 1rem; color: var(--primary); font-weight: bold; margin-bottom: 5px;">📍 ${data.location.city}</div>
            <div style="font-size: 0.7rem; color: #666; margin-bottom: 10px;">Lat: ${data.location.lat}, Lon: ${data.location.lon}</div>
            <div style="font-size: 1.8rem; font-weight: bold;">${data.temperature}</div>
            <div style="margin: 10px 0;">Humidity: ${data.humidity}</div>
            <div>Precipitation: ${data.precipitation}</div>
            <div style="margin-top: 10px; font-size: 0.9rem; color: #666;">
                Soil: ${data.soil_temperature}
            </div>
        `;
        updateElement('weather-data', html);
    } catch (err) {
        console.error("Weather fetch failed:", err);
        updateElement('weather-data', `<span style="color: red;">Error: ${err.message}</span>`);
    }
}

// Fetch Sensor Data
async function fetchSensors() {
    console.log("Fetching sensors...");
    try {
        const response = await fetch(`${backendUrl}/simulate/sensors`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        console.log("Sensor data received:", data);
        
        const html = data.sensors.map(sensor => `
            <div class="sensor-item">
                <span class="sensor-name">${sensor.name}</span>
                <span class="sensor-value">${sensor.value} ${sensor.unit}</span>
                <span style="font-size: 0.7rem; color: ${sensor.status === 'Optimal' ? 'green' : 'orange'}">${sensor.status}</span>
            </div>
        `).join('');
        updateElement('sensor-data', html);
    } catch (err) {
        console.error("Sensor fetch failed:", err);
        updateElement('sensor-data', `<span style="color: red;">Error: ${err.message}</span>`);
    }
}

// Handle Chat
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const messagesDiv = document.getElementById('messages');
    const recommendationDiv = document.getElementById('recommendation-content');

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const userMessage = userInput.value.trim();
            if (!userMessage) return;
            
            appendMessage('You', userMessage, 'user-message');
            userInput.value = '';
            
            try {
                const response = await fetch(`${backendUrl}/predict/rag`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: userMessage })
                });
                if (!response.ok) throw new Error('Backend error');
                const data = await response.json();
                
                appendMessage('Assistant', data.response, 'ai-message');
                if (data.recommendation || data.context) {
                    recommendationDiv.textContent = data.recommendation || "Analyzing field data...";
                }
            } catch (err) {
                appendMessage('Assistant', 'Sorry, there was a problem contacting the backend.', 'ai-message');
            }
        });
    }

    function appendMessage(sender, text, className) {
        const msg = document.createElement('div');
        msg.className = `message ${className}`;
        msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
        messagesDiv.appendChild(msg);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    // Initial Fetch
    fetchWeather();
    fetchSensors();

    // Update sensors every 10 seconds
    setInterval(fetchSensors, 10000);
    // Update weather every 10 minutes
    setInterval(fetchWeather, 600000);
});
