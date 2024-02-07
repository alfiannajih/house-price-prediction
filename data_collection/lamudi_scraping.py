from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import json
from tqdm import tqdm

driver = webdriver.Firefox()

def open_website(city):
    link = "https://www.lamudi.co.id/house/buy/?q={}".format(city)

    driver.get(link)
    #time.sleep(1)

def scrape_house_information():
    """
    Scrapes house information from a web page and returns a list of dictionaries containing details such as location, description, bedroom, building area, land area, and price for each house.
    """

    # Step 1: Initialize house information list
    houses = []

    # Step 2: Find list of houses
    try:
        house_parent = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]")
    except:
        time.sleep(1)

    house_list = house_parent.find_elements(By.CLASS_NAME, "row")[:-1]
    
    # step 0: scroll to bottom
    driver.execute_script("arguments[0].scrollIntoView();", house_list[-1])

    # Step 3: Breakdown information of each house
    for house in house_list:
        # Step 3.0: Initialize house dict
        house_info = {}

        # Step 3.1: Find house entity
        house_entity = house.find_element(By.CLASS_NAME, "ListingCell-AllInfo")

        # Step 3.2: Find house location
        house_location = house_entity.find_element(By.CLASS_NAME, "ListingCell-KeyInfo-address").text
        house_info["location"] = house_location

        # Step 3.3: Find house description
        house_desc = house_entity.find_element(By.CLASS_NAME, "ListingCell-shortDescription").text
        house_info["description"] = house_desc

        # Step 3.4: Find house detail: bedroom, building area, and land area
        #house_detail = house_entity.find_element(By.CLASS_NAME, "ListingCell-keyInfo-details").text.split("\n")
        #house_info["detail"] = house_detail
        """
        bedroom = house_detail[0]
        house_info["bedroom"] = bedroom

        building_area = house_detail[2]
        house_info["building_area"] = building_area

        land_area = house_detail[4]
        house_info["land_area"] = land_area
        """
        
        # Step 3.5: Find house price
        try:
            house_price = house_entity.find_element(By.CLASS_NAME, "PriceSection-FirstPrice").text
        except:
            house_price = None
        house_info["price"] = house_price

        houses.append(house_info)
    
    return houses

def scroll_to_bottom():
    """
    Scroll to bottom of the page to load all houses data
    """
    bottom = driver.find_element(By.CLASS_NAME, "BaseSection")
    driver.execute_script("arguments[0].scrollIntoView();", bottom)

def next_page():
    """
    Click next page button
    """
    next_page_button = driver.find_element(By.CLASS_NAME, "next")
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
def scraping_process(cities):
    for city in cities:
        open_website(city)
        print("Scraping {}...".format(city))
        for i in tqdm(range(50)):
            save_json(scrape_house_information(), "data_collection/lamudi/{}".format(city))
            next_page()
            time.sleep(1)
        #driver.close()

cities = [
    #"jakarta",
    #"surabaya",
    "bandung",
    "medan",
    "malang"
]

scraping_process(cities)