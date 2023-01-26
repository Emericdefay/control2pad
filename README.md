<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="./com/logo.png" alt="Logo"></a>
</p>

<h3 align="center">Control the controlpad</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/emericdefay/control2pad.svg)](https://github.com/emericdefay/control2pad/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/emericdefay/control2pad.svg)](https://github.com/emericdefay/control2pad/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Unleash the true power of your Controlpads
    <br> 
</p>

<h2> 📝 Table of Contents </h2>

- [🧐 About ](#-about-)
- [✔ Available controlpads](#-available-controlpads)
- [🏁 Getting Started ](#-getting-started-)
  - [Prerequisites](#prerequisites)
  - [Libusb](#libusb)
- [🎈 Usage ](#-usage-)
- [🚀 Additional Features ](#-additional-features-)
- [📌 Conclusion ](#-conclusion-)
- [⛏️ Built Using ](#️-built-using-)
- [✍️ Authors ](#️-authors-)

## 🧐 About <a name = "about"></a>

This project is designed to allow users to customize their keyboard shortcuts and actions. It allows users to assign specific actions to individual keys on their keyboard, such as running a Python script or launching a program. The program also saves these configurations in a keyboard.json file, so that the settings persist even after the program is closed.

## ✔ Available controlpads

|VID   |PID    |Manufacturer	     |Product               |
|------|-------|-------------------|----------------------|
|0x2516|0x007B |Cooler Master	     |Cherry                |

Products are stored in `app/layouts`  
I would like to create a "layout generator" to complete this tool.


## 🏁 Getting Started <a name = "getting_started"></a>

To get started with this project, you will need to have Python 3 and the PyQt5 library installed on your system. You can install these dependencies using pip by running the following command:

```
pip install -r requirements.txt
```

Once these dependencies are installed, you can run the program by executing the `launcher.py` script.

### Prerequisites

- Python > 3.6
- Controlpad
- libusb-win32

### Libusb

Please read this guide to setup this important lib: [How to use libusb](https://github.com/libusb/libusb/wiki/Windows#how-to-use-libusb-on-windows)

## 🎈 Usage <a name="usage"></a>

When the program is first run, it will display a button asking you to select a device. It will list all devices that your allowed through `libusb`. Select one of them.

After that, it will display a window with a grid of buttons representing the keys on your keyboard. When you click on a key, a dialog will appear allowing you to configure the action for that key. You can choose to run a Python script, launch a program, or assign a keyboard shortcut to the key.

After making your selections, you can click the "Save" button to save the configuration for that key. The program will automatically save all key configurations to the `keyboard.json` file, so that they persist even after the program is closed.

When the program is restarted, it will automatically load the `keyboard.json` file and apply the saved configurations to the keys on the grid.

## 🚀 Additional Features <a name = "additional"></a>

Your can handler several keyboards at the same time by adding tabs.

The program also includes a few additional features, such as the ability to display a help dialog when a specific key is pressed. The help dialog will display information about the current key's configuration, and will close automatically after 10 seconds.


## 📌 Conclusion <a name="conclusion"></a>

This project provides a powerful and flexible tool for customizing keyboard shortcuts and actions. It is designed to be easy to use and customize, and it allows users to easily assign actions to individual keys on their keyboard. With the ability to save and load configurations, as well as additional features such as the help dialog and simulated keyboard input, this program is a valuable tool for anyone looking to increase their productivity and efficiency.


## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://www.Python.com/) - Language
- [Libusb](https://github.com/libusb/libusb) - HID API
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - Applications Framework

## ✍️ Authors <a name = "authors"></a>

- [@Emericdefay](https://github.com/Emericdefay) - Idea & Initial work
