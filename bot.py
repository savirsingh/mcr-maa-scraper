from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import time

def crop_image(input_path, output_path, left, top, right, bottom):
    # Open the image file
    original_image = Image.open(input_path)

    # Crop the image
    cropped_image = original_image.crop((left, top, original_image.size[0]-56, bottom))

    # Save the cropped image
    cropped_image.save(output_path)

# Set the path to your WebDriver (replace with the actual path)
driver_path = '/path/to/chromedriver'

# Create a new instance of the Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
dr = webdriver.Chrome(options=chrome_options)
e = webdriver.Chrome(options=chrome_options)

import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path

def upload_to_github(repo_owner, repo_name, file_path, token):
    # API Endpoint to upload a file to a repository
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'

    # Read the file content
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # Base64 encode the file content
    import base64
    encoded_content = base64.b64encode(file_content).decode('utf-8')

    # Prepare the request payload
    data = {
        'message': 'Upload image',
        'content': encoded_content,
    }

    # Set the Authorization header with the PAT
    headers = {
        'Authorization': f'token {token}',
    }

    # Make the API request
    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 201:
        print('File uploaded successfully!')
    else:
        print(f'Error uploading file. Status code: {response.status_code}')
        print(response.text)
        
year = 2024
contest = 'I'
a = dict()
e.get("https://mathcontestrepository.pythonanywhere.com/login")
username_input = e.find_element("id", "username")  # Replace with the actual ID of the username input field
password_input = e.find_element("id", "password")  # Replace with the actual ID of the password input field
username_input.send_keys("uploadbot")
password_input.send_keys("password123")
# Submit the login form
password_input.send_keys(Keys.RETURN)
e.implicitly_wait(5)

while year != 2000:
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(3)
    if contest == '12':
        contest = '12A'
    elif contest == '12A':
        contest = '12B'
    elif contest == '12B':
        contest = '10A'
    elif contest == '10A':
        contest = '10B'
    elif contest == '10B':
        contest = '8'
    elif contest == '8':
        contest = '12'
        year -= 1
    dr.get(f'https://artofproblemsolving.com/wiki/index.php/{year}_AIME_{contest}_Answer_Key')
    ol_element = dr.find_element(By.TAG_NAME, 'ul')
    li_elements = ol_element.find_elements(By.TAG_NAME, 'li')
    for index, li_element in enumerate(li_elements, start=1):
        answer_letter = li_element.text.strip()
        a[index] = answer_letter
    dr.close()
    dr.quit()
    for i in range(1, 16):
        # Navigate to the website
        print(f'https://artofproblemsolving.com/wiki/index.php/{year}_AIME_{contest}_Problems/Problem_{i}')
        driver.get(f'https://artofproblemsolving.com/wiki/index.php/{year}_AIME_{contest}_Problems/Problem_{i}')  # Replace with your website URL
        time.sleep(5)
        url = 'https://artofproblemsolving.com/wiki/index.php/{{year}}_AIME_{{contest}}_Answer_Key'
        try:
            # Find the first h1 element using its ID (replace 'first_h1_id' with the actual ID)
            first_h1 = driver.find_element(By.CSS_SELECTOR, '[id*="Problem"]')

            # Find the second h1 element using its ID (replace 'second_h1_id' with the actual ID)
            second_h1 = driver.find_element(By.CSS_SELECTOR, '[id*="Solution"]')

            # Get the location of the two h1 elements
            first_h1_location = first_h1.location['y']
            second_h1_location = second_h1.location['y']

            # Calculate the height of the section between the two h1 elements
            section_height = second_h1_location - first_h1_location

            # Scroll to the first h1 element
            driver.execute_script('arguments[0].scrollIntoView(true);', first_h1)

            # Capture a screenshot of the section between the two h1 elements
            driver.save_screenshot('screenshot.png')
            bottom = section_height
            left = 1
            top = 32
            right = 1
            input_path = 'screenshot.png'
            output_path = f'{year}{contest}{i}.png'
            crop_image(input_path, output_path, left, top, right, bottom)
            # Replace these with your own values
            repo_owner = 'mathcontestrepository'
            repo_name = 'amc-screenshots'
            file_path = output_path
            token = 'GITHUB_TOKEN'

            upload_to_github(repo_owner, repo_name, file_path, token)
            time.sleep(4)
            e.get("https://mathcontestrepository.pythonanywhere.com/publish-problem")
            title = e.find_element("id", "username")
            code = e.find_element("id", "code")
            statement = e.find_element("id", "statement")
            contcode = e.find_element("id", "contcode")
            difficulty = e.find_element("id", "difficulty")
            ans = e.find_element("id", "ans")
            tags = e.find_element("id", "tags")
            title.send_keys(str(year)+" AIME " + contest + " Problem " + str(i))
            code.send_keys(str(year)+"aime"+contest.lower()+str(i))
            statement.send_keys(f'{year} AIME {contest} Problem ${i}$, &copy <a href="https://maa.org/" target="_blank">MAA</a>.<br><img src="https://mathcontestrepository.github.io/amc-screenshots/{output_path}" style="width:100%"><br>This problem statement was automatically fetched from <a href="https://artofproblemsolving.com/" target="_blank">AoPS</a>.')
            contcode.send_keys("None")
            if i < 5:
                difficulty.send_keys(str(max(6, min(20, i))))
            elif i < 10:
                difficulty.send_keys(str(max(14, min(20, i))))
            else:
                difficulty.send_keys(20)
            ans.send_keys(str(a[i]))
            tags.send_keys("aime aime"+contest.lower() + " " + str(year) + "aime"+contest.lower())
            tags.send_keys(Keys.RETURN)
            e.implicitly_wait(5)
            print(i, "done")

        finally:
            # Wait for a moment between iterations
            time.sleep(5)

    # Close the browser window outside the loop
    driver.close()
