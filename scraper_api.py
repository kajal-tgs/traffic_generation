import requests
import csv

# Initialize the counters for US and non-US IPs
us_count = 0
non_us_count = 0

# Create CSV files and write headers
with open('US_IPs.csv', mode='w', newline='') as us_file:
    us_writer = csv.writer(us_file)
    us_writer.writerow(['IP Address', 'Country Name'])

with open('Non-US-IP-Address.csv', mode='w', newline='') as non_us_file:
    non_us_writer = csv.writer(non_us_file)
    non_us_writer.writerow(['IP Address', 'Country Name'])

# Make 100 requests
for i in range(200):
    # Use Scraper API to get an IP address from the US
    proxies = {
        "http": "http://scraperapi:c6bca375057c7d70074f282ac0da61e1@proxy-server.scraperapi.com:8001?country=US"
    }
    r = requests.get('http://httpbin.org/ip', proxies=proxies, verify=False)
    data = r.json()

    # Get the IP address from the response
    ip_address = data['origin']

    # Use ipinfo.io to get the country information for the IP address
    ip_info_url = f"http://ipinfo.io/{ip_address}/json"
    ip_info_response = requests.get(ip_info_url)
    ip_info_data = ip_info_response.json()

    # Extract the country name
    country_name = ip_info_data.get('country', 'Unknown')

    # Check if the country name is 'US' to verify if it's a US IP address
    if country_name == 'US':
        # Save the US IP address and country name in the US IP's CSV file
        with open('US_IPs.csv', mode='a', newline='') as us_file:
            us_writer = csv.writer(us_file)
            us_writer.writerow([ip_address, country_name])
        us_count += 1
    else:
        # Save the non-US IP address and country name in the Non-US IP Address CSV file
        with open('Non-US-IP-Address.csv', mode='a', newline='') as non_us_file:
            non_us_writer = csv.writer(non_us_file)
            non_us_writer.writerow([ip_address, country_name])
        non_us_count += 1

print(f"Total US IP addresses: {us_count}")
print(f"Total non-US IP addresses: {non_us_count}")

