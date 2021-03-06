# RDW-First-Owners
Extracts first owners of cars from the [Dutch RDW site](https://www.rdwdata.nl/merken/) Author has specifically chosen not to extract this data by means of the Open Data sets that the RDW organisation provides. Instead, author opted for extraction of data from the webpages themselves, which are a translation of these datasets. There might be a faster way to extract this data, but author is satisfied with the results, since the main reason to create it was to collect more programming knowledge in Python by setting a simple challenge. Feel free to propose a different, better way of extracting this data, so the whole community can benefit.

## Some pre conditions and have-to-knows:
- Tested & created with Python 2.7.14 on a Windows 10 machine
- Using gtk library v2.22.1 & PyGtk library v2.22.0
- Script outputs progress on the GUI, when finished user can order a summary via the File-menu. 
- This script is created out of curiousity, to compare the effort to develop it against my old-time favorite scripting language tcl/tk

## Limitations & main features
- The limiations of the first branch-release has been fixed/updated. Now, an additional compare against the manufacturing date is performed to extract the real "FIRST-TIME" owner of the car.
- User can define a different car brand & model from the Options menu
- Color coding of detected first owners during extraction
- An extraction can be initiated from the menu or the play/stop button next to the progressbar.
- Script v1.1 is able to dynamically determine the number of pages for different brand/models
- Last but not least, script has not been optimized and there is a lot of redundancy present, please reuse with caution!

## This Release
This version has a GUI to follow and control the extraction progress. It's a quick and dirty implementation, so bear with me as I am also still learning the ins & outs of Python...

## Some Screenshots
![GUI_transp](https://user-images.githubusercontent.com/22547835/84597009-373c9780-ae61-11ea-8e5c-0791c495c931.png)
