import random

ship = {
    "hull": 100,
    "fuel": 50,
    "crew": 100,
    "distance": 20,
    "credits": 25,
}

events = [
    "pirates",
    "wreck",
    "storm",
    "trader",
    "nothing"
]

print("""
=================================
        STARBOUND
=================================

Earth is 20 jumps away.

Reach Earth before your ship fails.
""")

while True:

    if ship["distance"] <= 0:
        print("\n🌎 EARTH!")
        print("You made it home.")
        break

    if ship["hull"] <= 0:
        print("\n💥 Your ship breaks apart.")
        break

    if ship["fuel"] <= 0:
        print("\n⛽ You drift endlessly through space.")
        break

    if ship["crew"] <= 0:
        print("\n☠️ Nobody survives.")
        break

    print("\n" + "=" * 40)
    print(
        f"Hull:{ship['hull']} "
        f" Fuel:{ship['fuel']} "
        f" Crew:{ship['crew']} "
        f" Credits:{ship['credits']} "
        f" Earth:{ship['distance']} jumps"
    )

    print("\nChoose:")
    print("1. Jump toward Earth")
    print("2. Search for supplies")
    print("3. Repair ship")
    print("4. Rest crew")

    choice = input("> ")

    # JUMP
    if choice == "1":

        ship["fuel"] -= random.randint(3, 7)
        ship["distance"] -= 1

        print("\n🚀 You make a jump.")

        event = random.choice(events)

        if event == "pirates":
            damage = random.randint(10, 25)

            print("☠️ Space pirates attack!")

            fight = input("Fight or bribe? (f/b) ").lower()

            if fight == "f":
                if random.random() < 0.6:
                    reward = random.randint(15, 40)
                    ship["credits"] += reward
                    print(f"You win and loot {reward} credits.")
                else:
                    ship["hull"] -= damage
                    print(f"You lose. Hull -{damage}")
            else:
                if ship["credits"] >= 15:
                    ship["credits"] -= 15
                    print("Pirates accept the bribe.")
                else:
                    ship["hull"] -= damage
                    print(f"They attack anyway. Hull -{damage}")

        elif event == "wreck":
            reward = random.randint(10, 35)
            ship["credits"] += reward
            ship["fuel"] += 5

            print("🛰️ You discover a wreck.")
            print(f"Credits +{reward}")
            print("Fuel +5")

        elif event == "storm":
            damage = random.randint(5, 20)
            ship["hull"] -= damage

            print("⚡ Cosmic storm!")
            print(f"Hull -{damage}")

        elif event == "trader":

            print("🛒 Alien trader encountered.")

            if ship["credits"] >= 20:
                buy = input("Buy fuel for 20 credits? (y/n) ")

                if buy.lower() == "y":
                    ship["credits"] -= 20
                    ship["fuel"] += 15
                    print("Fuel +15")

        else:
            print("⭐ Quiet journey.")

    # SEARCH
    elif choice == "2":

        print("\n🔍 Searching nearby systems...")

        found = random.randint(1, 100)

        if found <= 50:
            fuel = random.randint(5, 15)
            ship["fuel"] += fuel
            print(f"Found {fuel} fuel.")

        elif found <= 80:
            credits = random.randint(10, 30)
            ship["credits"] += credits
            print(f"Found {credits} credits.")

        else:
            damage = random.randint(5, 15)
            ship["hull"] -= damage
            print("A trap!")
            print(f"Hull -{damage}")

    # REPAIR
    elif choice == "3":

        if ship["credits"] >= 15:
            ship["credits"] -= 15
            ship["hull"] = min(100, ship["hull"] + 20)

            print("\n🔧 Repairs completed.")
        else:
            print("\nNot enough credits.")

    # REST
    elif choice == "4":

        ship["crew"] = min(100, ship["crew"] + 10)
        ship["fuel"] -= 2

        print("\n😴 Crew morale improved.")

    else:
        print("\nInvalid choice.")

print("\n=== GAME OVER ===")