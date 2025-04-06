# HEI-VPN

**HEI-VPN** is a plug-and-play Linux application that allows seamless connection to the Ivanti VPN used by the Haute École d'Ingénierie (HEI).

---

## 📚 Table of Contents

- [Context](#context)
- [Key Features](#key-features)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Improvements over the Original Project](#improvements-over-the-original-project)
- [Credits](#credits)
- [Licenses](#licenses)

---

## 🎯 Context

The official VPN client provided by HEI (Ivanti Secure Access) is **not compatible with Linux**.  
**HEI-VPN** was created to address this gap by providing a reliable, portable, and easy-to-use alternative that requires no manual setup. This project is heavily inspired by [**hei-vpn-for-linux**](https://git.kb28.ch/HEL/hei-vpn-for-linux.git) by [**kb28**](https://git.kb28.ch).

---

## ✨ Key Features

- Automatic connection to the HEI's Ivanti VPN
- Detects when already inside the HEI network (prevents redundant connection)
- Console interface
- Extracts `DSID` cookie from Firefox automatically
- Manages and cleans temporary Firefox profile
- Graceful shutdown with `Ctrl+C`
- Delivered as an **AppImage** for portable execution
- **No dependencies required** – everything is bundled

---

## ▶️ Usage

### 🖥️ 1. Use the AppImage (recommended for most users)

1. **Download the AppImage** from the [releases page](#).
2. **Make it executable**:
   ```bash
   chmod +x HEI-VPN.AppImage
   ```
3. **Run the application**:
   ```bash
   ./HEI-VPN.AppImage
   ```
4. *(Optional)* **Add it to your app launcher**:
   - Use [Gear Lever](https://github.com/TheAssassin/AppImageLauncher) or any launcher editor (like `menulibre`, `alacarte`, `kmenuedit`) to integrate the AppImage into your system menu.

---

### 🐍 2. Install via `pip` (developer/advanced usage)

If you prefer Python package management or want system-wide access:

1. **Install the package locally**:
   ```bash
   pip install .
   ```
2. **Run from anywhere using the CLI command**:
   ```bash
   hei-vpn
   ```

---

### 👨‍💻 3. Run directly from source (dev mode)

If you’re modifying or testing the source code:

1. **Clone the repository** (or navigate to your local copy).
2. **Run the main script manually**:
   ```bash
   python3 -m hei_vpn
   ```

---

### 🧠 Note

- The application will automatically generate a `config.json` in `~/.config/hei-vpn/` the first time you run it.
- No manual installation of `geckodriver` or VPN software is needed — everything is embedded or handled by the app.

ℹ️ Firefox must be installed with at least one default profile.

---

## ⚙️ How It Works

- **Network check**: Prevents VPN use if already inside the HEI network
- **Browser automation**: Uses Selenium and geckodriver to open Firefox and retrieve the authentication cookie
- **VPN connection**: Launches `openconnect` with the `nc` protocol using the `DSID` cookie
- **Profile management**: Temporary Firefox profile is copied, used, cleaned, and restored
- **Signal handling**: `Ctrl+C` is intercepted to gracefully shut down the VPN connection and clean up resources

---

## 🆚 Improvements over the Original Project

This project is heavily inspired by [**hei-vpn-for-linux**](https://git.kb28.ch/HEL/hei-vpn-for-linux.git) by [**kb28**](https://git.kb28.ch), with the following enhancements:

| Feature                        | HEI-VPN                                     |
|--------------------------------|---------------------------------------------|
| AppImage packaging             | ✅ double-clickable App                     |
| Pip Package                    | ✅ hei-vpn command                          |
| Python main\.py                | ✅ python3 -m hei-vpn                       |
| Pre-installed dependencies     | ✅ Only requires **pyinstaller**, if building the AppImage from source|
| Advanced profile handling      | ✅ Copy/clean/permissions                   |
| Automatic cleanup              | ✅ Full Check                               |
| Multi-distro compatibility     | ✅ Does not rely on distro files structures |
| User experience                | ✅ Plug-and-play                            |

---

## 🙌 Credits

- Developed by **Zoatik** (© 2025)
- Inspired by [**hei-vpn-for-linux**](https://git.kb28.ch/HEL/hei-vpn-for-linux.git) by [**kb28**](https://git.kb28.ch)
- Built using the following open-source components:

### 🔸 geckodriver (Mozilla)
- Purpose: Firefox WebDriver automation
- License: Mozilla Public License 2.0 (MPL 2.0)
- Source: https://github.com/mozilla/geckodriver

### 🔸 appimagetool (AppImage Project)
- Purpose: Packaging HEI-VPN into a portable AppImage format
- License: MIT
- Source: https://github.com/mozilla/geckodriver

### 🔸 selenium (SeleniumHQ)
- Purpose: Web browser control
- License: Apache License 2.0
- Source: https://github.com/AppImage/appimagetool

### 🔸 psutil
- Purpose: Process and system monitoring
- License: BSD 3-Clause
- Source: https://pypi.org/project/psutil/

### 🔸 requests
- Purpose: HTTP requests in Python
- License: Apache License 2.0
- Source: https://pypi.org/project/requests/

---

## 📄 Licenses

The main source code of this project is published under the **MIT License**:

```
MIT License

Copyright (c) 2025 Zoatik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell    
copies of the Software, and to permit persons to whom the Software is        
furnished to do so, subject to the following conditions:                     

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.                             

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 📌 About hei-vpn-for-linux

The project [**hei-vpn-for-linux**](https://git.kb28.ch/HEL/hei-vpn-for-linux.git) does not declare an explicit license.  
Its code was studied and adapted for educational and technical purposes. 

---
