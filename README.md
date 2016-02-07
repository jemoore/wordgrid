WordGrid
========

This is a word search puzzle solver.

At the moment it only finds horizontal and vertical matches.

A sample dictionary and search puzzle are provided.

This was a 'toy' afternoon experiement.  The most difficult part was to
display the puzzle in ASCII with found words encapsulated between ( ).

For vertical words a ( will appear above a letter and ) will appear below
a letter.

A * indicates the end and start of a match ' )(' 

How to indicate a diagonal match?

Would benifit from using pyside or pygame.

Unfortunately my intrest subsided.  Will try to eventually get back to complete.

The implementation is brute force, examaning each row and column of letters
looking for a match in the dictionary.
