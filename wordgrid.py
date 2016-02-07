#!/usr/bin/env python

import getopt
import sys
import re

class WordDict(object):
    def __init__(self, wordFile):
        self.words = []
        try:
            fp = open(wordFile)
        except IOError as (errno, strerror):
            print "Unable to open file {0} : ({1}): {2}".format(
                wordFile, errno, strerror)
            return

        for word in fp:
            if len( word.strip() ) > 0:
                self.words.append( word.strip().upper() )

    def find(self, text):
        found =[]
        for word in self.words:
            match = re.search(word, text)
            if match:
                found.append( (match.start(), match.end()) )
                continue

            # see if word is reversed in text
            match = re.search(word[::-1], text)
            if match:
                found.append( (match.start(), match.end()) )
                continue

        return found

class WordGrid(object):
    def __init__(self, dictFile, gridFile):
        self.grid = []

        try:
            fp = open(gridFile)
        except IOError as (errno, strerror):
            print "Unable to open file {0} : ({1}) : {2}".format(
                gridFile, errno, strerror)
            return

        for line in fp:
            length = len( line.strip() )
            if length > 0:
                # add a blank row above first text row and
                # then between text rows
                self.grid.append( (2*length + 1) * ' ' )
                self.grid.append( ' ' + ' '.join(line.strip().upper()) + ' ' )

        # add a blank row after last row of text
        self.grid.append( (2*length + 1) * ' ' )
        self.wordDict = WordDict(dictFile)

    def display(self):
        for line in self.grid:
#            text = ""
#            prev = ""
#            for i in range(0, len(line)):
#                if line[i] not in ('(', ')',' ','*') and prev not in ('(', ')','*'):
#                    text += " "
#
#                text += line[i]
#                prev = line[i]

#            print text
            print line

    def insertParen(self, line):
        new_str = line
        line = ''.join(line.split())
        found = self.wordDict.find( line )

        if found:
            starts=[]
            ends=[]
            for match in found:
                (start,end) = match
                starts.append( start )
                ends.append( end )

            all_indexes = starts + ends
            all_indexes = list(set(all_indexes)) # remove dups
            all_indexes.sort(reverse=1)

            #maybe add some asserts about starts and ends
            for index in all_indexes:
                if index > len(line):
                    new_str += ')'
                else:
                    paren = '('

                    if index in ends:
                        paren = ')'
                    if index in starts and index in ends:
                        paren = '*'

                    liststr = list(new_str)
                    liststr[2*index] = paren
                    new_str = ''.join(liststr)
#                    new_str = new_str[0:2*index] + paren + new_str[2*index:len(new_str)]

        return new_str


    def solve(self):
        # find horizontal matches
        for i in range( 0, len(self.grid) ):
            if i % 2 == 0:
                continue
            self.grid[i] = self.insertParen(self.grid[i])

        print 'finding vertical matches'

        # find vertical matches
        # change the grid to a list of lists
        # so that can do individual char subst
        # in columns
        for i in range( 0, len(self.grid) ):
            self.grid[i] = list(self.grid[i])
        for c in range( 0, len(self.grid[1]) ):
            if c % 2 == 0:
                continue;
            text = ""
            for r in range( 0, len(self.grid) ):
                text += self.grid[r][c]

            text = self.insertParen(text)
            for r in range( 0, len(self.grid) ):
                self.grid[r][c] = text[r]

        # change the grid back to a list of strings
        for r in range( 0, len(self.grid) ):
            self.grid[r] = ''.join(self.grid[r])

        self.display()

def usage():
    print "wordgrid.py implements an algorithm to solve a word search puzzle.\n"
    print "Usage:\n"
    print "wordgrid.py --[d]ictionary dictfile --[g]ridfile grid_file\n"
    print "where:\n"
    print "dictfile is the filename of a file with the words to find in the grid"
    print "with each word on a separate line\n"
    print "grid_file is the filename of an NxM grid of letters to search"
    print "for the words contained in dictfile\n"

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hd:g:", ["help", "dictionary=", "gridfile="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    if len(argv) == 0:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-d", "--dictionary"):
            dictFile = a
        if o in ("-g", "--gridfile"):
            gridFile = a

    puzzle = WordGrid(dictFile, gridFile)
    puzzle.solve()

if __name__ == "__main__":
    main(sys.argv[1:])
