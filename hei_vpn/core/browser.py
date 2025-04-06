import os
import random
import shutil
import subprocess
import sys
import psutil
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxProfile, FirefoxService
from .logger import infoLogger, warningLogger, errorLogger
from .utils import get_driver_path

ROOT = "/"
APP_PATH = os.path.abspath(os.path.expanduser("~/.config/hei-vpn"))
PERSISTENT_PROFILE_PATH = os.path.join(APP_PATH, "firefox_profile/")
DRIVER_PATH = get_driver_path()

def startBrowser(headless=True):

    cleanTempFiles()

    infoLogger.log("Loading browser...")

    profilePath = PERSISTENT_PROFILE_PATH
    if not os.path.isdir(profilePath):
        dataDir = os.path.expanduser("~/.mozilla/firefox/")
        dirs = os.listdir(dataDir)

        for d in dirs:
            if ".default" in d:
                profilePath = os.path.join(dataDir, d)
                if d.endswith(".default-release"):
                    break
        else:
            if profilePath == PERSISTENT_PROFILE_PATH:
                warningLogger.log("Default Firefox profile not found. Please create one manually")
                exit()

    infoLogger.log(f"Using Firefox profile in {profilePath}")

    options = FirefoxOptions()
    profile = FirefoxProfile(profilePath)
    profile.set_preference("extensions.enabledScopes", 0)
    profile.set_preference("extensions.autoDisableScopes", 0)
    options.profile = profile
    distinguishkey = "-distinguishkey" + str(random.randint(111111, 999999))
    options.add_argument(distinguishkey)

    if headless:
        options.add_argument("--headless")

    service = FirefoxService(executable_path=DRIVER_PATH, log_output="/dev/null")
    driver = Firefox(options=options, service=service)

    return driver, distinguishkey

def closeBrowser(driver: Firefox, distinguishkey: str):
    infoLogger.log("Closing browser...")

    for pid in psutil.pids():
        try:
            cmdline = open(f"/proc/{pid}/cmdline", "r").read()
            if distinguishkey in cmdline:
                realProfilePath = cmdline.split('-profile')[1].split(' ')[0].replace('\x00', '')
                realProfilePath = os.path.abspath(os.path.join(ROOT, "./" + realProfilePath))
                break
        except:
            pass
    else:
        errorLogger.log("Cannot find Firefox PID")
        exit()

    infoLogger.log(f"Profile is stored in {realProfilePath}")

    psutil.Process(pid).kill()

    if os.path.isdir(PERSISTENT_PROFILE_PATH):
        shutil.rmtree(PERSISTENT_PROFILE_PATH)

    r = subprocess.run(["sudo", "cp", "-r", realProfilePath, PERSISTENT_PROFILE_PATH])

    if r.returncode:
        errorLogger.log("Could not copy temporary profile to persistent directory")
        errorLogger.log(f"Tried: sudo cp -r {realProfilePath} {PERSISTENT_PROFILE_PATH}")
        exit()

    lockPath = os.path.join(PERSISTENT_PROFILE_PATH, "lock")
    if os.path.isfile(lockPath):
        subprocess.run(["sudo", "rm", lockPath])

    subprocess.run(["sudo", "chown", "-R", f"{os.getuid()}:{os.getgid()}", PERSISTENT_PROFILE_PATH])
    subprocess.run(["sudo", "chmod", "-R", "0644", PERSISTENT_PROFILE_PATH])
    subprocess.run(["sudo", "chmod", "-R", "+X", PERSISTENT_PROFILE_PATH])

    try:
        driver.quit()
    except:
        pass

    if os.path.isdir(realProfilePath):
        if realProfilePath.startswith("/tmp/") \
        and realProfilePath.startswith(os.path.abspath(os.path.join(ROOT, "tmp"))) \
        and len(realProfilePath.split(os.path.sep)) >= 2 \
        and ".." not in realProfilePath:
            subprocess.run(["sudo", "rm", "-r", realProfilePath])

    cleanTempFiles()


def cleanTempFiles():
    infoLogger.log("Cleaning files...")
    # Extra cleanup if still not done
    root_tmp_folder = getattr(sys, 'MEIPASS', "/tmp/")
    for tmp_folder in os.listdir(root_tmp_folder):
        abs_tmp_folder = None
        # Look for tmp files from webDriver
        if "tmp" in tmp_folder:
            abs_tmp_folder = root_tmp_folder + tmp_folder
            if not "webdriver-py-profilecopy" in os.listdir(abs_tmp_folder):
                abs_tmp_folder = None
                

        # Look for tmp files from mozilla profiles            
        if "rust_mozprofile" in tmp_folder:
            abs_tmp_folder = root_tmp_folder + tmp_folder
        
        if abs_tmp_folder is not None:
            try:
                shutil.rmtree(abs_tmp_folder)
                infoLogger.log(f"Temporary file {tmp_folder} successfully removed from {root_tmp_folder}")

            except:
                errorLogger.log(f"Error while removing temporary file {tmp_folder} from {root_tmp_folder}")
