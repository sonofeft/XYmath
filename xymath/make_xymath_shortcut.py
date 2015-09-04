import os, sys
import pythoncom
try:
    from win32com.shell import shell, shellcon
except:
    print('WARNING... win32com.shell did NOT import properly.')
    print('Can NOT create desktop shortcut')
    print('='*55)
    sys.exit()


'''The requirement: Create a shortcut on the desktop to the Python executable.

A small explanation. Shortcuts are stored as .lnk files in the filesystem, 
but they're represented within the shell as IShellLink objects whose 
IPersistFile implementation uses the .lnk file as its storage backend. 
Therefore, to create a shortcut, you instantiate an IShellLink object, 
use the methods of the IShellLink interface to fill in its details, and 
then call its IPersistFile.Save method to write it away to the corresponding 
link file on-disk.'''

pypath = sys.executable
head,tail = os.path.split( pypath )
xypath = head + r'\Lib\site-packages\xymath\gui\xygui.py'
iconpath = head + r'\Lib\site-packages\xymath\gui\XYmath128.ico'

shortcut = pythoncom.CoCreateInstance (
  shell.CLSID_ShellLink,
  None,
  pythoncom.CLSCTX_INPROC_SERVER,
  shell.IID_IShellLink
)
shortcut.SetPath (pypath)
shortcut.SetArguments(xypath)
shortcut.SetDescription ("XYmath")
shortcut.SetIconLocation (iconpath, 0)

desktop_path = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)
persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
persist_file.Save (os.path.join (desktop_path, "xymath.lnk"), 0)

# http://timgolden.me.uk/python/win32_how_do_i/create-a-shortcut.html