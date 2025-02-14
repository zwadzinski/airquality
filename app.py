#import streamlit as streamlit
import time
import adafruit_sgp40
import board
import busio
# Import the BitBangIO version for software I2C
import adafruit_bitbangio as bitbangio
from adafruit_pm25.i2c import PM25_I2C
from adafruit_sgp40 import SGP40  
import streamlit as st

#rpi login:
# username: airquality
# password: pumpkins
# venv: source venv/bin/activate


# Function to read from the PMSA003 particulate matter sensor
# Using the pms5003 library which is compatible with many PMS sensors



def read_pmsa003_i2c():
    """
    Reads data from the PM2.5 sensor over hardware I2C.
    Returns a dictionary of sensor readings, or an error string.
    """
    try:
        i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
        reset_pin = None  # Change this if you've connected a GPIO to the sensor's RESET pin
        pm25 = PM25_I2C(i2c, reset_pin)
        aqdata = pm25.read()
        return aqdata
    except Exception as e:
        return f"Error reading PMSA003: {e}"

def interpret_air_quality(aqdata):
    """
    Interprets the air quality based on the PM2.5 concentration (µg/m³)
    and returns a friendly string.
    """
    pm25 = aqdata.get("pm25 standard", None)
    if pm25 is None:
        return "PM2.5 data not available."
    if pm25 <= 12.0:
        quality = "Good"
    elif pm25 <= 35.4:
        quality = "Moderate"
    elif pm25 <= 55.4:
        quality = "Unhealthy for Sensitive Groups"
    elif pm25 <= 150.4:
        quality = "Unhealthy"
    elif pm25 <= 250.4:
        quality = "Very Unhealthy"
    else:
        quality = "Hazardous"
    return f"PM2.5: {pm25} µg/m³  -->  Air Quality is {quality}."

def display_particle_counts(aqdata):
    """
    Returns a formatted string showing various particle count values.
    """
    parts = []
    keys = [
        "particles 03um",
        "particles 05um",
        "particles 10um",
        "particles 25um",
        "particles 50um",
        "particles 100um"
    ]
    for key in keys:
        value = aqdata.get(key, "N/A")
        parts.append(f"{key}: {value}")
    return "\n".join(parts)

# Create a software I2C bus on alternative GPIO pins using BitBangIO.
# For example, we choose GPIO17 for SDA and GPIO27 for SCL.
# i2c_sw = bitbangio.I2C(board.D17, board.D27)

# Initialize the SGP40 VOC sensor on the software I2C bus.
# sgp40_sw = SGP40(i2c_sw)

# def read_sgp40_sw():
#     try:
#         # Read a raw VOC value from the sensor.
#         voc = sgp40_sw.measure_raw()
#         return voc
#     except Exception as e:
#         return f"Error reading SGP40 on software I2C: {e}"

def main():
    print("Starting Air Quality Monitor...\n")
    while True:
        aqdata = read_pmsa003_i2c()
        if isinstance(aqdata, dict):
            print("===================================")
            print("Air Quality Reading:")
            # Output a summary message based on PM2.5
            print(interpret_air_quality(aqdata))
            print("\nOther Measurements:")
            # Output additional particle counts
            print(display_particle_counts(aqdata))
            print("===================================\n")
        else:
            # If there was an error reading the sensor, display it.
            print(aqdata)
        
        # voc = read_sgp40_sw()
        # print("SGP40 VOC Sensor Raw Value:", voc)
        
        # Wait for 5 seconds before taking another reading.
        time.sleep(5)

# Streamlit app code starts here
st.title("Air Quality Monitor")

# Get the latest sensor data
aqdata = read_pmsa003_i2c()

if isinstance(aqdata, dict):
    st.header("Air Quality Reading")
    st.write(interpret_air_quality(aqdata))
    st.subheader("Other Measurements")
    st.text(display_particle_counts(aqdata))
else:
    st.error(aqdata)

# Add a refresh button that, when clicked, forces the app to rerun
if st.button("Refresh"):
    st.experimental_rerun()

if __name__ == "__main__":
    main()