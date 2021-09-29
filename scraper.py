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
    for i in parser.find_all("a", href=True) :
        if i['href'].startswith('https'):
            link_url = i['href']
            links.append([i.text, link_url, (len(links)+1)])        
    writer.writerows(links)
    print(len(links))
    f.close()

if __name__ == '__main__':
    main()