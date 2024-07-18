
import requests
from bs4 import BeautifulSoup
import os
import platform
from dotenv import load_dotenv


def download_files():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0'
    }

    
    #Login Credentials
    load_dotenv()
    env_username = os.getenv("USERNAME")
    env_password = os.getenv("PASSWORD")
    
    # The URL of the webpage you want to scrape
    base_url = "https://emma-back.mse.psych.wsu.edu"
    login_url = "https://emma-back.mse.psych.wsu.edu/login"
    files_url = "https://emma-back.mse.psych.wsu.edu/admin/view-files"

    filenames = []
    total = 0

    # Make a GET request to fetch the raw HTML content, bypassing SSL verification
    try:
        s = requests.Session()
        response = s.get(login_url, verify=False)  # Not recommended for production
        # Check if the request was successful
        if response.status_code == 200:
            # Use BeautifulSoup to parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the input element with name="_csrf_token"
            csrf_token_input = soup.find('input', attrs={'name': '_csrf_token'})
            
            # Extract the value of the CSRF token, if the element is found
            if csrf_token_input:
                csrf_token_value = csrf_token_input['value']
                print(f"CSRF Token Value: {csrf_token_value}")
                
                payload = {
                    "username": env_username,
                    "password": env_password,
                    "_csrf_token": csrf_token_value
                }
                r = s.post(login_url, headers=headers, data=payload)
                #print(r.text)
                adminPage = s.get(files_url)
                #print(adminPage.text)
                soup = BeautifulSoup(adminPage.text, 'html.parser')
                # Find all <a> tags within the table
                links = soup.find('table', class_='centered').find_all('a')

                # Extract the href attribute AKA the fileanames from each link
                hrefs = [link.get('href') for link in links]

                with open('out.txt', 'w') as file:
                    for href in hrefs:
                        total += 1
                        #print(href)
                        file.write(href + '\n')
                        filenames.append(href)
                print(total, filenames[1])

                
                # Now we loop through all filenames and save them to their own .csv's
                # Folder where CSV files will be saved
                folder_path = "People"

                # Check if the folder exists, if not, create it
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                amount = 0
                # Iterate over each filename/number in the list
                for name in filenames:
                    print(str(amount) + "   -<-------<------<--")
                    amount += 1

                    #if amount == 6:
                    #    return(f"Downloaded {amount} TXT files\ninto the local 'People' folder.")

                    #The url cannot contain spaces which is how they are saved on the site before
                    modified_name = name.replace(" ", "%20")
                    #print(modified_name)

                    # Form the complete URL
                    csv_url = base_url + modified_name
                    #print(csv_url)
                    
                    # Define the CSV file name based on the item's name
                    # Remove leading slash if present for filename compatibility
                    clean_name = name.lstrip('/csv/')

                    os_name = platform.system()
                    if os_name == "Windows":
                        # Replace colons and other invalid characters for Windows filenames
                        clean_name = clean_name.replace(':', '-').replace('\\', '-').replace('/', '-').replace('|', '-').replace('?', '-').replace('*', '-').replace('"', '-').replace('<', '-').replace('>', '-')
                    
                    txt_file_path = os.path.join(folder_path, f"{clean_name}.txt")
                    #print(clean_name + "\n" + txt_file_path)
                    # Send a GET request to the URL
                    response = s.get(csv_url)
                    #print(response.text)
                    # Check if the request was successful 
                    if response.status_code == 200:
                        # Parse the HTML content of the page            
                        soup = BeautifulSoup(response.text, 'html.parser')
                        

                        # Extract text within the <body> tag
                        #body_text = soup.body.get_text(strip=True)
                        body_text = response.text

                        # Open the TXT file for this item in write mode
                        with open(txt_file_path, mode='w', encoding='utf-8') as file:
                            
                            # Check if the body contains data (not empty or doesn't just contain whitespace)
                            if body_text:
                                # Write the body text to the TXT file
                                file.write(body_text)
                            else:
                                print(f"No data found in {csv_url}")

                return(f"Downloaded {amount} TXT files \ninto the 'People' folder.")

            else:
                return("CSRF token input element not found.")
        else:
            return(f"Failed to fetch the webpage. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        return(f"Request failed: {e}")



    print("_____________------END-----------________________")



def edit_credentials_gui(username, password):
    # Prompt the user for username and password
    #username = input("Enter your username: ")
    #password = input("Enter your password: ")
    # Prepare the content to write to the .env file
    content = f'USERNAME = "{username}"\nPASSWORD = "{password}"'

    # Define the path to the .env file
    env_file_path = '.env'
    # Write (or overwrite) the .env file with the new content
    with open(env_file_path, 'w') as file:
        file.write(content)

    return("The credentials has been updated.")

if __name__ == "__main__":
    os.system('clear')
    print("_____________-------START----------________________")
    print("\n")
    download_files()
    print("\n")