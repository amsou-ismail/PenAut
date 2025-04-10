# File: shodan_scan.py
from shodan import Shodan, APIError
import json
import logging

# Configuration
OUTPUT_JSON_FILE = 'shodan_results.json'
OUTPUT_TXT_FILE = 'shodan_results.txt'
RESULT_LIMIT = 10
API_KEY = '4r0qsTvjuSvnYubE1v0iow4Z2hbWEfg2'  # Remplacez par votre clé API Shodan

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_to_json(data, filename):
    """Save data to a JSON file with pretty formatting."""
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4, separators=(',', ': '))
        logging.info(f"Results saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save results to {filename}: {e}")

def save_to_txt(data, filename):
    """Save data to a TXT file with organized formatting."""
    try:
        with open(filename, 'w') as file:
            file.write("Shodan Scan Results\n")
            file.write("====================\n\n")

            # IP Info
            file.write("IP Information:\n")
            if "ip_info" in data and data["ip_info"]:
                for key, value in data["ip_info"].items():
                    file.write(f"  {key}: {value}\n")
            else:
                file.write("  No IP information available.\n")
            file.write("\n")

            # Search Results
            file.write("Search Results:\n")
            if "search_results" in data and data["search_results"]:
                for idx, result in enumerate(data["search_results"], start=1):
                    file.write(f"  Result {idx}:\n")
                    for key, value in result.items():
                        file.write(f"    {key}: {value}\n")
            else:
                file.write("  No search results available.\n")
            file.write("\n")

            # ICS Count
            file.write("Industrial Control Systems (ICS) Count:\n")
            if "ics_count" in data:
                file.write(f"  Total: {data['ics_count']}\n")
            else:
                file.write("  ICS count information unavailable.\n")
        logging.info(f"Results saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save results to {filename}: {e}")

def search_shodan(api, query, limit):
    """Search Shodan for the given query and return results."""
    results = []
    try:
        for banner in api.search_cursor(query):
            results.append(banner)
            if len(results) >= limit:
                break
        logging.info(f"Found {len(results)} results for query: {query}")
        return results
    except APIError as e:
        logging.error(f"Shodan search error: {e}")
        return []

def get_ics_count(api):
    """Get the count of industrial control systems services."""
    try:
        ics_services = api.count('tag:ics')
        total = ics_services.get("total", "Unknown")
        logging.info(f"Industrial Control Systems: {total}")
        return total
    except APIError as e:
        logging.error(f"Shodan count error: {e}")
        return "Unknown"

def main_shodan():
    # Initialize Shodan API
    api = Shodan(API_KEY)

    # Get user input for the search query
    search_query = input("Enter your Shodan search query(EX:appache..): ").strip()
    if not search_query:
        logging.error("No search query provided. Exiting.")
        return

    # Lookup an IP address
    try:
        ipinfo = api.host('8.8.8.8')
        logging.info("IP Info retrieved successfully.")
    except APIError as e:
        logging.error(f"Shodan API error while retrieving IP info: {e}")
        ipinfo = {}

    # Search for websites that match the query
    search_results = search_shodan(api, search_query, RESULT_LIMIT)

    # Get the count of industrial control systems services
    ics_count = get_ics_count(api)

    # Combine all results into a single dictionary
    results = {
        "ip_info": ipinfo,
        "search_results": search_results,
        "ics_count": ics_count
    }

    # Save results to JSON and TXT files
    save_to_json(results, OUTPUT_JSON_FILE)
    save_to_txt(results, OUTPUT_TXT_FILE)

