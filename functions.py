def interpret_air_quality(aqdata):
    """
    Interprets the air quality based on the PM2.5 concentration (µg/m³)
    and returns a user-friendly string.
    """
    pm25 = aqdata.get("pm25 standard")
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
    Returns a formatted string showing particle count information.
    """
    keys = [
        "particles 03um",
        "particles 05um",
        "particles 10um",
        "particles 25um",
        "particles 50um",
        "particles 100um"
    ]
    parts = []
    for key in keys:
        value = aqdata.get(key, "N/A")
        parts.append(f"{key}: {value}")
    return "\n".join(parts)