import analysis


# File to test the text analysis
def main():
    eng = './repository-en/text.txt'
    frn = './repository-fr/text.txt'
    spn = './repository-es/text.txt'

    try:
        file = open(spn, encoding = "utf8")
        text = file.read()
        file.close()

        analysis.create(text)
    
    except IOError as e:
        print(e)


if __name__ == '__main__':
    main()