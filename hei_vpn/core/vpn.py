import os
import re
import signal
import subprocess
import time
import json

from .utils import load_config, getPublicIp
from .browser import startBrowser, closeBrowser
from .webdriver_helpers import AnyEc
from .logger import infoLogger, warningLogger, errorLogger, vpnLogger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def run_vpn():
    if getPublicIp() == "153.109.1.93":
        warningLogger.log("You are already in the HEI network. VPN is not needed.")
        exit()

    config = load_config()

    url = config["gateway"]
    timeout = config["timeout"]

    print("+-------------------+")
    print("| Accessing gateway |")
    print("+-------------------+")

    driver, dkey = startBrowser()

    infoLogger.log("Waiting for page to load...")

    tries = 0
    while tries < 5:
        time.sleep(1)
        try:
            driver.get(url)
            break
        except Exception as e:
            print(f"Error with Firefox: {e}")
            tries += 1

    wait = WebDriverWait(driver, timeout)
    wait.until(AnyEc(EC.url_changes("")))
    infoLogger.log("Page loaded")

    if "microsoft" in driver.current_url:
        infoLogger.log("Detected login page")
        closeBrowser(driver, dkey)
        doLogin(config)
        driver, dkey = startBrowser()
        driver.get(url)
        wait = WebDriverWait(driver, timeout)

    driver.implicitly_wait(0)
    continueBtn = driver.find_elements(By.ID, "btnContinue")
    driver.implicitly_wait(3)

    if continueBtn:
        infoLogger.log("Detected session continue button")
        continueBtn[0].click()

    infoLogger.log("Extracting cookies...")
    DSID = driver.get_cookie("DSID")["value"]
    infoLogger.log(f"DSID = {DSID}")
    closeBrowser(driver, dkey)

    if not re.match(r"[a-f0-9]{32}", DSID):
        errorLogger.log(f"Invalid DSID cookie format: {DSID}")
        return 1

    infoLogger.log("Starting VPN...")
    proc = subprocess.Popen(
        ["sudo", "openconnect", "--protocol=nc", "-C", f"DSID={DSID}", url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        while True:
            line = proc.stdout.readline().decode("utf-8").strip()
            if not line:
                print("OIHOFIH")
                break
            vpnLogger.log(line)
            if line == "ESP session established with server":
                infoLogger.log("VPN is up and running")
            elif "SSL connected" in line:
                warningLogger.log("Connected through SSL (ESP connection failed)")
                infoLogger.log("VPN is up and running")

    except KeyboardInterrupt:  
        try:
            print()
            infoLogger.log("Stopping VPN...")
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            proc.send_signal(signal.SIGINT)
            proc.wait()
        except KeyboardInterrupt:  
            print()
            infoLogger.log("Stopping VPN...")
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            proc.send_signal(signal.SIGINT)
            proc.wait()
        finally:
            signal.signal(signal.SIGINT, signal.default_int_handler)

    if proc.returncode == 0:
        infoLogger.log("VPN stopped")
        return 0
    else:
        errorLogger.log(f"VPN stopped unexpectedly (code: {proc.returncode})")
        return proc.returncode



def doLogin(config):
    print("+--------------------------+")
    print("| Prompting user for login |")
    print("+--------------------------+")
    from core.browser import startBrowser, closeBrowser
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait

    driver, dkey = startBrowser(False)
    driver.get(config["gateway"])
    wait = WebDriverWait(driver, 9999)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt=Logo],img[alt=logo]")))
    closeBrowser(driver, dkey)
