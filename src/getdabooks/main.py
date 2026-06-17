
from urllib import request
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth.stealth import Stealth
from random import randint
from getdabooks.bookSorter import move_books


def main(curr_url, max_length=150):
    
    with Stealth().use_sync(sync_playwright()) as p:
        url = curr_url

        browser = p.chromium.launch(headless=False, slow_mo=5000)
        context = browser.new_context()
        
        page = context.new_page()
        
        page.goto(url)
        html = page.content()
        all_links = []
        download_links = []
        soup = BeautifulSoup(html, 'html.parser')
        
        title = str(page.locator("div.font-semibold.text-2xl.mt-2").first.text_content())
        
        
        
        
        title = title.replace("🔍", "").strip()
        title = title.replace(":","").strip()
        title = title.replace(";","").strip()
        title = title.replace("\\","").strip()
        title = title.replace("*","").strip()
        title = title.replace("]", '-').strip()
        title = title.replace("[", '-').strip()
        title = title.replace(",", '').strip()
        title = title[:max_length].strip()
        for a in soup.find_all('a'):
            href = a.get('href')
            if 'slow_download' in str(href).lower():
                all_links.append(href)
                
       
       
        rand_num = randint(4,7)
        open_url ='https://annas-archive.gl'+ all_links[rand_num]
       
        page.goto(open_url)
        
       
        page.wait_for_timeout(10000)
        
        page_c = page.content()
        if "h-captcha" in page_c or "DDoS-Guard" in page_c:
            print("Blocked/challenge state, not scraping yet")
        else:
            print("Safe state, continue extraction")
        spans =page.query_selector_all('span')
        
        for span in spans:
            if 'http' in str(span.text_content()):
                download_links.append(span.text_content())
        page.wait_for_timeout(10000)
        
        link = download_links[-1] 
        
        filename = link.split("/")[-1]
        ext =  filename.split(".")[-1]
        browser.close()
        print("Starting download...")
        
        request.urlretrieve(link, title +"."+ ext)
        
        print("Download complete")
    
        

def run():
    import sys
    urls = sys.argv[1:]
    
    for url in urls:
        main(url)
        move_books()
