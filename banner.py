#-*- coding: utf-8 -*-
from sys import argv
from sys import getfilesystemencoding
from os.path import dirname
from os.path import splitext
from os.path import exists
from os import remove
from os import rename
from os import walk
from chardet.universaldetector import UniversalDetector
import codecs
import re

DEFAULT_ORDER = ['Name', 'Fontname', 'Fontsize', 'PrimaryColour', 'SecondaryColour',
                'OutlineColour', 'BackColour', 'Bold', 'Italic', 'Underline',
                'StrikeOut', 'ScaleX', 'ScaleY', 'Spacing', 'Angle', 'BorderStyle',
                'Outline', 'Shadow', 'Alignment', 'MarginL', 'MarginR', 'MarginV', 'Encoding']

DEFAULT_OPTIONS = {'Fontname': u'方正准圆_GBK', 'OutlineColour': '&H00000000',
                'Angle': '0', 'PrimaryColour': '&H00FFFFFF', 'BackColour': '&H00000000',
                'Italic': '0', 'BorderStyle': '1', 'MarginL': '10', 'Bold': '-1',
                'Spacing': '0', 'Fontsize': '35', 'Shadow': '0', 'Outline': '1.5',
                'Name': 'Default', 'ScaleX': '100', 'ScaleY': '100',
                'SecondaryColour': '&H000000FF', 'MarginR': '10',
                'MarginV': '10', 'StrikeOut': '0', 'Encoding': '1',
                'Underline': '0', 'Alignment': '2'}

def getname(options):
    ops = options.split(':')[1].strip()

    return ops.split(',')[0].strip()

def rebuildOptions(options):
    result = 'Style: '
    for name in DEFAULT_ORDER:
        result += options[name] + ','

    return result[0:len(result) - 1]

def adjustOptions(filename, encoding):
    bskip = False
    tmpfile = filename + '.tmp'

    try:
        # Encode detect
        detector = UniversalDetector()
        for line in file(filename, 'rb'):
            detector.feed(line)
            if detector.done: break

        detector.close()

        encoding = detector.result['encoding']

        with codecs.open(filename, 'r', encoding) as hread, codecs.open(tmpfile, 'w+', encoding) as hwrite:
            for line in hread:
                line = line.strip()

                if len(line) == 0: continue

                if not bskip:
                    if re.match('[Event]', line):
                        bskip = True
                        continue

                    if re.search('^Style:\s', line) != None:
                        options = DEFAULT_OPTIONS.copy()
                        options['Name'] = getname(line)

                        line = rebuildOptions(options)

                hwrite.write(line + "\n")

        remove(filename)
        rename(tmpfile, filename)
    except Exception as e:
        print "%s\n" % e
    finally:
        if exists(tmpfile): remove(tmpfile)

def main():
    pwd = dirname(__file__)
    filext = ".ass"
    filecoding = "UTF-8"
    filelist = []

    if len(argv) >= 2:
        pwd = argv[1]
    # Encoding issue
    pwd = unicode(pwd, getfilesystemencoding())

    for root, sub, fl in walk(pwd):
        for fn in fl:
            drop, ext = splitext(fn)
            if ext == filext:
                filelist.append(u'%s\\%s' % (pwd, fn))

    if len(filelist) == 0:
        print 'No subtitle file found.'
        return

    for fn in filelist:
        adjustOptions(fn, filecoding)

    print 'All Done! Enjoy!'

if __name__ == "__main__":
    main()
