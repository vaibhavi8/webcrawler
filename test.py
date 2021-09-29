import analysis

# File to test the text analysis
def main():
    try:
        file = open("text.txt", encoding = "utf8")
        text = file.read()
        file.close()

        analysis.create_zipf(text)
        analysis.create_heaps(text)
    
    except IOError as e:

        print(e)
main()