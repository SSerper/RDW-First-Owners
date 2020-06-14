#!/usr/bin/env python

# ---------------------------------------------------------------------------------------       
# Name              : RDWfirstowners_GUI.pyw - copyright 2020 by Sedat Serper -
# Author            : Sedat Serper
# Creation Date     : 12-06-2020
# Modification Date : 14-06-2020
# Version           : 1.1
# Description       : GUI to extract first-time owners of cars as registered at RDW site
# Input             : -
# Output            : on-screen progress
# Usage             : -
# Global variables  : see script...
# Keywords          : -
# Language          : python
# Category          : generic
# Dependencies      : gtk, os, sys, gobject, pygtk, requests, time, pyperclip
# To Do             : who knows...
# License           : BSD License
# ---------------------------------------------------------------------------------------

# -Import libs --------------------------------------------------------------------------
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import sys
import os 
import requests
from time import gmtime, strftime
import pyperclip

# - main globals here -------------------------------------------------------------
progTitle         = "RDW First Owner v"
ToolVersion       = "1.0"
programFont       = 'Consolas 11'
mainUrl           = "https://www.rdwdata.nl/merken/"
carUrl            = mainUrl + "subaru/impreza+gt+turbo+awd/"
numPages          = 2
toplevel          = None
IdleTxt           = "Idle..."
bizzyTxt          = "Bizzy..."
guiStatus         = IdleTxt
extrResults       = ""

# ---------------------------------------------------------------------------------
def getActiveGtkWindow():
  for w in getAllToplevels()[0]:
    if w.is_active():
      return w
  return None

# ------------------------------------------------------------------------------
def getMainToplevel():
  #print("------------->" + str(gtk.gdk.window_get_toplevels()))
  return gtk.gdk.window_get_toplevels()[0]

# ---------------------------------------------------------------------------------
def getAllToplevels():
  return [gtk.window_list_toplevels()]

# ---------------------------------------------------------------------------------
def ynBox(Parent=None, Title="Please respond?", msg="Here your question", type=(gtk.STOCK_YES, gtk.RESPONSE_YES, gtk.STOCK_NO, gtk.RESPONSE_NO, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)):
  response = gtk.RESPONSE_CANCEL
  dialog = gtk.Dialog(
    Title, 
    Parent, 
    gtk.DIALOG_MODAL, 
    (type)
  )
  dialog.get_content_area().add(gtk.Label(msg))
  dialog.get_content_area().set_size_request(300, 100)
  dialog.show_all()
  response = dialog.run()
  dialog.destroy()
  return response

# ---------------------------------------------------------------------------------
def mbox(Parent=None, Title="MessageBox", msg="Here your remark", icon="ok"):
  while switch(icon):
    if case("error"):
      icon = gtk.STOCK_DIALOG_ERROR
      break
    if case("info"):
      icon = gtk.STOCK_DIALOG_INFO
      break
    if case("warning"):
      icon = gtk.STOCK_DIALOG_WARNING
      break
    if case("ok"):
      icon = gtk.STOCK_OK
      break
    icon = gtk.STOCK_OK
    break

  dialog = gtk.Dialog(
    Title, 
    Parent, 
    gtk.DIALOG_MODAL, 
    (icon, gtk.RESPONSE_OK)
  )
  dialog.get_content_area().add(gtk.Label(msg))
  dialog.get_content_area().set_size_request(300, 100)
  dialog.show_all()
  dialog.run()
  dialog.destroy()

# ---------------------------------------------------------------------------------
class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

# ------------------------------------------------------------------------------
def defineMenuAcc(addItem, ar3, agr):
  # add the accell image and key(s), if provided...
  try:
    key, mod = gtk.accelerator_parse(ar3)
    addItem.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
  except:
    pass

