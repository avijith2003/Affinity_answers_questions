from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tabulate import tabulate
import time

def fetch_page_source(url):
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # Open the URL
        driver.get(url)
        
        # Wait for the page to fully load 
        time.sleep(15)
        
        # Get the rendered HTML
        page_source = driver.page_source
        return page_source
    
    except Exception as e:
        print(f"An error occurred while fetching the page: {e}")
        return None
    
    finally:
        # Close the browser
        driver.quit()

def extract_ads(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    
    ads = []
    # Find all ad containers
    ad_containers = soup.find_all('li', attrs={'data-aut-id': 'itemBox3'})
    for container in ad_containers:
        # Extract title
        title = container.find('span', attrs={'data-aut-id': 'itemTitle'}).text.strip() if container.find('span', attrs={'data-aut-id': 'itemTitle'}) else 'N/A'
        
        # Extract description
        description = container.find('span', attrs={'data-aut-id': 'itemDetails'}).text.strip() if container.find('span', attrs={'data-aut-id': 'itemDetails'}) else 'N/A'
        
        # Extract price
        price = container.find('span', attrs={'data-aut-id': 'itemPrice'}).text.strip() if container.find('span', attrs={'data-aut-id': 'itemPrice'}) else 'N/A'
        
        # Truncate description if too long
        if len(description) > 100:
            description = description[:97] + "..."
        
        # Add to list of ads
        ads.append([title, description, price])
    
    return ads

def print_table(ads):
    # Define table headers
    headers = ["Title", "Description", "Price"]
    
    # Use tabulate to print a structured table
    print(tabulate(ads, headers=headers, tablefmt="grid", stralign="left", maxcolwidths=[50, 100, 15]))

# Main program
url = "https://www.olx.in/items/q-car-cover?isSearchCall=true"
page_source = fetch_page_source(url)

if page_source:
    ads = extract_ads(page_source)
    if ads:
        print_table(ads)
    else:
        print("No ads found on the page.")
else:
    print("Failed to retrieve the page content.")