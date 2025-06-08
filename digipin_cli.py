import math
import sys # Import sys for exiting the program

# DIGIPIN Encoder and Decoder Library
# Developed by India Post, Department of Posts
# Released under an open-source license for public use

# This module contains the core functions for encoding/decoding DIGIPINs,
# and integrates a command-line interface for easy use.

DIGIPIN_GRID = [
    ['F', 'C', '9', '8'],
    ['J', '3', '2', '7'],
    ['K', '4', '5', '6'],
    ['L', 'M', 'P', 'T']
]

BOUNDS = {
    'minLat': 2.5,
    'maxLat': 38.5,
    'minLon': 63.5,
    'maxLon': 99.5
}

def get_digipin(lat: float, lon: float) -> str:
    """
    Encodes latitude and longitude into a 10-digit alphanumeric DIGIPIN.

    Args:
        lat (float): Latitude coordinate.
        lon (float): Longitude coordinate.

    Returns:
        str: The 10-digit DIGIPIN code.

    Raises:
        ValueError: If latitude or longitude is out of the defined bounds.
    """
    if not (BOUNDS['minLat'] <= lat <= BOUNDS['maxLat']):
        raise ValueError(f'Latitude {lat} out of range ({BOUNDS["minLat"]} to {BOUNDS["maxLat"]})')
    if not (BOUNDS['minLon'] <= lon <= BOUNDS['maxLon']):
        raise ValueError(f'Longitude {lon} out of range ({BOUNDS["minLon"]} to {BOUNDS["maxLon"]})')

    min_lat = BOUNDS['minLat']
    max_lat = BOUNDS['maxLat']
    min_lon = BOUNDS['minLon']
    max_lon = BOUNDS['maxLon']

    digi_pin_chars = []

    for level in range(1, 11):  # Levels 1 to 10
        lat_div = (max_lat - min_lat) / 4
        lon_div = (max_lon - min_lon) / 4

        # Calculate row and column indices based on the JS logic:
        # row is 3 - floor(...), which means row 0 corresponds to the highest latitude block
        row = 3 - math.floor((lat - min_lat) / lat_div)
        col = math.floor((lon - min_lon) / lon_div)

        # Ensure indices are within [0, 3]
        row = max(0, min(row, 3))
        col = max(0, min(col, 3))

        digi_pin_chars.append(DIGIPIN_GRID[row][col])

        # Add hyphen separators as per JS logic (after 3rd and 6th characters)
        if level == 3 or level == 6:
            digi_pin_chars.append('-')

        # Update bounds for the next level, mirroring the JS logic's handling of latitude
        # The JS effectively calculates the new minLat and maxLat for the selected row:
        # new_min_lat is the lower bound of the chosen row's latitude range
        # new_max_lat is the upper bound of the chosen row's latitude range
        temp_max_lat = min_lat + lat_div * (4 - row)
        temp_min_lat = min_lat + lat_div * (3 - row)
        
        min_lat = temp_min_lat
        max_lat = temp_max_lat

        min_lon = min_lon + lon_div * col
        max_lon = min_lon + lon_div

    return "".join(digi_pin_chars)

def get_lat_lng_from_digi_pin(digi_pin: str) -> dict:
    """
    Decodes a DIGIPIN back into its central latitude and longitude.

    Args:
        digi_pin (str): The 10-digit DIGIPIN code (can include hyphens).

    Returns:
        dict: A dictionary containing 'latitude' and 'longitude' (as strings,
              formatted to 6 decimal places).

    Raises:
        ValueError: If the DIGIPIN is invalid (wrong length or invalid characters).
    """
    pin_cleaned = digi_pin.replace('-', '')
    if len(pin_cleaned) != 10:
        raise ValueError(f'Invalid DIGIPIN: Expected 10 alphanumeric characters, got {len(pin_cleaned)} (after removing hyphens).')

    min_lat = BOUNDS['minLat']
    max_lat = BOUNDS['maxLat']
    min_lon = BOUNDS['minLon']
    max_lon = BOUNDS['maxLon']

    # Create a reverse lookup map for efficiency
    grid_char_to_coords = {DIGIPIN_GRID[r][c]: (r, c) for r in range(4) for c in range(4)}

    for char_index in range(10):
        char = pin_cleaned[char_index]
        
        coords = grid_char_to_coords.get(char)
        if coords is None:
            raise ValueError(f"Invalid character '{char}' in DIGIPIN at position {char_index + 1}.")
        
        r_idx, c_idx = coords

        lat_div = (max_lat - min_lat) / 4
        lon_div = (max_lon - min_lon) / 4

        # Calculate the new bounds for the current character's cell
        # Mirroring JS logic for latitude:
        # new_min_lat is the lower bound of the chosen row's latitude range
        # new_max_lat is the upper bound of the chosen row's latitude range
        new_min_lat = max_lat - lat_div * (r_idx + 1)
        new_max_lat = max_lat - lat_div * r_idx
        
        new_min_lon = min_lon + lon_div * c_idx
        new_max_lon = min_lon + lon_div * (c_idx + 1)

        # Update bounding box for next level
        min_lat = new_min_lat
        max_lat = new_max_lat
        min_lon = new_min_lon
        max_lon = new_max_lon

    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    return {
        'latitude': f"{center_lat:.6f}",
        'longitude': f"{center_lon:.6f}"
    }

def display_menu():
    """Displays the main menu options to the user."""
    print("\n--- India DIGIPIN Tool ---")
    print("1. Encode Latitude and Longitude to DIGIPIN")
    print("2. Decode DIGIPIN to Latitude and Longitude")
    print("3. Exit")
    print("----------------------------")

def run_encoder():
    """Handles the encoding process, taking user input for latitude and longitude."""
    try:
        latitude_str = input("Enter Latitude (e.g., 28.622788): ")
        longitude_str = input("Enter Longitude (e.g., 77.213033): ")

        latitude = float(latitude_str)
        longitude = float(longitude_str)

        digipin_code = get_digipin(latitude, longitude)
        print(f"\nResulting DIGIPIN: {digipin_code}")
    except ValueError as e:
        print(f"Error: Invalid input. {e}")
    except Exception as e:
        print(f"An unexpected error occurred during encoding: {e}")

def run_decoder():
    """Handles the decoding process, taking user input for a DIGIPIN."""
    try:
        digipin_input = input("Enter DIGIPIN (e.g., '39J-49L-L8T4' or '39J49LL8T4'): ")
        coords = get_lat_lng_from_digi_pin(digipin_input)
        print(f"\nDecoded Latitude: {coords['latitude']}")
        print(f"Decoded Longitude: {coords['longitude']}")
    except ValueError as e:
        print(f"Error: Invalid input. {e}")
    except Exception as e:
        print(f"An unexpected error occurred during decoding: {e}")

def main():
    """Main function to run the interactive DIGIPIN tool."""
    while True:
        display_menu()
        choice = input("Enter your choice (1, 2, or 3): ").strip()

        if choice == '1':
            run_encoder()
        elif choice == '2':
            run_decoder()
        elif choice == '3':
            print("Exiting India DIGIPIN Tool. Goodbye!")
            sys.exit(0) # Exit the program
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

