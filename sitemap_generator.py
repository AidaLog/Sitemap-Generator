import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, ElementTree

def crawl_page(url):
    """
    # Function to crawl a webpage and extract links
    :param url::  str: url of the webpage
    :return:: []:list
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                links.append(href)
        return links
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return []


def generate_sitemap(start_url):
    """
    # Function to generate a sitemap
    :param start_url:: str: url of the website
    :return:: None
    """
    root = Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    links_to_crawl = [start_url]
    while links_to_crawl:
        url = links_to_crawl.pop()
        links = crawl_page(url)
        for link in links:
            if link not in links_to_crawl:
                links_to_crawl.append(link)
            url_element = SubElement(root, 'url')
            loc_element = SubElement(url_element, 'loc')
            loc_element.text = link
    tree = ElementTree(root)
    tree.write('sitemap.xml')

if __name__ == "__main__":
    start_url = "https://eddiegulay.me"
    print(f"Generating sitemap for {start_url}...")
    generate_sitemap(start_url)
    print("Sitemap generated successfully.")
