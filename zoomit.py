import sys
import os
import django
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from django.core.exceptions import ObjectDoesNotExist

sys.path.append(r'C:\Users\fara\Desktop\roshan\project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from part1.models import News
from django.contrib.auth.models import User

url_addr = "https://www.zoomit.ir"

browser = webdriver.Firefox()

browser.get(url_addr)
sleep(5)  

wait = WebDriverWait(browser, 20)

try:
    html_source = browser.page_source

    json_ld_pattern = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)
    json_ld_match = json_ld_pattern.search(html_source)

    if json_ld_match:
        json_ld_data = json_ld_match.group(1)

        data = json.loads(json_ld_data)

        if isinstance(data, list):
            data = data[0]  

        title = data.get('headline', 'No title found')
        text = data.get('description', 'No article body found')
        source = data.get('url', 'No source URL found')
        publish_date = data.get('datePublished', 'No publish date found')

        try:
            tags_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.typography__StyledDynamicTypographyComponent-t787b7-0.cHbulB')))
            tags = tags_element.text.strip()
        except Exception as tag_exception:
            print(f"An error occurred while extracting tags: {tag_exception}")
            tags = 'No tags found'  

        author_name = ''
        if 'author' in data and isinstance(data['author'], list):
            author_name = data['author'][0].get('name', 'No author found')
        elif 'author' in data:
            author_name = data['author'].get('name', 'No author found')

        user, created = User.objects.get_or_create(username=author_name)
        if created:
            print(f"Created new user: {user.username}")
        else:
            print(f"User found: {user.username}")

        news_article, created = News.objects.update_or_create(
            title=title,
            defaults={
                'text': text,
                'tags': tags,
                'source': source,
                'category': 'OTHER', 
                'user': user
            }
        )

        print(f"Article saved: {news_article}")

    else:
        print("No JSON-LD structured data found on the page.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    browser.quit()
