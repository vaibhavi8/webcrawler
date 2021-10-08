from bs4 import BeautifulSoup
from langdetect import detect
import requests
import random
import time


# Tests if text in title tag matches the desired language
def detect_language(lang, t):
    try:
        return detect(t) == lang
    except Exception as e:
        print(e)
    return False


# Initializes web scraper with seed URL and desired language
# The langdetect library uses supports 55 languages: https://pypi.org/project/langdetect/
# Assumes that an appropriate repository has already been created (i.e. repository-en, repository-fr, etc.)
def scrape(seed_url, repo_lang):
    seed = requests.get(seed_url)
    parser = BeautifulSoup(seed.content, 'html.parser')
    # Dictionary where key is url and value is number of outlinks
    links = {}
    # Minimum number of links to crawl
    crawled = 0
    target = 500

    while crawled < target:
        for i in parser.find_all("a", href=True):
            if i['href'].startswith('https'):
                link_url = i['href']
                if link_url not in links.keys():
                    doc = requests.get(link_url)
                    parser = BeautifulSoup(doc.content, 'html.parser')

                    # detect language
                    if parser.title is not None:
                        title = parser.title.text
                    else:
                        title = 'No title provided'
                    try:
                        if detect_language(repo_lang, title):
                            crawled += 1
                            report = './repository-' + repo_lang + '/docs.html'
                            with open(report, 'a') as f:
                                f.write('\n' + str(doc.content))
                                f.close()
                            find_text(doc.content, repo_lang)
                        else:
                            continue
                    except AtributeError as e:
                        print(e)

                else:
                    continue

                print("%s%%" %
                      str(float(crawled)/float(target)*100))

                # Get number of outlinks
                outlinks = 0
                for i in parser.find_all("a", href=True):
                    if i['href'].startswith('https'):
                        outlinks += 1
                # Store URL and number of outlinks in dictionary
                links[link_url] = outlinks
                print(str(link_url + " " + str(outlinks)))
                if crawled > target:
                    break

        # Get random link to crawl next
        doc = requests.get(random.choice(list(links.keys())))
        parser = BeautifulSoup(doc.content, 'html.parser')
        time.sleep(1.5)

    # Write URL and number of outlinks to CSV
    report = './repository-' + repo_lang + '/report.csv'
    f = open(report, 'w')
    for k, v in links.items():
        f.write(k + " " + str(v) + "\n")


def find_text(doc, repo_lang):
    soup = BeautifulSoup(doc, 'html.parser')
    p_tags = soup.find_all('p')
    for i in p_tags:
        if len(i.get_text()) > 200:
            print('here')
            report = './repository-' + repo_lang + '/text.txt'
            with open(report, 'a') as file:
                file.write(i.get_text() + '\n')
                file.close()

def main():
    time_start = time.time()
    scrape('https://cbsnews.com', 'en')                     # english
    time_end = time.time()
    print('Time elapsed: ' + str(time_end - time_start) + 'sec')

    # time_start = time.time()
    # scrape('https://www.20minutes.fr/', 'fr')               # french
    # time_end = time.time()
    # print('Time elapsed: ' + str(time_end - time_start) + 'sec')

    # time_start = time.time()
    # scrape('https://elpais.com/america/', 'es')               # spanish
    # time_end = time.time()
    # print('Time elapsed: ' + str(time_end - time_start) + 'sec')


if __name__ == '__main__':
    main()
