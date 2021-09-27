from bs4 import BeautifulSoup
import requests

def main():
    seed = requests.get('https://www.espn.com/')
    print(seed.text)

    parser = BeautifulSoup(seed.text, 'html.parser')
    

if __name__ == '__main__':
    main()