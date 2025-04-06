# SPDX-License-Identifier: MIT
# © 2025 Zoatik


import sys
try:
    from hei_vpn.core import run_vpn
except ModuleNotFoundError:
    # Fallback si exécuté directement (python3 hei_vpn/main.py)
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from hei_vpn.core import run_vpn


def main():
    try:
        exit_code = run_vpn()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected.")
        sys.exit(130)

if __name__ == "__main__":
    main()
