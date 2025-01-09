<template>
  <div id="app" class="app-wrapper">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-container">
        <h1>Gateway Monitor</h1>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="content-wrapper">
      <div class="container">
        <h2>Gateway IP Address Viewer</h2>
        <button 
          @click="subscribeToTopic" 
          :disabled="subscribed"
          :class="{ 'btn-subscribed': subscribed }"
          class="primary-button"
        >
          {{ subscribed ? "Subscribed" : "Fetch Gateway IP Address" }}
        </button>
        
        <div v-if="ipAddress" class="ip-container">
          <div class="ip-display">
            <span class="ip-label">IP Address:</span>
            <strong>{{ ipAddress }}</strong>
          </div>
          <button @click="copyToClipboard" class="copy-btn">
            Copy
          </button>
        </div>
        
        <p v-if="!ipAddress && subscribed" class="status">
          Waiting for Gateway IP Address...
        </p>
      </div>
    </div>

    <!-- Footer -->
    <!-- <footer>
      <p>&copy; 2024 SavannaTrace IoT. All rights reserved.</p>
    </footer> -->
  </div>
</template>

<script>
import mqtt from "mqtt";

export default {
  data() {
    return {
      ipAddress: null,
      subscribed: false,
    };
  },
  methods: {
    subscribeToTopic() {
      const broker = "wss://broker.emqx.io:8084/mqtt";
      const topic = "savannaTrace/ip_address";

      const client = mqtt.connect(broker);

      client.on("connect", () => {
        console.log("Connected to MQTT broker!");
        this.subscribed = true;

        client.subscribe(topic, (err) => {
          if (err) {
            console.error("Subscription error:", err);
          } else {
            console.log(`Subscribed to topic: ${topic}`);
          }
        });
      });

      client.on("message", (receivedTopic, message) => {
        if (receivedTopic === topic) {
          this.ipAddress = message.toString();
          console.log(`Received IP address: ${this.ipAddress}`);
        }
      });

      client.on("error", (err) => {
        console.error("Connection error:", err);
      });
    },
    copyToClipboard() {
      if (this.ipAddress) {
        navigator.clipboard
          .writeText(this.ipAddress)
          .then(() => {
            alert("IP Address copied to clipboard!");
          })
          .catch((err) => {
            console.error("Failed to copy text: ", err);
          });
      }
    },
  },
};
</script>

<style>
/* Reset and Base Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: #f8fafc;
  color: #1e293b;
  line-height: 1.5;
  min-height: 100vh;
}

/* App Layout */
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
}

/* Navbar Styles */
.navbar {
  background: linear-gradient(to right, #2563eb, #3b82f6);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}

.nav-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
}

.navbar h1 {
  font-size: 1.5rem;
  font-weight: 600;
}

/* Content Styles */
.content-wrapper {
  flex: 2;
  padding: 6rem 2rem 2rem;
  background-color: #f8fafc;
  width: 100%;
  margin: 0 auto;
  
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  width: 100%;
}

h2 {
  color: #1e293b;
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  text-align: center;
}

/* Button Styles */
.primary-button {
  background-color: #2563eb;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
  display: block;
}

.primary-button:hover:not(:disabled) {
  background-color: #1d4ed8;
  transform: translateY(-1px);
}

.primary-button:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.btn-subscribed {
  background-color: #16a34a;
}

/* IP Address Display */
.ip-container {
  margin: 2rem auto 0;
  padding: 1.5rem;
  background-color: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  max-width: 800px;
}

.ip-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.ip-label {
  color: #64748b;
  font-size: 0.875rem;
}

strong {
  color: #1e293b;
  font-size: 1.125rem;
  font-family: monospace;
}

.copy-btn {
  background-color: #16a34a;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  min-width: 100px;
}

.copy-btn:hover {
  background-color: #15803d;
}

/* Status Message */
.status {
  margin-top: 1.5rem;
  text-align: center;
  color: #64748b;
  font-style: italic;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.6; }
  100% { opacity: 1; }
}

/* Footer Styles */
footer {
  background-color: #1e293b;
  color: #f8fafc;
  text-align: center;
  padding: 1rem;
  width: 100%;
}

</style>