# ------------------------------------------------------------------------------
def createMenuItem(mnu, pItem, agr):
  global rfManager
  
  txt = pItem[0]
  ar1 = pItem[1]
  ar2 = pItem[2]
  ar3 = pItem[3]
  mtype = pItem[4]
  
  if txt == "-":
    mnu.append(gtk.SeparatorMenuItem())
    return

  if (mtype==None) or (mtype==""):
    addItem = gtk.MenuItem(txt)
    addItem.connect_object ("activate", ar1, ar2)
  else:
    # STOCK icons
    if mtype.find("gtk-")>=0:
      addItem = gtk.ImageMenuItem(txt)
      image = gtk.Image()
      image.set_from_stock(mtype, gtk.ICON_SIZE_BUTTON)
      addItem.set_image(image)
      addItem.connect_object ("activate", ar1, ar2)
    else:
      while switch(mtype):
        if case("check"):
          addItem = gtk.CheckMenuItem(txt)
          addItem.connect_object ("toggled", ar1, [txt, ar2, addItem])
          break
        if case("radio"):
          addItem = gtk.RadioMenuItem(None, txt)
          addItem.connect_object ("toggled", ar1, ar2)
          break
        if case("recent_files"):
          # load recent-files to python-memory
          loadRecentFilesMenu(pItem[5])
          
          # create menu-entry
          addItem = gtk.ImageMenuItem(txt)
          image = gtk.Image()
          image.set_from_stock(gtk.STOCK_DND_MULTIPLE, gtk.ICON_SIZE_BUTTON)
          addItem.set_image(image)
          mnuchsr = gtk.RecentChooserMenu(rfManager)
          mnuchsr.connect("item-activated", ar1)
          mnuchsr.show()
          addItem.set_submenu(mnuchsr)
          break
        addItem = gtk.MenuItem(txt)
        addItem.connect_object ("activate", ar1, ar2)
        break
  if (ar3!=None) and (ar3!=''):
    defineMenuAcc(addItem, ar3, agr)

  mnu.append(addItem)
  addItem.show()
    
  return addItem

# ------------------------------------------------------------------------------
def sepList():
  return ["-", "", "", "", "", []]

# ------------------------------------------------------------------------------
def menuBar(self, struct=[
    ["File", 
      [
        ["Quit", gtk.main_quit, "file.quit pressed", "<Control>q", None, []]
      ]
    ]
  ]):
  
  # create the menu-bar  
  menu_bar = gtk.MenuBar()
  
  # create accel. group
  agr = gtk.AccelGroup()
  self.window.add_accel_group(agr)
  
  # create all menu items
  for mItem in struct:
    # create the main menu-object
    mnu = gtk.Menu() 

    # in case of radio's needed
    group = None

    # Create the sub-menu items
    for pItem in mItem[1]:
      # create menu item
      zitem = createMenuItem(mnu, pItem, agr)

      if (group!=None) and (pItem[4]=="radio"):
        group.set_group(zitem)
      group = zitem
      
      # does sub-menu contain another sub-menu?
      if (pItem[5]!=[]) and (type(pItem[5])!=str):
        smnu = gtk.Menu()
          
        # in case of radio's needed
        group = None
        
        for spItem in pItem[5]:
          # create menu item
          mitem = createMenuItem(smnu, spItem, agr)
          if (group!=None) and (spItem[4]=="radio"):
            group.set_group(mitem)
          group = mitem
  
        zitem.set_submenu(smnu)
          
    # now insert the main menu-items to the menu-bar
    item = gtk.MenuItem(mItem[0])
    item.show()
    item.set_submenu(mnu)
    item.set_right_justified(False)
    menu_bar.append(item)
  
  menu_bar.show_all()
  return menu_bar

# ------------------------------------------------------------------------------
# --------------------------- CUSTOMIZATION STARTS HERE ------------------------
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def destroyGtkWindow(self, window, Parent):
  try:
    print("--> Window '" + str(window.get_title()) + "' destroy pre-actions here...")
    Parent.present()
    Parent.set_accept_focus(True)
  except:
    if window==None:
      print("Destroy pre-actions here, triggered by menu...")
    pass 

# ------------------------------------------------------------------------------
class createToplevelLayout:
  # Clean up allocated memory and remove the timer, quit GUI
  def destroyToplevel(self, widget, data=None):
    try:
      destroyGtkWindow(self, widget, data)
    except:
      print("Pre-actions failed, check source code...")
      pass
      
    gtk.main_quit()
      
  def __init__(self):
    global Self
    global ToolVersion
    global progTitle
    global programFont
    
    Self = createToplevel(self, title=progTitle + ToolVersion)
    self = Self
    
    # create the customized GUI, hide progressbar widget
    align = gui(self)

