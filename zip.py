# zip_un
import zipfile
import optparse
from threading import Thread


def extractFile(zFile, password):
    try:
        zFile.extractFile(pwd=password)
        print('found password'+password+'\n')
    except:
        pass


def main():
    parser = optparse.OptionParser('usage%prog' +
                                   '-f <zipfile> -d <dictionary>')
    parser.add_option('-d', dest='danme', type='string',
                      help='specify dictionary file')
    (options, args) = parser.parse_args()
    if (options.zname is None) | (optons.dname is None):
        print(parser.usage)
        exit(0)
    else:
        zname = optons.zname
        dname = options.dname
    zFile = zipfile.ZipFile(zname)
    passFile = open(dname)
    for line in passFile.readlines():
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile, password))
        t.start()


if __name__ == '__main__':
    main()
