# -Import libs -----------------------------------------------------------------
import requests
import sys
import os

# -- constants and variables ---------------------------------------------------
mainUrl                 = "https://www.rdwdata.nl/merken/subaru/impreza+gt+turbo+awd/"
kentekens_start         = '<li><a href="https://www.rdwdata.nl/kenteken/'
kenteken_eerste_afgifte = 'Datum eerste afgifte Nederland'
kenteken_aanvang        = 'Datum aanvang tenaamstelling'
numPages                = 2
tot = [] ;# all 1st owners
j = 0    ;# count number of registered owners
z = 0    ;# URL page ID

# -- main ----------------------------------------------------------------------
while z < numPages:
  z = z+1
  url = mainUrl + str(z)
  r = requests.get(url, allow_redirects=True)
  
  for line in r.content.split('\n'):
    if (line.find(kentekens_start) != -1):
      j=j+1
      nurl = line.split('"')[1]
      kenteken = nurl.split('/')[-1]
      print('Checking ' + kenteken + ' in page ' + str(z))
      sys.stdout.flush()
      
      # load car page
      i = 0
      nr = requests.get(nurl, allow_redirects=True)
      kdata = nr.content.split('\n')
      d1 = ""
      d2 = ""
      
      # extract the relevant dates
      for nline in kdata:
        if (nline.find(kenteken_eerste_afgifte) != -1):
          d1 = kdata[i+2].strip()
          #print('  Datum eerste afgifte Nederland : ' + d1)
        if (nline.find(kenteken_aanvang) != -1):
          d2 = kdata[i+2].strip()
          #print('  Datum aanvang tenaamstelling   : ' + d2)
        i = i+1
  
      # do they match? then 1st owner found
      if (d1 == d2):
        print('  First owner on ' + d1 + ', nr ' + str(len(tot)+1))
        sys.stdout.flush()
        tot.append(kenteken + ' @ ' + d1.split('>')[1].split('<')[0])

# -- Print summary and format the list of 1st owners and dates -----------------
print('\nTotal of first owners: ' + str(len(tot)) + ', out of a total of ' + str(j) + ' registrations scanned...')
lst = ''
tot.sort()
for line in tot:
  print('  ' + line)
  lst = lst + line + '\r\n'

# -- write to a file and open for viewing --------------------------------------
open('results.lst', 'wb').write(lst)
os.system('notepad results.lst')
exit