setattr(createToplevelLayout, "destroyGtkWindow", destroyGtkWindow)

# ------------------------------------------------------------------------------
def createToplevel(self, title="tool", resize=True, bw=0, x=1300,y=25, W=400, H=250):
  global toplevel
  
  self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
  toplevel = self.window
  self.window.set_resizable(resize)
  self.window.connect("destroy", self.destroyToplevel)
  self.window.set_title(title)
  self.window.set_border_width(bw)
  self.window.move(x,y)
  self.window.set_size_request(W, H)
  return self

# ------------------------------------------------------------------------------
def printTxt(ptext, resetFirst=False):
  global textview
  global text_mark_end
  global c_tag

  bufferTxt = textview.get_buffer()
  if resetFirst==True:
    bufferTxt.set_text("",-1)

  text_iter_end = bufferTxt.get_end_iter()

  if ptext.find("*") != -1:
    #bufferTxt.remove_all_tags(text_iter_start, text_iter_end)
    bufferTxt.insert(text_iter_end, '      ')   
    text_iter_end = bufferTxt.get_end_iter()
    try:
      c_tag = bufferTxt.create_tag( "colored", foreground="green", background="gray30") 
    except:
      pass
    bufferTxt.insert_with_tags( text_iter_end, ptext + '\n' , c_tag)     
  else:
    ptext = ptext + '\n'
    bufferTxt.insert(text_iter_end, ptext)
  
  while gtk.events_pending():
    gtk.main_iteration_do(True)  
  # now scroll using mark
  textview.scroll_to_mark(text_mark_end, 0, False, 0, 0)

# ------------------------------------------------------------------------------
def determineNrPages():
  printTxt("Checking number of pages...", True)
  r = requests.get(carUrl, allow_redirects=True)
  ret = 1
  k = 0
  data = r.content.split('\n')
  for line in data:
    if (line.find(">pagina:<") != -1):
      z = 1
      k=k+1
      while (data[k].strip() != "") and (data[k].find("merken/") != -1):
        z=z+1
        k=k+1
      ret = z
      break
    k=k+1
  printTxt("Found a total of " + str(ret) + " page(s) to scan...\n")
  return ret

# ------------------------------------------------------------------------------
def extractCarOwners():
  global extrResults
  global sBar
  global carUrl
  global guiStatus
  global numPages
  
  guiStatus = bizzyTxt
  extrResults = ""

  numPages = determineNrPages()
  
  # -- constants and variables -------------------------------------------------
  kentekens_start         = '<li><a href="https://www.rdwdata.nl/kenteken/'
  kenteken_eerste_afgifte = 'Datum eerste afgifte Nederland'
  kenteken_aanvang        = 'Datum aanvang tenaamstelling'
  tot = [] ;# all 1st owners
  j = 0    ;# count number of registered owners
  z = 0    ;# URL page ID
  
  # start iterating the pages
  while z < numPages:
    if guiStatus == IdleTxt:
      break
    z = z+1
    url = carUrl + str(z)
    r = requests.get(url, allow_redirects=True)
    
    for line in r.content.split('\n'):
      if guiStatus == IdleTxt:
        break
      if (line.find(kentekens_start) != -1):
        j=j+1
        sBar.push(0, "Processing page " + str(z) + ' out of ' + str(numPages) + ', plate number ' + str(j))
        nurl = line.split('"')[1]
        kenteken = nurl.split('/')[-1]
        printTxt('Checking license-plate ' + kenteken)
        
        # load car page
        i = 0
        nr = requests.get(nurl, allow_redirects=True)
        kdata = nr.content.split('\n')
        d1 = ""
        d2 = ""
        d3 = ""
        
        # extract the relevant dates
        for nline in kdata:
          if (nline.find(kenteken_eerste_afgifte) != -1):
            d1 = kdata[i+2].strip()
            #print('  Datum eerste afgifte Nederland : ' + d1)
          if (nline.find(kenteken_aanvang) != -1):
            d2 = kdata[i+2].strip()
            #print('  Datum aanvang tenaamstelling   : ' + d2)
          if (nline.find("Bouwjaar") != -1):
            d3 = kdata[i+2].strip().split('>')[1].split('<')[0]
            #print('  Datum aanvang tenaamstelling   : ' + d2)
          i = i+1
    
        # do they match? then 1st owner found
        if (d1 == d2) and (d3 == d1.split('>')[1].split('<')[0].split('-')[-1]):
          printTxt('* First owner nr. ' + str(len(tot)+1) + ' found...')
          tot.append(kenteken + ' @ ' + d1.split('>')[1].split('<')[0])
  
  if guiStatus == IdleTxt:
    printTxt('\nProcess prematurely ended by user...')
  else:
    # -- Print summary and format the list of 1st owners and dates -----------------
    printTxt('\nTotal number of first owners: ' + str(len(tot)) + '\nTotal of license plates scanned: ' + str(j))
    lst = ''
    tot.sort()
    for line in tot:
      #print('  ' + line)
      lst = lst + '  ' + line + '\r\n'
    extrResults = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\r\n'
    extrResults = extrResults + 'URL: ' + carUrl + '\r\n' 
    extrResults = extrResults + 'Total number of first owners   : ' + str(len(tot)) + '\r\n'
    extrResults = extrResults + 'Total of license plates scanned: ' + str(j) + '\r\n\r\n'
    extrResults = extrResults + 'List of first owner license plates:\r\n'
    extrResults = extrResults + lst
    printTxt('\nFinished processing...')
    guiStatus = IdleTxt
    
  sBar.push(0, IdleTxt)
  
