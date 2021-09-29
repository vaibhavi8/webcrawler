from bs4 import BeautifulSoup
import requests

def main():
    seed = requests.get('https://www.espn.com/')
    '''print(seed.text)'''

    parser = BeautifulSoup(seed.content, 'html.parser')
    links = []
    for i in parser.find_all('a', attrs={'class': 'quicklinks_list__link'}) :
        links.append([i.text, i['href']])
    print(links[0])

if __name__ == '__main__':
    main()