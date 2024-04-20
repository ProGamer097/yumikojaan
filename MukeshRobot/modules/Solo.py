import random
from telegram.ext import Updater, CommandHandler
import MukeshRobot
TOKEN = '7135306288:AAGWeXVNNHiRnwVDtnrfytXyFWOqe3rxSKM'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Your other code here...

# Dictionary to store player information
players = {}

# Character class
class Character:
    def __init__(self, name, level=1, skills=['magic', 'sword'], magic_power=0):
        self.name = name
        self.level = level
        self.skills = skills
        self.magic_power = magic_power
        self.health = 100

# Monster class
class Monster:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health

# Inventory class
class Inventory:
    def __init__(self, tokens=0, potions={'strength': 0, 'health': 0, 'speed': 0}, weapons={}):
        self.tokens = tokens
        self.potions = potions
        self.weapons = weapons

# Exploration function
def explore(update, context):
    player_id = update.message.from_user.id
    monster = Monster('Random Monster')
    context.bot.send_message(player_id, f"A wild {monster.name} appears!")
    context.bot.send_message(player_id, "What will you do?")
    context.bot.send_message(player_id, "/fight - Fight the monster\n/run - Run away")

# Fight function
def fight(update, context):
    player_id = update.message.from_user.id
    player = players[player_id]['character']
    monster = Monster('Random Monster')
    context.bot.send_message(player_id, f"You and the {monster.name} engage in battle!")
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
        context.bot.send_message(player_id, "You were defeated!")
    else:
        context.bot.send_message(player_id, "Congratulations! You defeated the monster!")
        tokens_reward = random.randint(600, 700)
        players[player_id]['inventory'].tokens += tokens_reward
        player.level += 1
        context.bot.send_message(player_id, f"You earned {tokens_reward} tokens and leveled up! Your new level is {player.level}.")
        # Give mystery box
        mystery_box(player_id, context)

# Mystery box function
def mystery_box(player_id, context):
    keys = ['low level cave key', 'medium level cave key', 'hard level cave key']
    random_key = random.choice(keys)
    context.bot.send_message(player_id, f"You found a mystery box and got a {random_key}!")
    players[player_id]['inventory'].mystery_box_key = random_key

# Inventory command
def inventory_command(update, context):
    player_id = update.message.from_user.id
    if player_id in players and players[player_id]['character']:
        inventory = players[player_id]['inventory']
        reply = f"Tokens: {inventory.tokens}\n"
        reply += "Potions:\n"
        for potion, quantity in inventory.potions.items():
            reply += f"{potion.capitalize()}: {quantity}\n"
        reply += "Weapons:\n"  # Correct indentation here
        for weapon_id, weapon_info in inventory.weapons.items():
            reply += f"{weapon_id}: {weapon_info['name']} (Type: {weapon_info['type']}, Attack: +{weapon_info['attack']}, Rank: {weapon_info['rank']})\n"
        context.bot.send_message(player_id, reply)
    else:
        context.bot.send_message(player_id, "You must choose a character first! Use /start to begin.")

# Register command handlers
dispatcher.add_handler(CommandHandler('explore', explore))
dispatcher.add_handler(CommandHandler('fight', fight))
dispatcher.add_handler(CommandHandler('inventory', inventory_command))

# Start the bot
try:
    updater.start_polling()
    updater.idle()
except Conflict:
    print("Another instance of the bot is already running.")
        
