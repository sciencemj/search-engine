import requests
from bs4 import BeautifulSoup

    
def prRed(skk) -> None: print("\033[91m{}\033[00m" .format(skk))

def prGreen(skk) -> None: print("\033[92m{}\033[00m" .format(skk))

def prYellow(skk) -> None: print("\033[93m{}\033[00m" .format(skk))

def prCyan(skk) -> None: print("\033[96m{}\033[00m" .format(skk))

def clear() -> None: print("\033c", end="", flush=True)

def open_url(url: str) -> list[str]:
    try:
        with requests.get(url) as req:
            html: BeautifulSoup = BeautifulSoup(req.text, 'html.parser')
    except:
        return []

    url_www = url.split('/')[2] #https://[url_www]/~
    if url_www.count('.') < 2:
        url_main = url_www
    else:
        url_main = url_www.split('.')[1] + '.' + url_www.split('.')[2]
    clear()

    prGreen(f"url_main is {url_main}")
    a_list = [a.get('href') for a in html.find_all('a')]
    a_list = list(filter(lambda href: href is not None, a_list))
    if len(a_list) > 0:
        link_list = [a for a in a_list if (a.startswith('https://') and not url_main in a)] #get only https link and exclude in-site link
        for i, link in enumerate(link_list, 1):
            print(f"[{i}] {link}")
    else:
        print(f"no link in {url_www}")
        link_list = []
    return link_list
    
def search(startURL: str, depth: int, tree: list) -> dict:
    if depth < 0: #end searching
        return {}
    links: list[str] = open_url(startURL)
    tree.append(startURL)
    if len(links) > 0: 
        link_dic: dict = {link:1 for link in links}
        for link in links:
            if link in tree: #같은 경로에서 열었던 링크를 열면 안됨
                continue
            result = search(link, depth-1, tree)
            link_dic = {k: link_dic.get(k, 0) + result.get(k, 0) for k in set(link_dic) | set(result)} #merge two dict
    else:
        link_dic = {}
    return link_dic



def main() -> None:
    startURL: str = input('Enter the start URL: ')
    search_depth: int = int(input('Enter the depth of search(number): '))
    if(search_depth <= 0):
        print("search depth must be over 0!")
    else:
        rank_dic: dict = search(startURL, search_depth, [])
        sorted_dic = dict(sorted(rank_dic.items(), key=lambda item: item[1], reverse=True))
    while True:
        user_input: str = input('>>')
        clear()
        if user_input == "exit": #프로그램 종료
            break
        elif user_input == "list" or user_input.split(' ')[0] == "list": #사이트 리스트 표시
            for i, items in enumerate(sorted_dic.items(), 1):
                if user_input != "list" and (i - 1) == int(user_input.split(' ')[1]):
                    break
                print(f"[{i}] {items[1]}: {items[0]}")
        elif user_input.split(' ')[0] == "search": #검색
            arg = user_input.split(' ')[1]
            search_results = [r for r in sorted_dic.keys() if arg in r]
            if len(search_results) <= 0:
                prYellow("no result matching!")
            else:
                for result in search_results:
                    print(f"[*] {result}")
        else: #잘못된 입력
            prRed("wrong command!")

if __name__ == "__main__":
    main()