import os


directory = 'the/directory/you/want/to/use'

def doIt()

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            f = open(filename)
            lines = f.read()
            print (lines[10])
            continue
        else:
        continue

def main():
    pass



if __name__ == '__main__':
    main()


