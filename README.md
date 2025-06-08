# Digital Postal Index Number (DIGIPIN) CLI Tool

## 🚀 Introduction

This repository contains a Python Command Line Interface (CLI) tool for working with the Digital Postal Index Number (DIGIPIN), a standardized, geo-coded addressing system initiative by the Department of Posts, Government of India.

The DIGIPIN system divides India's geographical territory into uniform 4-meter by 4-meter (approx.) units, each assigned a unique 10-digit alphanumeric code derived from its latitude and longitude coordinates. This tool allows you to:

- **Encode** geographic coordinates (latitude and longitude) into a DIGIPIN
- **Decode** a DIGIPIN back into its central latitude and longitude

## 🙏 Credits

This implementation is based on the technical specifications and logic outlined in the **Digital Postal Index Number (DIGIPIN) - National Level Addressing Grid (Technical Document – Final version)** released by the Ministry of Communications, Department of Posts, Government of India.

The original DIGIPIN initiative was undertaken by the Department of Posts in collaboration with **IIT Hyderabad** and **NRSC, ISRO**. Full credit for the design and concept of DIGIPIN goes to these esteemed organizations.

## 🤖 AI Assistance

This specific some code and README.md file were generated with the assistance of an AI. 

## ✨ Features

- **encode**: Convert latitude and longitude coordinates into a DIGIPIN code
- **decode**: Convert a DIGIPIN code back into its approximate central latitude and longitude
- **Validation**: Includes basic validation for input coordinates and DIGIPIN formats

## 💻 Installation

1. Clone this repository (or simply download the `digipin_cli.py` file):

```bash
git clone https://github.com/AngshuCode/DIGIPIN.git
cd DIGIPIN
```


2. No external Python libraries are strictly required beyond standard built-in modules (`math`, `argparse`). Ensure you have Python 3 installed.

## 🚀 Usage

You can run the `digipin_cli.py` script directly from your terminal.

```--- India DIGIPIN Tool ---
1. Encode Latitude and Longitude to DIGIPIN
2. Decode DIGIPIN to Latitude and Longitude
3. Exit
----------------------------
Enter your choice (1, 2, or 3):
```
Enter the number corresponding to your desired action and press Enter.
Encoding Coordinates to DIGIPIN
 * From the main menu, enter 1.
 * The tool will prompt you for the Latitude and Longitude.
   * Example Latitude: 28.622788 (for Dak Bhawan)
   * Example Longitude: 77.213033 (for Dak Bhawan)
   Enter your choice (1, 2, or 3): 1
Enter Latitude (e.g., 28.622788): 28.622788
Enter Longitude (e.g., 77.213033): 77.213033

Resulting DIGIPIN: 39J-49L-L8T4

Decoding a DIGIPIN to Coordinates
 * From the main menu, enter 2.
 * The tool will prompt you for the DIGIPIN code. You can enter the code with or without hyphens.
   * Example DIGIPIN: 39J-49L-L8T4 or 39J49LL8T4
   Enter your choice (1, 2, or 3): 2
Enter DIGIPIN (e.g., '39J-49L-L8T4' or '39J49LL8T4'): 39J-49L-L8T4

Decoded Latitude: 28.622788
Decoded Longitude: 77.213033

Exiting the Tool
 * From the main menu, enter 3.
   Enter your choice (1, 2, or 3): 3
Exiting India DIGIPIN Tool. Goodbye!


## 🛠️ How It Works (Core Logic)

The core logic within `digipin_cli.py` directly translates the encoding and decoding algorithms defined in the official DIGIPIN technical document, including:

- **Bounding Box**: The geographical extent of India (Longitude 63.5° – 99.5° East, Latitude 2.5° – 38.5° North)
- **Hierarchical Grid**: Dividing the area into 16 (4x4) regions at each of 10 levels
- **Alphanumeric Symbols**: Using the specified 16 characters (2, 3, 4, 5, 6, 7, 8, 9, C, J, K, L, M, P, F, T) for encoding
- **Spiral Labeling**: The specific anti-clockwise spiraling pattern for assigning symbols within each 4x4 grid
- **Coordinate-to-Code Mapping**: Precise calculations to map latitude and longitude to the correct grid cell at each level
- **Code-to-Coordinate Mapping**: Reverse calculations to determine the central point of a given DIGIPIN's cell

## 📁 Project Structure

```
digipin/
├── digipin_cli.py          # Main CLI application
├── readme.md               # This file
└── requirements.txt        # Python dependencies (if any)
```

## 🧪 Testing

To test the tool with known coordinates:

```bash
# Test encoding
python digipin_cli.py encode 28.622788 77.213033

# Test decoding
python digipin_cli.py decode 39J-49L-L8T4
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

As per the original DIGIPIN initiative, this tool is intended to be open-source and freely available for public use. While a specific license for this repository is not explicitly stated here, it aligns with the spirit of public digital infrastructure.

**Note**: This tool is an independent implementation based on publicly available technical specifications. It is not officially endorsed by the Department of Posts, Government of India.
