import requests
from bs4 import BeautifulSoup

def open_url(url: str) -> None:
    with requests.get(url) as req:
        html: BeautifulSoup = BeautifulSoup(req.text, 'html.parser')

    url_www = url.split('/')[2] #https://[url_www]/~
    if url_www.count('.') < 2:
        url_main = url_www
    else:
        url_main = url_www.split('.')[1] + '.' + url_www.split('.')[2]

    print(f"url_main is {url_main}")
    link_list = [a.get('href') for a in html.find_all('a') if (a.get('href').startswith('https://') and not url_main in a.get('href'))] #get only https link and exclude in-site link
    for i, link in enumerate(link_list, 1):
        print(f"[{i}] {link}")
    

def main() -> None:
    startURL: str = input('Enter the start URL: ')
    #search_deep: int = input('Enter the deep of search(number): ')
    open_url(startURL)

if __name__ == "__main__":
    main()