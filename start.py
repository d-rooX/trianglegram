import registration, main
import time

print("  _____          _                           _         ")
time.sleep(0.2)
print(" |_   _|  _ __  (_)   __ _   _ __     __ _  | |   ___  ")
time.sleep(0.2)
print("   | |   | '__| | |  / _` | | '_ \   / _` | | |  / _ \ ")
time.sleep(0.2)
print("   | |   | |    | | | (_| | | | | | | (_| | | | |  __/ ")
time.sleep(0.2)
print("   |_|   |_|    |_|  \__,_| |_| |_|  \__, | |_|  \___| ")
time.sleep(0.2)
print("                                     |___/             ")
time.sleep(0.5)

print("Добро пожаловать в trianglegram v2.5 by Black Triangle (refactored by droox)")
print("Нажми Enter чтобы запустить...")
input()

api_id, api_hash, name, password = registration.start()
time.sleep(0.2)
main.start(api_id, api_hash, name)
time.sleep(0.2)