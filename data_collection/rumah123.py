from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import json
from tqdm import tqdm
from selenium.common.exceptions import TimeoutException

driver = webdriver.Firefox()
driver.implicitly_wait(0.5)

def open_website(city, certif, furnish):
    link = "https://www.rumah123.com/jual/{}/rumah/?certificates[]={}&furnish[]={}&page=1".format(city, certif, furnish)
    driver.set_page_load_timeout(10)
    
    try:
        driver.get(link)
        
    except TimeoutException:
        driver.execute_script("window.stop();")

    #time.sleep(1)

def scrape_house_information(additional):
    """
    Scrapes house information from a web page and returns a list of dictionaries containing details such as location, description, bedroom, building area, land area, and price for each house.
    """

    # Step 1: Initialize house information list
    houses = []

    # Step 2: Find list of houses
    for attempt in range(3):
        try:
            house_parent = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[3]/div[1]/div")
            house_list = house_parent.find_elements(By.CLASS_NAME, "ui-organism-intersection__element")
            break
        except:
            driver.refresh()
            time.sleep(1)
    
    # step 3: scroll to bottom
    driver.execute_script("arguments[0].scrollIntoView();", house_list[-1])

    # Step 4: Breakdown information of each house
    for house in house_list:
        # Step 4.0: Initialize house dict
        house_info = {}

        # Step 4.1: Find house entity
        try:
            house_entity = house.find_element(By.CLASS_NAME, "card-featured__middle-section")
        except:
            continue

        # Step 4.2: Find house location
        house_location = house_entity.find_elements(By.TAG_NAME, "span")[1].text
        house_info["location"] = house_location

        # Step 4.3: Find house description
        #house_desc = house_entity.find_element(By.CLASS_NAME, "ListingCell-shortDescription").text
        #house_info["description"] = house_desc

        # Step 4.4: Find house detail: bedroom, building area, and land area
        house_detail = house_entity.find_element(By.CLASS_NAME, "card-featured__middle-section__attribute")
        house_info["detail"] = house_detail.text

        # Determine whether it is a carport, bath room, or bed room
        house_facility = []
        facility_info = house_detail.find_elements(By.TAG_NAME, "use")
        for facility in facility_info:
            house_facility.append(facility.get_attribute("xlink:href"))

        house_info["facility"] = house_facility

        """
        bedroom = house_detail[0]
        house_info["bedroom"] = bedroom

        building_area = house_detail[2]
        house_info["building_area"] = building_area

        land_area = house_detail[4]
        house_info["land_area"] = land_area
        """
        
        # Step 4.5: Find house price
        house_price = house_entity.find_element(By.CLASS_NAME, "card-featured__middle-section__price").text
        house_info["price"] = house_price

        houses.append(house_info|additional)
    
    return houses

def next_page():
    """
    Click next page button
    """
    next_page_button = driver.find_element(By.CLASS_NAME, "ui-molecule-paginate__item--next")

    next_page_button.click()
    
def save_json(json_data, output_file):
    """
    Save JSON data to a file.

    :param JSON_file: the JSON data to be saved
    :return: None
    """
    with open('{}.txt'.format(output_file), 'a') as outfile:
        for entry in json_data:
            json.dump(entry, outfile)
            outfile.write('\n')

# Execute scraping process
def scraping_process(cities, certif, furnish):
    """
    Scrapes house information from the given list of cities by iterating through each city, opening the website, and scraping 50 pages of house data. It saves the collected data as a JSON file for each city in the specified directory. 
    :param cities: list of cities to scrape house information from
    :return: None
    """
    for city in cities:
        open_website(city, certif, furnish)
        print("Scraping {}...".format(city))
        # Scrape 50 pages
        for i in tqdm(range(1000)):
            additional = {
                "certif": certif,
                "furnish": furnish
            }
            save_json(scrape_house_information(additional), city)
            
            # Attempt to click next page button 5 times
            attempt = 0
            while attempt < 5:
                try:
                    attempt += 1
                    next_page()
                except:
                    time.sleep(0.5)
                else:
                    break
            else:
                break

        time.sleep(1)
cities = [
    "jakarta-pusat",
    "jakarta-utara",
    "jakarta-timur",
    "jakarta-selatan",
    "jakarta-barat"
]
# certif 1: SHM, 2: HGB
# furnish 1: furnished, 3: unfurnished
scraping_process(["jakarta-selatan"], certif=1, furnish=1)

print("Done!")