# ------------------------------------------------------------------------------
def menuResponse(data):
  global extrResults
  global guiStatus
  
  while switch(data):
    if case(0):
      #mbox(Self.window, "File IO", "Save summary")
      if guiStatus != IdleTxt:
        mbox(Self.window, "Extraction Interrupt", "An extraction is already active\nPlease try again later...")
      else:
        if extrResults == "":
          mbox(Self.window, "Empty Extraction", "Please initiate a complete extraction first...")
        else:
          pyperclip.copy(extrResults)
          printTxt(pyperclip.paste(), True)
      break
    if case(1):
      Self.destroyGtkWindow(None, toplevel)
      gtk.main_quit()
      break
    if case(2):
      if guiStatus != IdleTxt:
        mbox(Self.window, "Extraction Interrupt", "An extraction is already active\nPlease try again later...")
      else:
        changecarUrl()
      break
    if case(3):
      if guiStatus != IdleTxt:
        mbox(Self.window, "Extraction Interrupt", "An extraction is already active\nPlease try again later...")
      else:
        plyImage.set_from_stock(gtk.STOCK_MEDIA_STOP, gtk.ICON_SIZE_MENU)
        extractCarOwners()
      break
    if case(4):
      plyImage.set_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_MENU)
      guiStatus = IdleTxt
      break
    break

# ------------------------------------------------------------------------------
def verifyTheCarUrl(url):
  r = requests.get(url, allow_redirects=True)
  
  if str(r) == "<Response [404]>":
    return 0
  else:
    if (r.content.find("Voertuiggegevens") == -1) or (r.content.find("Gegevens ophalen") == -1):
      return 0
    else:
      printTxt('New url is accepted!', True)
      return 1
      
# ------------------------------------------------------------------------------
def verifyUrl(data=""):
  global urlentry
  global carUrl
  
  Parent = getActiveGtkWindow()
  url = mainUrl + urlentry.get_text()
  if verifyTheCarUrl(url) == 0:
    mbox(toplevel, Title="URL access failed", msg="url does not exist or not a valid brand-page?")
  else:
    carUrl = url.strip('/') + '/'
    printTxt('\nBrand : ' + url.split("/")[-2].upper())
    printTxt('Model : ' + url.split("/")[-1])
    Parent.destroy()

