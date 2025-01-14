import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import json
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

def wait_for_image_in_gallery(driver):
    """Wait until an <img> tag appears within the <tm-player-images-gallery>."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tm-player-images-gallery img"))
    )

def create_driver():
    """Create and configure a new Firefox driver with optimal settings."""
    options = Options()
    options.page_load_strategy = 'eager'
    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", False)
    options.set_preference("browser.cache.offline.enable", False)
    options.set_preference("network.http.use-cache", False)
    
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(20)
    return driver

def get_gallery_with_images(players):
    driver = create_driver()
    
    for player in players:
        try:
            url = player["url"]
            print(f"Processing player: {player['name']}")
            
            # Load the URL
            driver.get(url)

            # scroll 100 px down
            driver.execute_script("window.scrollBy(0, 1000);")
            
            # Wait for an <img> tag to be loaded inside the <tm-player-images-gallery>
            wait_for_image_in_gallery(driver)

            # Parse the fully rendered page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            gallery = soup.find("tm-player-images-gallery")
            
            if not gallery:
                print(f"Gallery not found for {player['name']}, skipping...")
                continue

            # Get all the img tags inside the gallery
            images = gallery.find_all("img")
            
            if not images:
                print(f"No images found for {player['name']}, skipping...")
                continue

            # Create a folder inside the photos folder with the player's id
            base_dir = os.path.dirname(os.path.abspath(__file__))
            photos_folder = os.path.join(base_dir, "..", "photos", player["id"])
            os.makedirs(photos_folder, exist_ok=True)

            # Download the images inside the new folder
            for i, image in enumerate(images):
                image_url = image["src"]
                image_path = os.path.join(photos_folder, f"{i}.jpg")
                
                try:
                    response = requests.get(image_url, timeout=10)
                    if response.status_code == 200:
                        with open(image_path, "wb") as file:
                            file.write(response.content)
                except Exception as e:
                    print(f"Error downloading image {i} for {player['name']}: {e}")

            print(f"Successfully processed {player['name']}")
            
            # Add a small delay between players
            sleep(2)
                
        except Exception as e:
            print(f"Error processing player {player['name']}: {e}")
            
            # If there's an error, recreate the driver
            try:
                driver.quit()
            except:
                pass
            driver = create_driver()
            sleep(2)

    try:
        driver.quit()
    except:
        pass

# Get the absolute path of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the players.json file
players_file_path = os.path.join(base_dir, "players.json")

# Get the players from the players.json file
with open(players_file_path, 'r') as file:
    players = json.load(file)

get_gallery_with_images(players)