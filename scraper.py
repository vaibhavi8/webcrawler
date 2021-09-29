from bs4 import BeautifulSoup
import requests
import csv 

def main():
    f = open('./repository/report.csv', 'w')
    writer = csv.writer(f)

    seed = requests.get('https://www.espn.com/')
    #print(seed.text)

    parser = BeautifulSoup(seed.content, 'html.parser')
    links = []
    for i in parser.find_all('a', attrs={'class': 'quicklinks_list__link'}) :
        links.append([i.text, i['href']])
    writer.writerows(links)

    print(links[0])
    f.close()

if __name__ == '__main__':
    main()