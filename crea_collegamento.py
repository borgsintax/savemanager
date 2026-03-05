import os
import winshell
from win32com.client import Dispatch

def create_desktop_shortcut():
    desktop = winshell.desktop()
    path = os.path.join(desktop, "Save Manager.lnk")
    
    # Percorso del file batch che abbiamo appena creato
    current_dir = os.path.dirname(os.path.abspath(__line__ if '__line__' in locals() else __file__))
    target = os.path.join(current_dir, "Avvia_SaveManager.bat")
    
    # Percorso dell'icona di python come icona di default
    icon = "python.exe"

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = current_dir
    shortcut.IconLocation = icon
    shortcut.save()
    
    print(f"Collegamento creato sul desktop: {path}")

if __name__ == "__main__":
    create_desktop_shortcut()
