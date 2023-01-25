import subprocess
import os
import sys
import win32gui
import win32console


if __name__ == '__main__':
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)
    subprocess.run(['python', f"{os.path.join(sys.argv[1], 'app', 'main.py')}"])
    sys.exit()
