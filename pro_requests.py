import requests
from bs4 import BeautifulSoup

####################################################################################################################

# Paste converted curl command to utilize auth without a web scraper

# 1. Log into ProABD
# 2. Open Chrome Dev Tools using Right Click -> Inspect
# 3. Naviate to Network tab and clear the contects but keep recording enabled
# 4. make a search in the quick search box
# 5. Fnd the package that pertains to the request
# 6. Right Click -> Copy as Curl command (bash)
# 7. Go to https://curlconverter.com and paste the contents
# 8. Copy the output from the Python output
# 9. Paste between these lines

####################################################################################################################
soup = BeautifulSoup(response.text, "html.parser")

if soup.find('ul', class_='list-group').find('a'):
    # If there is an <a> tag within the <ul> element
    # Do something with the result
    print("Result found!")
    # For example, you can extract the href attribute of the <a> tag
    result_href = soup.find('ul', class_='list-group').find('a')['href']
    print("Result href:", result_href)
else:
    # If there is no <a> tag within the <ul> element
    # Do something else
    print("No result found!")