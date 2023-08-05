from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge import service
import os
os.system("cls") #clear screen from previous sessions
import time

options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument("start-maximized")
my_service=service.Service(r'msedgedriver.exe')
options.page_load_strategy = 'eager' #do not wait for images to load
options.add_experimental_option("detach", True)
options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage') # uses disk instead of RAM, may be slow, use it if You receive "driver Run out of memory" crashed browser message

s = 20 #time to wait for a single component on the page to appear, in seconds; increase it if you get server-side errors «try again later»

driver = webdriver.Edge(service=my_service, options=options)
action = ActionChains(driver)
wait = WebDriverWait(driver,s)

username = "nakigoe"
password = "Super_Mega_Password"
login_page = "https://www.github.com/login"
pages_to_star = [
    "https://github.com/nakigoe"
    ]

def scroll_to_bottom(): 
    reached_page_end= False
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    #expand the skills list:
    while not reached_page_end:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            reached_page_end = True
        else:
            last_height = new_height
             
def star_the_visible_page(): 
    try:
        star_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//button[@aria-label="Star this repository"]')))
        for star_button in star_buttons:
            try:
                action.move_to_element(star_button).perform()
                time.sleep(0.5)
                action.click(star_button).perform()
                time.sleep(1)
            except:
                continue #there are invisible buttons included into the star_buttons, nothing I can do for now, tried many selectors. Email me solutions if You find them! 
    except:
        do = "nothing"

         
def login():
    driver.get(login_page)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="login_field"]'))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="password"]'))).send_keys(password)
    action.click(wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="commit"]')))).perform()

def main():
    login()
    time.sleep(10) # in case two-step verification is necessary, keep your phone nearby!
    
    for user_page in pages_to_star:
        driver.get(user_page + "?tab=repositories")
        time.sleep(5) #just in case of a slow connection
        while True:
            star_the_visible_page()
            try:
                scroll_to_bottom()
                next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="next_page"]')))
                action.move_to_element(next_page_button).perform()
                time.sleep(0.5)
                action.click(next_page_button).perform()
                time.sleep(5) #just in case of a slow connection
            except:
                break

    os.system("cls") #clear screen from unnecessary logs since the operation has completed successfully
    print("All Your desired pages are completely starred! \n \nSincerely Yours, \nNAKIGOE.ORG\n")
    driver.close()
    driver.quit()
main()
