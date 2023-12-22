from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import csv
import schedule

# Counter to keep track of the number of IP addresses fetched
ip_counter = 0

# Define the perform_random_action function here (already defined earlier)
def perform_random_action(driver):
    actions = [
        "click_on_case_study",
        "click_learn_more",
        "click_on_image",
        "click_on_link",
    ]
    random_action = random.choice(actions)

    if random_action == "click_on_case_study":
        # Randomly select a case study ID and perform the action
        selected_case_study_id = random.choice(case_study_ids)
        case_study_section = driver.find_element(By.ID, selected_case_study_id)
        driver.execute_script("arguments[0].scrollIntoView();", case_study_section)
        driver.execute_script("arguments[0].click();", case_study_section)
    elif random_action == "click_on_image":
        # Implement the code to click on an image (if present)
        images = driver.find_elements(By.TAG_NAME, 'img')
        if images:
            random_image = random.choice(images)
            driver.execute_script("arguments[0].scrollIntoView();", random_image)
            driver.execute_script("arguments[0].click();", random_image)
    elif random_action == "click_on_link":
        # Implement the code to click on a link (if present)
        links = driver.find_elements(By.TAG_NAME, 'a')
        if links:
            random_link = random.choice(links)
            driver.execute_script("arguments[0].scrollIntoView();", random_link)
            driver.execute_script("arguments[0].click();", random_link)
    elif random_action == "click_learn_more":
        # Implement the code to click the "Learn More" button
        learn_more_button = driver.find_element(By.ID, "appx-btn-learnmore-summary-bar-id")
        driver.execute_script("arguments[0].scrollIntoView();", learn_more_button)
        driver.execute_script("arguments[0].click();", learn_more_button)

# Read IP addresses from a CSV file
def read_ip_addresses_from_csv(csv_file):
    ip_addresses = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Check if the row is not empty
                ip_addresses.append(row[0])
    return ip_addresses

# List of case study IDs (you can add more as needed)
case_study_ids = [
    "AppxConsultingListingDetail:AppxLayout:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id770:j_id771:j_id788:0:title",
    "AppxConsultingListingDetail:AppxLayout:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id770:j_id771:j_id788:1:title",
    "AppxConsultingListingDetail:AppxLayout:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id770:j_id771:j_id788:2:title",
    "AppxConsultingListingDetail:AppxLayout:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id770:j_id771:j_id788:3:title",
    "AppxConsultingListingDetail:AppxLayout:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id770:j_id771:j_id788:4:title",
    "AppxConsultingListingDetail:AppxLayout:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id770:j_id771:j_id788:5:title",
    "AppxConsultingListingDetail:AppxLayout:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id770:j_id771:j_id788:6:title",
]

# Read IP addresses from a CSV file
ip_addresses = read_ip_addresses_from_csv('us_ips_1.csv')

# List of search keywords
search_keywords = ["techila", "techila global", "techila global services", "techila services"]

# Define a function to encapsulate your existing script
def run_script():
    global ip_counter  # Use the global counter variable
    for proxy_ip in ip_addresses:
        # If the daily limit is reached (2 IPs), exit the script
        if ip_counter >= 20:
            print("Daily limit reached. Exiting the script.")
            break

        # Increment the IP counter
        ip_counter += 1

        try:
            print(f'Using proxy IP: {proxy_ip}')

            options = webdriver.FirefoxOptions()
            options.add_argument(f'--proxy-server=http://{proxy_ip}')
            options.add_argument('--headless')  # Add this line for headless mode
            driver = webdriver.Firefox(options=options)

            url = 'https://appexchange.salesforce.com/'

            random_keyword = random.choice(search_keywords)

            driver.get(url)

            time.sleep(5)

            script = """
                return document.querySelector("#main > page-container").shadowRoot
                    .querySelector("analytics-handler > ace-header").shadowRoot
                    .querySelector("div > div > div > header > div.appx-global-header--search > search-type-ahead").shadowRoot
                    .querySelector("div > div.input-container > input");
            """

            input_element = driver.execute_script(script)

            if input_element:
                input_element.clear()
                input_element.send_keys(random_keyword)
                input_element.send_keys(Keys.RETURN)

                print(f'Searching for keyword "{random_keyword}" with proxy IP: {proxy_ip}')

                time.sleep(5)

                script_consultants = """
                    return document.querySelector("#main > page-container").shadowRoot
                        .querySelector("analytics-handler > div > x-lazy").shadowRoot
                        .querySelector("div > div.search-title-container > search-switcher").shadowRoot
                        .querySelector("div > ads-button:nth-child(2)").shadowRoot
                        .querySelector("amc-analytics-instrument > button");
                """

                consultants_button = driver.execute_script(script_consultants)

                if consultants_button:
                    consultants_button.click()
                    print('Consultants button clicked successfully')

                    time.sleep(5)

                    script_element = """
                        return document.querySelector("#main > page-container").shadowRoot
                            .querySelector("analytics-handler > div > x-lazy").shadowRoot
                            .querySelector("div > div.content-container > div.results-container > div.search-container > search-results").shadowRoot
                            .querySelector("div > amc-tiles-grid").shadowRoot
                            .querySelector("div > ads-grid > ads-grid-item > amc-listing-tile").shadowRoot
                            .querySelector("amc-analytics-instrument > div > ads-card > div:nth-child(1) > div:nth-child(2) > ads-content-title > div > a");
                    """

                    target_element = driver.execute_script(script_element)

                    if target_element:
                        target_element.click()
                        print('Target element clicked successfully')

                        time.sleep(5)

                        perform_random_action(driver)

                    else:
                        print('Target element not found.')
                else:
                    print('Consultants button not found.')

            else:
                print('Input element not found.')

        except Exception as e:
            print("Error:", e)

        finally:
            time.sleep(5)
            driver.quit()

# Schedule the script to run on specific days and times
schedule.every().monday.at("22:22").do(run_script)
schedule.every().tuesday.at("13:30").do(run_script)
schedule.every().wednesday.at("17:00").do(run_script)
schedule.every().thursday.at("13:00").do(run_script)
schedule.every().friday.at("18:00").do(run_script)

# Keep the script running to allow scheduled tasks to execute
while True:
    schedule.run_pending()
    time.sleep(1)

