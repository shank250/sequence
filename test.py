import time
import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import configparser
from credentials import username, password

# init
connecting_str = f"mongodb+srv://{username}:{password}@bulk.h6leskz.mongodb.net/"
# "mongodb+srv://<username>:<password>@<cluster-url>/<database>?retryWrites=true&w=majority"
client = pymongo.MongoClient(connecting_str)
# driver = webdriver.Chrome()

# for activating headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")  # Set log level to suppress INFO messages
driver = webdriver.Chrome(options=chrome_options)

# push data into mongodb atlas
db = client["oeis"]
collection = db["sequences"]

# inputs
last_inserted_document = collection.find_one(sort=[("_id", -1)])
if last_inserted_document:
    for key, value in last_inserted_document.items():
        if key != "_id":
            initialise = key
            break
else:
    print("No Data found.")
# initialise = int(input("Initialise from :"))
initialise = initialise[1:]
initialise = int(initialise) + 1
ending = 350000

def add_data(key, val):
    data = {key: val}
    collection.insert_one(data)
# data = {
#     "key1": "value1",
#     "key2": "value2",
#     "key3": "value3"
# }
# collection.insert_one(data)

# crwaling
def crawl(initialise, ending):
    for i in range(initialise, ending): 
        start = time.time() 
        i_str = str(i)
        no_of_numbers = len(i_str)
        for j in range(6-no_of_numbers):
            i_str = "0" + i_str
        i_str = "A" + i_str
        driver.get(f"https://oeis.org/{i_str}")
        element_id = 'seqwin'
        driver.implicitly_wait(30)
        center_element = driver.find_element(By.XPATH, "(//center)[2]")
        element_text = center_element.text
        add_data(i_str, element_text)  
        end = time.time()
        print(f"Time taken for {i_str} is {end-start} seconds")
        # print(element_text)

crawl(initialise, ending)

# time.sleep(3)
# target_element = driver.find_element(By.ID ,  element_id)
# target_element = driver.find_element_by_id(element_id)

# my_element.click()
# target_element = driver.find_element_by_id('downloadButton')
# driver.quit()
# import os

# os.environ['PATH'] += r"C:/SeleniumDrivers"
# driver = webdriver.Chrome()
# driver.get("https://www.seleniumeasy.com/test/jquery-download-progress-bar-demo.html")