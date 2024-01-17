import screen_brightness_control as sbc
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
from time import sleep
import ddc_ci

# Connection
port = 'COM3'
arduino = serial.Serial(port, 9600)
sleep(1)

# Plot setup
fig = plt.figure(figsize=(18, 7))
ax = fig.add_subplot(1, 2, 1)
xs = []
ys = []

ax1 = fig.add_subplot(1, 2, 2)
xs1 = []
ys1 = []

while True:
    line = arduino.readline().decode('ascii').strip()
    print(line)
    if line == 'START':
        break


# This function is called periodically from FuncAnimation
def animate(i, xs, ys, xs1, ys1):
    sensorLight = float(arduino.readline().decode('ascii').strip())

    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(sensorLight)

    # Limit x and y lists to 20 items
    xs = xs[-1200:]
    ys = ys[-1200:]

    primary = sbc.get_brightness(display=0)
    # secondary = sbc.get_brightness(display=1)

    xs1.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys1.append(primary)

    # Limit x and y lists to 20 items
    xs1 = xs1[-1200:]
    ys1 = ys1[-1200:]

    # Draw x and y lists
    ax.clear()
    plt.subplot(1, 2, 1)
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Light over time')
    plt.ylabel('Light')
    ax.xaxis.set_major_locator(plt.MaxNLocator(15))

    ax1.clear()
    plt.subplot(1, 2, 2)
    ax1.plot(xs1, ys1)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Monitor over time')
    plt.ylabel('Monitor')
    ax1.xaxis.set_major_locator(plt.MaxNLocator(15))

    light = 30 + min(sensorLight / 700 * (40), 40)

    if abs(light - primary[0]) >= 1:
        sbc.set_brightness(light)


ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, xs1, ys1), interval=30000)  # DOVREBBERO ESSERE 1 MIN
plt.show()

print("Program ended")
