from selenium import webdriver  
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.webdriver import WebDriver  
from fake_useragent import UserAgent 
 
 
def get_user_agent(): 
    return UserAgent().random 
 
 
class Scraper: 
    driver : WebDriver = None 
     
    def get_driver(self): 
        if self.driver is None: 
            user_agent = get_user_agent() 
            options = Options() 
            options.add_argument("--no-sandbox") 
            options.add_argument("--headless") 
            options.add_argument(f"user-agent={user_agent}")  
            driver = webdriver.Chrome(options=options) 
            self.driver = driver 
        return self.driver  # Added return statement