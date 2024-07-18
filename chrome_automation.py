from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import os
from dotenv import load_dotenv

#LastTwoFeatures

def test_selenium():
    
    # Sets up driver and opens browser
    driver = webdriver.Chrome()  ### NEED CHROME WEBDRIVERS TO BE RELEASED
    driver.get("https://example.com")

    # Sets Screen Size
    driver.set_window_size(720, 790)  # fullscreen size is 1440 x 790 for Mitchell's machine

    # Sets Window Location
    screen_width = driver.execute_script("return window.screen.width;")
    driver.set_window_position(screen_width // 2, 0)

    #This uses JavaScript to check the readyState of the document. When the readyState is "complete", it means the webpage has finished loading
    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    print('Test Completed')
    sleep(3)
    driver.quit()


def edit_credentials():
    # Prompt the user for username and password
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    # Prepare the content to write to the .env file
    content = f'USERNAME = "{username}"\nPASSWORD = "{password}"'

    # Define the path to the .env file
    env_file_path = '.env'
    # Write (or overwrite) the .env file with the new content
    with open(env_file_path, 'w') as file:
        file.write(content)

    print("The credentials has been updated.")


def automation(amountOfFiles):

    # Sets up driver and opens browser
    driver = webdriver.Chrome()  ### NEED CHROME WEBDRIVERS TO BE RELEASED
    driver.get("https://emma-back.mse.psych.wsu.edu/login")

    # Sets Screen Size
    driver.set_window_size(720, 790)  # fullscreen size is 1440 x 790 for Mitchell's machine

    # Sets Window Location
    screen_width = driver.execute_script("return window.screen.width;")
    driver.set_window_position(screen_width // 2, 0)

    #This uses JavaScript to check the readyState of the document. When the readyState is "complete", it means the webpage has finished loading
    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    #Login Credentials
    load_dotenv()
    env_username = os.getenv("USERNAME")
    env_password = os.getenv("PASSWORD")
    #print(env_password, env_username)
    signInBoxUsername = driver.find_element(By.ID, 'inputUsername')
    signInBoxUsername.send_keys(env_username)
    signInBoxPassword = driver.find_element(By.ID, 'inputPassword')
    signInBoxPassword.send_keys(env_password)
    signInButton = driver.find_element(By.XPATH, '/html/body/div/form[1]/button')
    signInButton.click()

    #Wait a bit for the page to react to the login attempt
    sleep(1)
    #Check for the presence of the alert indicating incorrect credentials
    try:
        alert_div = driver.find_element(By.CLASS_NAME, 'alert-danger')
        if "Email could not be found" in alert_div.text or "Invalid credentials." in alert_div.text:
            print("The credentials are incorrect.")
            driver.close()
    except NoSuchElementException:
        # If the element is not found, it means login might have been successful or the page didn't show the error as expected
        print("Login attempt completed.")

    #Goes to the training files tab of the website
    sleep(1)
    try:
        trainingButton = driver.find_element(By.PARTIAL_LINK_TEXT, 'Training Files')
        trainingButton.click()
    except NoSuchElementException:
        print("Element not found. Please check your Xpath selector.")
        driver.quit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        driver.quit()

    #Loops through files and prints them
    try:
        #Gets title of the first item
        title = driver.find_element(By.XPATH, '/html/body/div/div/div/table/tbody/tr[2]').text
        print(f"First item is: {title}")

        #Counts all file items in the list
        rows = len(driver.find_elements(By.XPATH, '/html/body/div/div/div/table/tbody/tr'))
        print(f"Total number of patient data: {rows-1}")

        #Get the current working directory (where the web script is located)
        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        print("Current directory:", currentDirectory)
        #Checks/creates a People folder in this directory.
        dirPath = currentDirectory + "/People"
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        
        if amountOfFiles == "all":
            amountOfFiles = rows
        else:
            # Check if amountOfFiles is a digit and its integer value is >= rows
            if amountOfFiles.isdigit():
                amountOfFiles_int = int(amountOfFiles)  # Convert to integer
                if amountOfFiles_int >= rows:
                    amountOfFiles = rows
                else:
                    amountOfFiles = amountOfFiles_int
            else:
                # Handle the case where amountOfFiles is neither "all" nor a digit
                print("Invalid input")


        #Loops through files and downloads them
        for r in range(2, (amountOfFiles+2)):
            # Find the file list on webpage
            xpath = f'/html/body/div/div/div/table/tbody/tr[{r}]'
            fileCurrent = driver.find_element(By.XPATH, xpath)
            fileTitle = fileCurrent.text
            # Define the file path including the file name
            filePath = os.path.join(dirPath, f"{fileTitle}.txt")
            
            # Click into the files and copy its contents then go back to the file listing page
            fileCurrent.click()
            #sleep(1)
            fileContent = driver.find_element(By.XPATH, '/html/body/pre').text
            driver.execute_script("window.history.go(-1)")
            
            # Open the file in write mode ('w') and write the content from the selected file into it
            with open(filePath, "w") as file:
                file.write(fileContent)
            # Print the title to the screen
            print(fileTitle)



    except Exception as e:
        print(f"An unexpected error occurred: {e}")


    sleep(3)
    print('Session Ended')
    driver.quit()

    #Waits until the browser window is closed then closes the script and driver
    # try:
    #     # Wait until there are no open windows
    #     WebDriverWait(driver, 9999999).until(EC.number_of_windows_to_be(0))
    # finally:
    #     print('Session Ended')
    #     driver.quit()

   
if __name__ == "__main__":
    automation()


