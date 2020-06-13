# RDW-First-Owners
Extracts first owners of cars from the Dutch RDW site

Some pre conditions and have-to-knows:
- Tested with Python 2.7 on a Windows 10 machine
- Script outputs progress on the DOS terminal, when finished a file is written out with the results. 
- Results file is opened for viewing by calling the default text editor of Windows (notepad), when closed, the DOS terminal also closes
- This script is created out of curiousity, to compare the effort to develop it against my old-time favorite scripting language tcl

This script has a standard BSD license, would be nice to refer to my name if you use it.

WORDS OF CAUTION:
The entries that are identified as first-time owners are license plates that have been registered in the Netherlands and on equal date assigned to an owner who has not changed since that date. If the actual age of the car is older, such as in the case if it is imported as a second hand from outside of the Netherlands, this is not known or not taken into consideration in this first release of the script. In such cases, the car in question could be considered not being a first-time owner indeed... If I have some more time, I could implement comparing  against the manufacturing date of the car to determine if it is really a "FIRST-TIME" owner...
