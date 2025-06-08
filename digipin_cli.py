import math
import argparse

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

def main():
    parser = argparse.ArgumentParser(
        description="DIGIPIN Encoder and Decoder CLI Tool",
        formatter_class=argparse.RawTextHelpFormatter # Preserve newlines in help
    )

    # Create subparsers for 'encode' and 'decode' commands
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # --- Encode Subparser ---
    encode_parser = subparsers.add_parser('encode', help='Encode latitude and longitude to a DIGIPIN.')
    encode_parser.add_argument('latitude', type=float, 
                               help='The latitude (e.g., 28.622788).')
    encode_parser.add_argument('longitude', type=float, 
                               help='The longitude (e.g., 77.213033).')

    # --- Decode Subparser ---
    decode_parser = subparsers.add_parser('decode', help='Decode a DIGIPIN to latitude and longitude.')
    decode_parser.add_argument('digipin', type=str, 
                               help='The 10-character DIGIPIN code (e.g., "39J-49L-L8T4" or "39J49LL8T4").')

    args = parser.parse_args()

    if args.command == 'encode':
        try:
            digipin_code = get_digipin(args.latitude, args.longitude)
            print(f"DIGIPIN: {digipin_code}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    elif args.command == 'decode':
        try:
            coords = get_lat_lng_from_digi_pin(args.digipin)
            print(f"Latitude: {coords['latitude']}")
            print(f"Longitude: {coords['longitude']}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()