# ------------------------------------------------------------------------------
def changecarUrl():
  global urlentry
  
  title  = "Set new URL"
  W = 500
  H = 50
  Parent = getActiveGtkWindow()

  # this disables all key-board input event handlings...
  Parent.set_accept_focus(False)
  window = gtk.Window(gtk.WINDOW_TOPLEVEL)
  window.set_deletable(True)
  window.set_resizable(False)
  window.set_transient_for(Parent)
  window.set_modal(True)
  window.set_title(title)
  window.set_border_width(0)
  (x, y) = Parent.get_position()
  window.move(int(x + Parent.get_size()[0]/2 - W/2),int(y + Parent.get_size()[1]/2 - H/2))
  window.set_size_request(W, H)
  window.show()
  
  hbox = gtk.HBox(False, 1)
  hbox.set_border_width(10)
  window.add(hbox)
  hbox.show()

  nurl = gtk.Label(mainUrl)
  hbox.pack_start(nurl, expand=False)
  
  urlentry = gtk.Entry()
  hbox.pack_start(urlentry, expand=True)
  urlentry.set_text(carUrl[len(mainUrl):-1])

  btn = gtk.Button(" Verify ")
  hbox.pack_end(btn, expand=False)
  btn.connect("clicked", verifyUrl)
  
  window.show_all()
  
# ------------------------------------------------------------------------------
def fetchMenuBarItems():
  return [
    ["File", 
      [
        ["Show summary", menuResponse, 0,         None, None, []],
        sepList(),
        ["Quit",         menuResponse, 1, "<Control>q", gtk.STOCK_QUIT, []]
      ]
    ],
    ["Options",
      [
        ["Set new car & model page", menuResponse, 2,         None, None, []],
        sepList(),
        ["Start extraction...", menuResponse, 3,      None, None, []],
        ["Stop extraction", menuResponse, 4,      None, None, []],
      ]
    ]
  ]

# ------------------------------------------------------------------------------
def gui(self):
  global bufferTxt
  global textview
  global text_mark_end
  global sBar
  global plyImage
  
  # create a vertical box
  self.window.show_all()
  self.window.show()

  vbox = gtk.VBox(False, 1)
  vbox.set_border_width(2)
  self.window.add(vbox)
  vbox.show()
  
  # Create a centering alignment object
  align = gtk.Alignment(0.5, 0.5, 0, 0)
  vbox.pack_start(align, False, False, 0)
  align.show()

  menu_bar = menuBar(self, fetchMenuBarItems())
  vbox.pack_start(menu_bar, False, False, 0)

  # progress text-box
  
  scrolledwindow = gtk.ScrolledWindow()
  scrolledwindow.set_border_width(2)
  scrolledwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
  
  bufferTxt = gtk.TextBuffer()
  textview = gtk.TextView(buffer=bufferTxt)
  text_iter_end = bufferTxt.get_end_iter()
  text_mark_end = bufferTxt.create_mark("", text_iter_end, False)
  textview.set_editable(False)
  textview.set_cursor_visible(False) 
  scrolledwindow.add(textview)
  vbox.pack_start(scrolledwindow, True, True, 0)
  
  textview.show()
  printTxt('Ready for action...',True)

  shbox = gtk.HBox(False, 1)
  shbox.set_border_width(1)
  vbox.pack_end(shbox, expand=False)
  shbox.show()

  sBar = gtk.Statusbar()
  shbox.pack_end(sBar, expand=True)
  sBar.push(0, IdleTxt)

  button = gtk.Button()
  inner_box = gtk.HBox()
  button.props.relief = gtk.RELIEF_NORMAL
  plyImage = gtk.Image()
  plyImage.set_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_MENU)
  inner_box.add(plyImage)
  plyImage.show()
  button.add(inner_box)
  shbox.pack_start(button, expand=False)
  button.props.relief = gtk.RELIEF_NONE
  button.connect("clicked", toggleExtraction)
  button.show()

  #label = gtk.Label("Another label")
  #sBar.add(label)
  toplevel.show_all()

  return align

# ------------------------------------------------------------------------------
def toggleExtraction(data):
  global plyImage
  
  if guiStatus != IdleTxt:
    menuResponse(4)
  else:
    menuResponse(3)

# ------------------------------------------------------------------------------
def main():
  gtk.main()
  return 0

# ------------------------------------------------------------------------------
if __name__ == "__main__":
  mainInst = createToplevelLayout()
  main()

