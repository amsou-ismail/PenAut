import os,sys
from cve_scan import main_scancve
from cve_search import main_cve
from hashcracker import NoSaltedHashCracker,main_hashcracker
from network_scanner import Network_scanner,main_net
from passpwnd import CheckPasswordPwned,main_passpwnd
from port_scanner import main_port
from shodan_scan import main_shodan
from url_enum import WordlistLoader,DomainScanner,main_url_enum
from tool_style import banner,clear



#Vérification des droits root
if os.geteuid() != 0:
    print("❌ Ce script doit être exécuté en root (utilisez sudo).")
    sys.exit(1)

while True:
    clear()
    print("\n\n------> TAP 0 TO QUIT <------\n\n")
    print(" 1 - Network Scanner               :")
    print(" 2 - port scanner                  :")
    print(" 3 - Shodan Scan                   :")
    print(" 4 - Url Enumeration               :")
    print(" 5 - CVE Search                    :")
    print(" 6 - CVE Scan                      :")
    print(" 7 - Hash Cracker                  :")
    print(" 8 - Password Pwned                ?")
    
    try:
        choice = int(input("------------------------------------>  ").strip())
    except ValueError:
        continue  # Si entrée invalide, recommencer

    if choice == 0:
        break  # Quitter le programme

    if choice not in range(1, 9):
        continue  # Si entrée pas valide, recommencer

    var = 1
    while var != 0:
        if choice == 1:
            main_net()
        elif choice == 2:
            main_port()
        elif choice == 3:
            main_shodan()
        elif choice == 4:
            main_url_enum()
        elif choice == 5:
            main_cve()
        elif choice == 6:
            main_scancve()
        elif choice == 7:
            main_hashcracker()
        elif choice == 8:
            main_passpwnd()

        try:
            var = int(input("------> TAP 0 TO QUIT <------").strip())
        except ValueError:
            var = 1  # Revenir au menu du module

        clear()
