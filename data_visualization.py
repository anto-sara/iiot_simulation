import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

# Create a directory for saving visualizations
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')

# Initialize data storage
data = []
plt.ion()  # Enable interactive mode
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle('Real-time Sensor Data Visualization')

# MQTT callback when a message is received
def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        sensor_data = json.loads(payload)
        timestamp = datetime.now()
        
        # Store data
        data.append((timestamp, sensor_data["temperature"], sensor_data["humidity"]))
        
        # Keep only the last 100 data points
        if len(data) > 100:
            data.pop(0)
            
        # Convert to DataFrame for easier plotting
        df = pd.DataFrame(data, columns=["timestamp", "temperature", "humidity"])
        
        # Clear previous plots
        ax1.clear()
        ax2.clear()
        
        # Plot temperature
        ax1.plot(df["timestamp"], df["temperature"], 'r-', label="Temperature (°C)")
        ax1.set_ylabel('Temperature (°C)')
        ax1.set_title('Temperature over Time')
        ax1.grid(True)
        ax1.legend()
        
        # Plot humidity
        ax2.plot(df["timestamp"], df["humidity"], 'b-', label="Humidity (%)")
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Humidity (%)')
        ax2.set_title('Humidity over Time')
        ax2.grid(True)
        ax2.legend()
        
        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        
        # Update the plot
        plt.draw()
        plt.pause(0.1)
        
        # Save the visualization periodically (every 50 data points)
        if len(data) % 50 == 0:
            plt.savefig(f'visualizations/mqtt_visualization_{len(data)}.png')
            print(f"Visualization saved to visualizations/mqtt_visualization_{len(data)}.png")
            
    except Exception as e:
        print(f"Error processing message: {e}")

# Set up MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to the broker
try:
    client.connect("localhost", 1883)
    client.subscribe("sensor/data")
    print("Connected to MQTT broker, waiting for data...")
    
    # Start the MQTT client loop
    client.loop_start()
    
    # Keep the script running
    plt.show(block=True)
    
except KeyboardInterrupt:
    print("Visualization stopped by user")
except Exception as e:
    print(f"Error: {e}")
finally:
    client.loop_stop()
    plt.savefig('visualizations/final_visualization.png')
    print("Final visualization saved to visualizations/final_visualization.png")