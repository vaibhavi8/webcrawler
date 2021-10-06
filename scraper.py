from bs4 import BeautifulSoup
import requests
import random


def main():
    seed = requests.get('https://espn.com')
    parser = BeautifulSoup(seed.content, 'html.parser')

    # Dictionary where key is url and value is number of outlinks
    links = {}

    # Get 500 links using seed
    while(len(links) < 500):
        for i in parser.find_all("a", href=True):
            if i['href'].startswith('https'):
                link_url = i['href']
                # append html to file
                filename = "./repository/text.html"
                f = open(filename, "a")
                nextLink = requests.get(link_url)
                parser = BeautifulSoup(nextLink.content, 'html.parser')
                # check if link is already in dictionary
                if links.has_key(link_url) == False:
                    f.write(nextLink.content)
                if parser.title != None:
                    title = parser.title.text
                    print(title)
                print("%s%%" %
                      str(float(len(links))/float(500)))
                if(len(links) > 500):
                    break
                f.close
                # Get number of outlinks
                outlinks = 0
                for i in parser.find_all("a", href=True):
                    if i['href'].startswith('https'):
                        outlinks += 1
                # Store URL and number of outlinks in dictionary
                links[link_url] = outlinks
        # Get random link to crawl next
        nextLink = requests.get(random.choice(list(links.keys())))
        parser = BeautifulSoup(nextLink.content, 'html.parser')

    # Write URL and number of outlinks to CSV
    f = open('./repository/report.csv', 'w')
    for k, v in links.items():
        f.write(k + " " + str(v) + "\n")


if __name__ == '__main__':
    main()
