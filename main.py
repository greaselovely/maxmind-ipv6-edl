import csv
import zipfile
import os, sys
import requests
import netaddr

BLOCKED_COUNTRIES = ['VA', 'MC']  # Replace with your list of country ISO codes

LICENSE_KEY = '<YOUR_LICENSE_KEY>'
# find your account ID and use the following URL with your account id replaced
# https://www.maxmind.com/en/accounts/your_account_id/license-key/create

GEOIP_DOWNLOAD_URL = f"https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country-CSV&license_key={LICENSE_KEY}&suffix=zip"
ZIP_FILE = 'GeoLite2-Country.zip'
EXTRACT_FOLDER = 'geolite2_data'
OUTPUT_FILE = 'blocked_ipv6_edl.txt'

def check_zip_file(file):
    return os.path.exists(file)

def download_geolite2_database():
    """
    Downloads the GeoLite2 CSV database from MaxMind using the provided license key.
    Saves the downloaded zip file to the specified location.
    """
    response = requests.get(GEOIP_DOWNLOAD_URL)
    if response.status_code == 200:
        with open(ZIP_FILE, 'wb') as f:
            f.write(response.content)
        print(f"Database downloaded and saved to {ZIP_FILE}")
    else:
        print(f"Failed to download GeoLite2 database. Status code: {response.status_code}")
        exit(1)

def extract_database():
    """
    Extracts the downloaded GeoLite2 CSV zip file to the specified folder.
    """
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_FOLDER)
    print(f"Database extracted to {EXTRACT_FOLDER}")

def find_file(file_name):
    """
    Searches for a specified file within the extracted folder.
    Returns the full path to the file if found.
    Raises FileNotFoundError if the file is not found.
    """
    for root, _, files in os.walk(EXTRACT_FOLDER):
        for file in files:
            if file == file_name:
                found_path = os.path.join(root, file)
                print(f"Found {file_name} at {found_path}")
                return found_path
    raise FileNotFoundError(f"{file_name} not found in extracted data")

def get_geoname_country_mapping():
    """
    Creates a mapping of GeoName IDs to country ISO codes using the locations CSV file.
    Returns a dictionary with GeoName IDs as keys and country ISO codes as values.
    """
    locations_csv = find_file('GeoLite2-Country-Locations-en.csv')
    mapping = {}
    with open(locations_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            geoname_id = row['geoname_id']
            country_code = row['country_iso_code']
            mapping[geoname_id] = country_code
    print(f"Loaded {len(mapping)} geoname_id to country code mappings")
    return mapping

def extract_ipv6_blocks(country_mapping):
    """
    Extracts IPv6 networks for the specified blocked countries from the GeoLite2 CSV file.
    Returns a dictionary with country codes as keys and lists of IPv6 networks as values.
    """
    ipv6_blocks = {}
    csv_path = find_file('GeoLite2-Country-Blocks-IPv6.csv')

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            geoname_id = row.get('registered_country_geoname_id', '')
            if geoname_id in country_mapping:
                country_code = country_mapping[geoname_id]
                if country_code in BLOCKED_COUNTRIES:
                    if country_code not in ipv6_blocks:
                        ipv6_blocks[country_code] = []
                    ipv6_blocks[country_code].append(netaddr.IPNetwork(row['network']))
    print(f"Found IPv6 blocks for blocked countries")
    return ipv6_blocks

def write_edl_file(ipv6_blocks):
    """
    Aggregates IPv6 blocks for each country and writes them to an External Dynamic List (EDL) text file.
    Outputs the number of lines in the generated EDL file.
    """
    with open(OUTPUT_FILE, 'w') as edl_file:
        for country_code, blocks in ipv6_blocks.items():
            aggregated_blocks = netaddr.cidr_merge(blocks)
            for block in aggregated_blocks:
                edl_file.write(f"{block} - {country_code}\n")
    print(f"IPv6 EDL saved to {OUTPUT_FILE}")

    with open(OUTPUT_FILE, 'r') as edl_file:
        line_count = sum(1 for _ in edl_file)
    print(f"Number of lines in the EDL output file: {line_count}")

def main():
    if LICENSE_KEY == '<YOUR_LICENSE_KEY>':
        print("\n\nUpdate your license key from MaxMind and re-run\n\tFind your account ID and use the following URL with your account id replaced\n\thttps://www.maxmind.com/en/accounts/your_account_id/license-key/create\n\n")
        sys.exit(0)
    if not check_zip_file(ZIP_FILE):
        print("Downloading...")
        download_geolite2_database()
    extract_database()
    country_mapping = get_geoname_country_mapping()
    ipv6_blocks = extract_ipv6_blocks(country_mapping)
    write_edl_file(ipv6_blocks)

if __name__ == '__main__':
    main()
