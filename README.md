# MaxMind IPv6 EDL Generator

This project is a Python script that generates an External Dynamic List (EDL) of IPv6 network addresses for specified countries using MaxMind's GeoLite2 Country CSV database. The script can be used to block traffic from specific countries by aggregating IPv6 blocks and exporting them to an EDL file.

## Features
- Downloads the latest GeoLite2 Country CSV database from MaxMind.
- Extracts IPv6 address blocks for specified countries.
- Aggregates overlapping IPv6 prefixes for efficiency.
- Saves the consolidated IPv6 address blocks to a text file in EDL format.
- Outputs the number of lines in the generated EDL file.

## Prerequisites
- Python 3.x
- Required Python libraries:
  - `requests`
  - `netaddr`

Install the required libraries using:
```sh
pip install -r requirements.txt
```

## Setup
1. **MaxMind License Key**: You need a license key from MaxMind to download the GeoLite2 Country database. Update the `LICENSE_KEY` constant in the script with your MaxMind license key.

2. **Blocked Countries**: Update the `BLOCKED_COUNTRIES` list with the ISO codes of countries you want to block.

## Usage
1. Clone the repository or download the script.
2. Make sure all prerequisites are installed.
3. Run the script using Python:
   ```sh
   python main.py
   ```

## Script Workflow
1. **Download GeoLite2 Database**: The script downloads the latest GeoLite2 Country CSV database from MaxMind using your license key.
2. **Extract Database**: The downloaded zip file is extracted to a specified folder.
3. **Find and Parse CSV Files**: The script finds the necessary CSV files to create a mapping between GeoName IDs and country ISO codes.
4. **Extract IPv6 Blocks**: IPv6 blocks for specified blocked countries are extracted.
5. **Aggregate and Write EDL**: The extracted IPv6 blocks are aggregated, and the final list is written to `blocked_ipv6_edl.txt` in a format suitable for use as an External Dynamic List.
6. **Display Summary**: The number of entries in the output EDL file is displayed in the terminal.

## Example Output
The output file (`blocked_ipv6_edl.txt`) will look like this:
```
2400:cc40::/29 - IS
2400:cda0::/32 - IS
2001:db8::/30 - IS
```
This format includes the IPv6 block along with the corresponding country code.

## Notes
- Make sure to replace `<YOUR_LICENSE_KEY>` in the script with your actual MaxMind license key.
- This script is for educational and security purposes. It allows you to block IPv6 traffic from countries deemed risky or unwanted.
- This script checks to see if there is a ZIP file already downloaded, and uses it.  If you want to download everytime, uncomment `delete_file(ZIP_FILE)` in main().

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer
The GeoLite2 data used in this project is provided by MaxMind and is subject to the MaxMind End User License Agreement. The geolocation accuracy may vary, and it is recommended not to use this data for pinpointing individuals or households.

## Contributions
Contributions are welcome! Feel free to submit a pull request or report issues.

