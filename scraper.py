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
    num_links = 500

    # Get 500 links using seed
    while len(links) < num_links:
        for i in parser.find_all('a', href=True):
            if i['href'].startswith('http'):
                link_url = i['href']

                # Append html textual content to file
                filename = './repository-' + repo_lang + '/text.txt'
                f = open(filename, 'a')
                next_link = requests.get(link_url)
                # Check if link is already in dictionary
                if link_url not in links:
                    parser = BeautifulSoup(next_link.content, 'html.parser')
                    if parser.title is not None:
                        title = parser.title.text
                    else:
                        title = 'No title provided'

                    # Checks if title of page is in the appropriate language
                    try:
                        if detect_language(repo_lang, title):
                            # Extracts text based on surrounding tags
                            text_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'nav', 'ul', 'ol', 'li']
                            for i in text_tags:
                                # Returns a list with searched tags
                                text = parser.find_all(i)
                                # Iterates through list if list is not empty
                                if text:
                                    for k in text:
                                        f.write(k.text.encode('utf-8'))

                            # Get number of outlinks
                            outlinks = 0
                            for i in parser.find_all("a", href=True):
                                if i['href'].startswith('https'):
                                    outlinks += 1
                            # Store URL and number of outlinks in dictionary
                            links[link_url] = outlinks

                    except AttributeError as e:
                        print(e)

                # close file
                f.close()

                # Console output - crawl progress
                if parser.title is not None:
                    title = parser.title.text
                    print(title)
                print("%s%%" %
                      str(float(len(links)) / float(num_links) * 100))

                if len(links) > num_links:
                    break
                # Pause program to decrease timeout likelihood
                time.sleep(0.5)

        # Get random link to crawl next
        next_link = requests.get(random.choice(list(links.keys())))
        parser = BeautifulSoup(next_link.content, 'html.parser')

    # Write URL and number of outlinks to CSV
    report = './repository-' + repo_lang + '/report.csv'
    f = open(report, 'w')
    for k, v in links.items():
        f.write(k + " " + str(v) + "\n")
    f.close()


def main():
    time_start = time.time()
    scrape('https://cbsnews.com', 'en')                     # english
    time_end = time.time()
    print('Time elapsed: ' + str(time_end - time_start) + 'sec')

    time_start = time.time()
    scrape('https://www.20minutes.fr/', 'fr')               # french
    time_end = time.time()
    print('Time elapsed: ' + str(time_end - time_start) + 'sec')

    # time_start = time.time()
    # scrape('https://www.joongang.co.kr/', 'ko')     # korean
    # time_end = time.time()
    # print('Time elapsed: ' + str(time_end - time_start) + 'sec')

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