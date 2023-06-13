import serial
import matplotlib.pyplot as plt
import math
import csv
import time

# for logging
BUFFER_SIZE = 100
buffer = []

LOG_NAME = "MADDY.CSV"

# Establish a Bluetooth serial connection
ser = serial.Serial('COM3', 115200)  # port

# Create empty lists to store accelerometer data
timestamps = []
x_values = []
y_values = []
g_forces = []

# Constants for static acceleration compensation and sensor drift
static_x = 0.0054  # Adjust to static x-axis reading
static_y = 0.0059  # Adjust to static y-axis reading

# Create a figure and axis for plotting
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, polar=True)

# Rotate the graph so that 0 degrees is at the top
ax.set_theta_zero_location('N')

# Configure the plot
ax.set_ylim(0, 0.6)  # Set constant y-axis limit
ax.set_yticklabels([])

# Create a marker for indicating the current g-force
marker, = ax.plot([0], [0], marker='o', markersize=12, color='red')  # Adjust red markersize

TIME_SET = -1
calibrationData = -1

while True:
    if TIME_SET == -1: # setup
        TIME_SET = time.time()  # T+ time offset

    if ser.in_waiting > 0:
        line = ser.readline().decode().strip()
        if line:
            # Split the received line into individual values
            values = line.split(',')

            print("Received:", values)

            # Extract the accelerometer data
            timestamp = str(int(values[0])) + "-" + str(int(values[1])) + "-" + str(int(values[2]))  + "@" + str(int(values[3]))  + ":" + str(int(values[4]))  + ":" + str(int(values[5]))
            x = float(values[6]) - static_x
            y = float(values[7]) - static_y
            g_force = math.sqrt(x ** 2 + y ** 2)

            # Add the data to the lists
            #timestamps.append(timestamp)
            x_values.append(x)
            y_values.append(y)
            g_forces.append(g_force)

            # Convert the g-force magnitude to degrees for polar plot
            angle = math.degrees(math.atan2(y, x))
            if angle < 0:
                angle += 360

            # Invert the angle (reflect over the y-axis)
            angle = (180 - angle) % 360

            # Update the plot with the new data
            marker.set_data(math.radians(angle), g_force)  # Invert the x-axis

            # Pause to allow time for the plot to update
            plt.pause(0.001)

            # Add the data to the buffer
            buffer.append([timestamp, x, y, g_force, angle])

            # If the buffer is full, write the data to the CSV file and clear the buffer
            if len(buffer) >= BUFFER_SIZE:
                with open(LOG_NAME, 'a', newline='') as f:
                    writer = csv.writer(f)
                    buffer.append(["++++", TIME_SET, time.time()]) # write time offsets periodically, [ , start, current]
                    writer.writerows(buffer)
                buffer.clear()



# Invert the x-axis
ax.set_theta_direction(-1)

# Close the Bluetooth connection
ser.close()

# Show the final plot
plt.show()

# Write any remaining data in the buffer
if buffer:
    with open(LOG_NAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(buffer)
