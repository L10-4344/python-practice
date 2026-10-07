import random


def get_choice(valid_choices, prompt='> '):
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print('Invalid choice. Try again.')


def pause():
    input('\nPress ENTER to continue.')


def restore_hull(amount):
    old_hull = ship['hull']
    ship['hull'] = min(ship['max_hull'], ship['hull'] + amount)
    return ship['hull'] - old_hull


def restore_crew(amount):
    old_crew = ship['crew']
    ship['crew'] = min(ship['max_crew'], ship['crew'] + amount)
    return ship['crew'] - old_crew


def apply_hull_damage(amount, source='Damage'):
    damage = max(1, int(amount))
    if ship['class'] == 'Cruiser':
        damage = max(1, damage - 1)
    ship['hull'] = max(0, ship['hull'] - damage)
    print(f'{source}: Hull -{damage}')


def apply_crew_damage(minimum, maximum, source='Crew injured'):
    loss = min(random.randint(minimum, maximum), ship['crew'])
    ship['crew'] -= loss
    print(f'{source}: Crew -{loss}')


def show_status():
    print('\n' + '=' * 52)
    print(f"Class       : {ship['class']}")
    print(f'Difficulty  : {difficulty_name}')
    print(f"Hull        : {ship['hull']}/{ship['max_hull']}")
    print(f"Fuel        : {ship['fuel']}")
    print(f"Crew        : {ship['crew']}/{ship['max_crew']}")
    print(f"Credits     : {ship['credits']}")
    print(f"Reputation  : {ship['reputation']}")
    print(f"Distance    : {ship['distance']} jumps")
    print(f'Turns       : {turns}')
    print('=' * 52)


def show_ship_information():
    print('\n============== SHIP INFORMATION ==============')
    if ship['class'] == 'Scout':
        print('''
Scout abilities:
- 12% chance for a jump to use no fuel
- 25% bonus retreat chance
- Highest starting fuel
''')
    elif ship['class'] == 'Cruiser':
        print('''
Cruiser abilities:
- Highest maximum hull
- Repairs restore 30 hull instead of 20
- Incoming hull damage is reduced by 1
''')
    else:
        print('''
Gunship abilities:
- Laser attacks deal 3 additional damage
- Focused shots deal 4 additional damage
- Pirate victories award 10 extra credits
- Better chance to salvage pirate fuel
''')
    print('================================================')


def calculate_score():
    score = (
        max(0, ship['hull'])
        + max(0, ship['fuel'])
        + max(0, ship['crew'])
        + max(0, ship['credits'])
        + ship['reputation'] * 20
        - turns * 2
    )
    if difficulty_name == 'Easy':
        score = int(score * 0.75)
    elif difficulty_name == 'Hard':
        score = int(score * 1.50)
    return max(0, score)


def alien_trader():
    print('''
================ ALIEN TRADER ================
An alien merchant signals your ship.
You may make multiple purchases.
==============================================
''')
    while True:
        print(f"\nCredits: {ship['credits']}")
        print(f"Fuel: {ship['fuel']}")
        print(f"Hull: {ship['hull']}/{ship['max_hull']}")
        print(f"Crew: {ship['crew']}/{ship['max_crew']}")
        print('''
1. Buy 15 fuel for 20 credits
2. Repair 25 hull for 18 credits
3. Restore 15 crew for 15 credits
4. Leave trader
''')
        choice = get_choice(['1', '2', '3', '4'])

        if choice == '1':
            if ship['credits'] < 20:
                print('\nNot enough credits.')
            else:
                ship['credits'] -= 20
                ship['fuel'] += 15
                print('\nFuel +15')
                print('Credits -20')
        elif choice == '2':
            if ship['hull'] >= ship['max_hull']:
                print('\nYour hull is already at maximum.')
            elif ship['credits'] < 18:
                print('\nNot enough credits.')
            else:
                ship['credits'] -= 18
                repaired = restore_hull(25)
                print(f'\nHull +{repaired}')
                print('Credits -18')
        elif choice == '3':
            if ship['crew'] >= ship['max_crew']:
                print('\nYour crew is already fully recovered.')
            elif ship['credits'] < 15:
                print('\nNot enough credits.')
            else:
                ship['credits'] -= 15
                recovered = restore_crew(15)
                print(f'\nCrew +{recovered}')
                print('Credits -15')
        else:
            print('\nYou leave the alien trader.')
            return


