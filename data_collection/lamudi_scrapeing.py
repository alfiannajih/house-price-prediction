from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

driver = webdriver.Firefox()

link = "https://www.lamudi.co.id/house/buy/"

driver.get(link)

time.sleep(3)

while True:
    # Step 1: Scroll to bottom
    bottom = driver.find_element(By.CLASS_NAME, "BaseSection")
    driver.execute_script("arguments[0].scrollIntoView();", bottom)

    # Step 2: Find list of houses
    house_parent = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]")
    house_list = house_parent.find_elements(By.CLASS_NAME, "row")[:-1]
    
    # Step 3: Breakdown information of each house
    

    pass