import MukeshRobot
import random

TOKEN = '7135306288:AAFkD9E8lcuGCDRuGNi_-Ig5lG0r5kK4vBM'
bot = telebot.TeleBot(TOKEN)

# Dictionary to store player information
players = {}

# Character class
class Character:
    def init(self, name, level=1, skills=['magic', 'sword'], magic_power=0):
        self.name = name
        self.level = level
        self.skills = skills
        self.magic_power = magic_power
        self.health = 100

# Monster class
class Monster:
    def init(self, name, health=100):
        self.name = name
        self.health = health

# Inventory class
class Inventory:
    def init(self, tokens=0, potions={'strength': 0, 'health': 0, 'speed': 0}, weapons={}):
        self.tokens = tokens
        self.potions = potions
        self.weapons = weapons

# Character store
character_store = {
    'joohee': Character('Joohee', skills=['magic', 'sword'], magic_power=50),
    # Add more characters here if needed
}

# Weapon store
weapon_store = {
    1: {'name': "KASAMA'S VENOM FANG", 'type': 'DAGGER', 'attack': 25, 'rank': 'C'},
    2: {'name': 'NIGHT KILLER', 'type': 'DAGGER', 'attack': 75, 'rank': 'B'},
    3: {'name': "BATUKA'S DAGGER", 'type': 'DAGGER', 'attack': 110, 'rank': 'A'},
    4: {'name': "DEMON KING'S LONGSWORD", 'type': 'LONGSWORD', 'attack': 350, 'rank': 'S'},
}

# Potion store
potion_store = {
    'strength': {'name': 'Strength Potion', 'price': 500},
    'health': {'name': 'Health Potion', 'price': 600},
    'speed': {'name': 'Speed Potion', 'price': 450},
}

# Exploration function
def explore(player_id):
    monster = Monster('Random Monster')
    bot.send_message(player_id, f"A wild {monster.name} appears!")
    bot.send_message(player_id, "What will you do?")
    bot.send_message(player_id, "/fight - Fight the monster\n/run - Run away")

# Fight function
def fight(player_id):
    player = players[player_id]['character']
    monster = Monster('Random Monster')
    bot.send_message(player_id, f"You and the {monster.name} engage in battle!")
    # Calculate damage based on player level and magic power
    player_damage = (player.level * 10) + player.magic_power
    monster_damage = random.randint(10, 30)
    # Fight loop
    while player.health > 0 and monster.health > 0:
        # Player's turn
        player_choice = random.choice(player.skills)
        if player_choice == 'magic':
            monster.health -= player_damage
        elif player_choice == 'sword':
            monster.health -= player_damage
        # Monster's turn
        player.health -= monster_damage
    # Determine winner
    if player.health <= 0:
        bot.send_message(player_id, "You were defeated!")
    else:
        bot.send_message(player_id, "Congratulations! You defeated the monster!")
        tokens_reward = random.randint(600, 700)
        players[player_id]['inventory'].tokens += tokens_reward
        player.level += 1
        bot.send_message(player_id, f"You earned {tokens_reward} tokens and leveled up! Your new level is {player.level}.")
        # Give mystery box
        mystery_box(player_id)

# Mystery box function
def mystery_box(player_id):
    keys = ['low level cave key', 'medium level cave key', 'hard level cave key']
    random_key = random.choice(keys)
    bot.send_message(player_id, f"You found a mystery box and got a {random_key}!")
    players[player_id]['inventory'].mystery_box_key = random_key

# Inventory command
@bot.message_handler(commands=['inventory'])
def inventory_command(message):
    player_id = message.from_user.id
    if player_id in players and players[player_id]['character']:
        inventory = players[player_id]['inventory']
        reply = f"Tokens: {inventory.tokens}\n"
        reply += "Potions:\n"
        for potion, quantity in inventory.potions.items():
            reply += f"{potion.capitalize()}: {quantity}\n"

reply += "Weapons:\n"
        for weapon_id, weapon_info in inventory.weapons.items():
            reply += f"{weapon_id}: {weapon_info['name']} (Type: {weapon_info['type']}, Attack: +{weapon_info['attack']}, Rank: {weapon_info['rank']})\n"
        bot.send_message(player_id, reply)
    else:
        bot.send_message(player_id, "You must choose a character first! Use /start to begin.")

# Potion store command
@bot.message_handler(commands=['potionStore'])
def potion_store_command(message):
    player_id = message.from_user.id
    if player_id in players and players[player_id]['character']:
        bot.send_message(player_id, "Welcome to the Potion Store!")
        reply = "Available potions:\n"
        for potion, info in potion_store.items():
            reply += f"{info['name']} - Price: {info['price']} tokens\n"
        bot.send_message(player_id, reply)
    else:
        bot.send_message(player_id, "You must choose a character first! Use /start to begin.")

# Weapon store command
@bot.message_handler(commands=['weaponStore'])
def weapon_store_command(message):
    player_id = message.from_user.id
    if player_id in players and players[player_id]['character']:
        bot.send_message(player_id, "Welcome to the Weapon Store!")
        reply = "Available weapons:\n"
        for weapon_id, info in weapon_store.items():
            reply += f"{weapon_id}: {info['name']} (