def choose_pirate():
    progress = 1 - ship['distance'] / starting_distance
    raider = {
        'name': 'Raider', 'hull': 25, 'damage': 9,
        'minimum_reward': 14, 'maximum_reward': 28
    }
    marauder = {
        'name': 'Marauder', 'hull': 38, 'damage': 13,
        'minimum_reward': 22, 'maximum_reward': 38
    }
    dreadnought = {
        'name': 'Dreadnought', 'hull': 58, 'damage': 18,
        'minimum_reward': 35, 'maximum_reward': 55
    }

    if progress < 0.33:
        pool = [raider, raider, raider, marauder]
    elif progress < 0.70:
        pool = [raider, marauder, marauder, dreadnought]
    else:
        pool = [marauder, marauder, dreadnought, dreadnought]
    return random.choice(pool)


def pirate_battle():
    enemy = choose_pirate()
    maximum = max(1, int(enemy['hull'] * settings['pirate_hull']))
    enemy_hull = maximum
    enemy_damage = max(1, int(enemy['damage'] * settings['pirate_damage']))
    print(f"\nPirate {enemy['name']} attacks!")

    intimidation = 0.0
    if ship['reputation'] >= 8:
        intimidation = 0.35
    elif ship['reputation'] >= 5:
        intimidation = 0.20
    if enemy['name'] == 'Dreadnought':
        intimidation *= 0.5
    if random.random() < intimidation:
        print('The pirates recognize your reputation and flee!')
        return

    while enemy_hull > 0 and ship['hull'] > 0 and ship['crew'] > 0:
        print('\n-----------------------------')
        print(f"Your Hull       : {ship['hull']}/{ship['max_hull']}")
        print(f"Your Crew       : {ship['crew']}/{ship['max_crew']}")
        print(f"{enemy['name']} Hull: {enemy_hull}/{maximum}")
        print('-----------------------------')
        print('''
1. Fire Lasers
2. Focused Shot
3. Brace
4. Retreat
''')
        choice = get_choice(['1', '2', '3', '4'])
        bracing = False

        if choice == '1':
            damage = random.randint(8, 15)
            if ship['class'] == 'Gunship':
                damage += 3
            enemy_hull -= damage
            print(f'\nYou deal {damage} damage!')
        elif choice == '2':
            hit_chance = 0.70 if ship['class'] == 'Gunship' else 0.65
            if random.random() < hit_chance:
                damage = random.randint(14, 23)
                if ship['class'] == 'Gunship':
                    damage += 4
                enemy_hull -= damage
                print(f'\nFocused shot hits for {damage} damage!')
            else:
                print('\nFocused shot missed!')
        elif choice == '3':
            bracing = True
            print('\nYou brace for impact!')
        else:
            chance = 0.42 + settings['retreat_bonus']
            if ship['class'] == 'Scout':
                chance += 0.25
            chance = max(0.10, min(0.90, chance))
            if random.random() < chance:
                print('\nEscape successful!')
                return
            print('\nEscape failed!')

        if enemy_hull <= 0:
            reward = random.randint(
                enemy['minimum_reward'], enemy['maximum_reward']
            )
            reward = int(reward * settings['reward'])
            if ship['class'] == 'Gunship':
                reward += 10
            ship['credits'] += reward
            ship['reputation'] += 1
            print('\nPirate defeated!')
            print(f'Credits +{reward}')
            print('Reputation +1')

            salvage_chance = 0.35 if ship['class'] == 'Gunship' else 0.20
            if random.random() < salvage_chance:
                fuel = random.randint(2, 6)
                ship['fuel'] += fuel
                print(f'Salvaged fuel +{fuel}')
            return

        incoming = max(1, enemy_damage + random.randint(-2, 2))
        if bracing:
            incoming = max(1, incoming // 2)
        apply_hull_damage(incoming, 'Pirate attack')
        if ship['hull'] <= 0:
            return

        injury_chance = 0.04 if bracing else 0.16
        if random.random() < injury_chance:
            apply_crew_damage(2, 6, 'Crew injured')


def jump_event():
    roll = random.randint(1, 100)
    if difficulty_name == 'Easy':
        limits = (18, 45, 60, 80)
    elif difficulty_name == 'Hard':
        limits = (28, 45, 68, 84)
    else:
        limits = (23, 45, 64, 82)

    if roll <= limits[0]:
        pirate_battle()
    elif roll <= limits[1]:
        credits = random.randint(10, 35)
        fuel = random.randint(3, 10)
        ship['credits'] += credits
        ship['fuel'] += fuel
        print('\nAbandoned wreck discovered!')
        print(f'Credits +{credits}')
        print(f'Fuel +{fuel}')
    elif roll <= limits[2]:
        damage = int(random.randint(6, 18) * settings['danger'])
        print('\nCosmic storm!')
        apply_hull_damage(damage, 'Storm damage')
        if ship['hull'] > 0 and random.random() < 0.25:
            apply_crew_damage(2, 7, 'Crew injured in the storm')
    elif roll <= limits[3]:
        alien_trader()
    else:
        quiet = random.randint(1, 3)
        if quiet == 1:
            fuel = random.randint(1, 4)
            ship['fuel'] += fuel
            print(f'\nSolar collectors gather {fuel} fuel.')
        elif quiet == 2:
            recovered = restore_crew(3)
            print('\nThe crew enjoys a calm journey.')
            if recovered > 0:
                print(f'Crew +{recovered}')
        else:
            print('\nQuiet journey through the stars.')


def search_system():
    ship['fuel'] -= 1
    print('\nSearching nearby systems...')
    print('Fuel -1')
    roll = random.randint(1, 100)

    if difficulty_name == 'Easy':
        limits = (35, 62, 72, 82)
    elif difficulty_name == 'Hard':
        limits = (28, 50, 60, 72)
    else:
        limits = (32, 56, 66, 78)

    if roll <= limits[0]:
        fuel = random.randint(5, 14)
        ship['fuel'] += fuel
        print(f'Found {fuel} fuel.')
    elif roll <= limits[1]:
        credits = random.randint(10, 28)
        ship['credits'] += credits
        print(f'Found {credits} credits.')
    elif roll <= limits[2]:
        recovered = restore_crew(random.randint(5, 12))
        if recovered > 0:
            print(f'Rescued survivors. Crew +{recovered}')
        else:
            reward = random.randint(8, 18)
            ship['credits'] += reward
            print(f'Your crew is full. The survivors give you {reward} credits.')
    elif roll <= limits[3]:
        print('A hidden pirate patrol finds you!')
        pirate_battle()
    else:
        damage = int(random.randint(6, 15) * settings['danger'])
        print('It is a trap!')
        apply_hull_damage(damage, 'Trap damage')
        if ship['hull'] > 0 and random.random() < 0.20:
            apply_crew_damage(2, 5, 'Crew injured in the trap')


print('''
=========================================
              STARBOUND
=========================================

You are the captain of a starship stranded
deep in unexplored space. Earth is your only
way home.

Manage hull, fuel, crew, credits, and
reputation. Survive pirates, storms, traders,
and dangerous discoveries.

View detailed rules? (y/n)
''')

if get_choice(['y', 'n']) == 'y':
    print('''
================ DETAILED RULES ================
GOAL
Reduce Distance to 0 jumps to reach Earth.

LOSE CONDITIONS
- Hull reaches 0
- Fuel reaches 0 before reaching Earth
- Crew reaches 0

ACTIONS
Jump moves toward Earth and triggers an event.
Search costs 1 fuel and may find resources.
Repair costs 15 credits.
Rest costs 2 fuel and restores crew.

COMBAT
Fire Lasers is reliable.
Focused Shot is stronger but may miss.
Brace halves the next incoming attack.
Retreat attempts to escape.

Reaching Earth with exactly 0 fuel is a win.
================================================
''')
    pause()

print('''
================ CHOOSE YOUR SHIP ================
1. Scout   - Hull 80, Fuel 70, Credits 20
2. Cruiser - Hull 140, Fuel 50, Credits 25
3. Gunship - Hull 110, Fuel 50, Credits 30
==================================================
''')

choice = get_choice(['1', '2', '3'])
if choice == '1':
    ship = {
        'class': 'Scout', 'hull': 80, 'max_hull': 80,
        'fuel': 70, 'crew': 100, 'max_crew': 100,
        'credits': 20, 'distance': 20, 'reputation': 0
    }
elif choice == '2':
    ship = {
        'class': 'Cruiser', 'hull': 140, 'max_hull': 140,
        'fuel': 50, 'crew': 100, 'max_crew': 100,
        'credits': 25, 'distance': 20, 'reputation': 0
    }
else:
    ship = {
        'class': 'Gunship', 'hull': 110, 'max_hull': 110,
        'fuel': 50, 'crew': 100, 'max_crew': 100,
        'credits': 30, 'distance': 20, 'reputation': 0
    }

print('''
================ CHOOSE DIFFICULTY ================
1. Easy
2. Normal
3. Hard
===================================================
''')

choice = get_choice(['1', '2', '3'])
if choice == '1':
    difficulty_name = 'Easy'
    settings = {
        'danger': 0.75, 'pirate_hull': 0.85,
        'pirate_damage': 0.80, 'reward': 1.10,
        'retreat_bonus': 0.10
    }
    ship['fuel'] += 15
    ship['credits'] += 15
elif choice == '3':
    difficulty_name = 'Hard'
    settings = {
        'danger': 1.35, 'pirate_hull': 1.25,
        'pirate_damage': 1.30, 'reward': 1.00,
        'retreat_bonus': -0.10
    }
    ship['fuel'] = max(20, ship['fuel'] - 8)
    ship['credits'] = max(10, ship['credits'] - 8)
    ship['distance'] += 5
else:
    difficulty_name = 'Normal'
    settings = {
        'danger': 1.00, 'pirate_hull': 1.00,
        'pirate_damage': 1.00, 'reward': 1.00,
        'retreat_bonus': 0.00
    }

starting_distance = ship['distance']
turns = 0
victory = False
end_reason = ''

while True:
    if ship['distance'] <= 0:
        victory = True
        end_reason = 'Earth reached'
        break
    if ship['hull'] <= 0:
        end_reason = 'Your ship was destroyed'
        break
    if ship['fuel'] <= 0:
        end_reason = 'Your ship ran out of fuel'
        break
    if ship['crew'] <= 0:
        end_reason = 'Your crew was lost'
        break

    show_status()
    print('''
Choose an action
1. Jump
2. Search
3. Repair
4. Rest
5. Ship Information
6. Rules Summary
''')
    action = get_choice(['1', '2', '3', '4', '5', '6'])

    if action == '1':
        jump_cost = random.randint(3, 7)
        if ship['class'] == 'Scout' and random.random() < 0.12:
            jump_cost = 0
            print('\nEfficient route found!')

        if jump_cost >= ship['fuel'] and ship['distance'] > 1:
            print(f'\nThis jump requires {jump_cost} fuel.')
            print(f"You currently have {ship['fuel']} fuel.")
            print('Search for fuel before jumping.')
            continue

        ship['fuel'] -= jump_cost
        ship['distance'] -= 1
        turns += 1
        print(f'\nFuel used: {jump_cost}')
        print(f"Distance remaining: {max(0, ship['distance'])} jumps")
        if ship['distance'] > 0:
            jump_event()

    elif action == '2':
        if ship['fuel'] <= 1:
            print('\nYou need more than 1 fuel to search safely.')
            continue
        turns += 1
        search_system()

    elif action == '3':
        if ship['hull'] >= ship['max_hull']:
            print('\nYour hull is already at maximum.')
            continue
        if ship['credits'] < 15:
            print('\nNot enough credits. Repairs cost 15 credits.')
            continue
        ship['credits'] -= 15
        amount = 30 if ship['class'] == 'Cruiser' else 20
        repaired = restore_hull(amount)
        turns += 1
        print('\nRepairs complete.')
        print(f'Hull +{repaired}')
        print('Credits -15')

    elif action == '4':
        if ship['crew'] >= ship['max_crew']:
            print('\nYour crew is already fully recovered.')
            continue
        if ship['fuel'] <= 2:
            print('\nYou need more than 2 fuel to rest safely.')
            continue
        ship['fuel'] -= 2
        recovered = restore_crew(12)
        turns += 1
        print('\nThe crew rests and recovers.')
        print(f'Crew +{recovered}')
        print('Fuel -2')

    elif action == '5':
        show_ship_information()

    else:
        print('''
================ RULES SUMMARY ================
- Reduce Distance to 0 to reach Earth.
- Do not let Hull, Fuel, or Crew reach 0.
- Jumping advances the journey.
- Searching costs 1 fuel.
- Repairs cost 15 credits.
- Resting costs 2 fuel.
- Reaching Earth with exactly 0 fuel is a win.
================================================
''')

if victory:
    print('''
=================================
          EARTH REACHED
=================================
''')
    print("Your battered starship enters Earth's orbit.")
    print('The crew cheers. You made it home!')
    print(f'\nFinal Score: {calculate_score()}')
else:
    print('''
=================================
            DEFEAT
=================================
''')
    print(end_reason + '.')

print('\n========== GAME OVER ==========')
print(f"Ship Class : {ship['class']}")
print(f'Difficulty : {difficulty_name}')
print(f'Turns      : {turns}')
print(f"Hull       : {max(0, ship['hull'])}")
print(f"Fuel       : {max(0, ship['fuel'])}")
print(f"Crew       : {max(0, ship['crew'])}")
print(f"Credits    : {max(0, ship['credits'])}")
print(f"Reputation : {ship['reputation']}")
print(f"Distance   : {max(0, ship['distance'])} jumps")
print('================================')
