from celery import shared_task
from .models import News
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
from time import sleep

@shared_task
def fetch_and_save_news():
    url_addr = "https://www.zoomit.ir"
    browser = webdriver.Firefox()
    try:
        browser.get(url_addr)
        sleep(5)  
        wait = WebDriverWait(browser, 20)
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

            try:
                tags_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.typography__StyledDynamicTypographyComponent-t787b7-0.cHbulB')))
                tags = tags_element.text.strip()
            except Exception:
                tags = 'No tags found'

            author_name = ''
            if 'author' in data and isinstance(data['author'], list):
                author_name = data['author'][0].get('name', 'No author found')
            elif 'author' in data:
                author_name = data['author'].get('name', 'No author found')

            user, created = User.objects.get_or_create(username=author_name)

            News.objects.update_or_create(
                title=title,
                defaults={
                    'text': text,
                    'tags': tags,
                    'source': source,
                    'category': 'OTHER',
                    'user': user
                }
            )

    finally:
        browser.quit()
