import analysis


# File to test the text analysis
def main():
    eng = '.repository-en/text.txt'
    frn = '.repository-fr/text.txt'
    kor = '.repository-ko/text.txt'

    try:
        file = open("loremipsum.txt", encoding = "utf8")
        text = file.read()
        file.close()

        analysis.create(text)
    
    except IOError as e:
        print(e)


if __name__ == '__main__':
    main()