import random
import json
import time
# Anthony Montes
# Jose Zavala
# ETE 4990 Python Project #1

# My rant/notes: I wanted to make it so that the character wanders throughout the game, but at that point, I would be making -->
# a whole story, so the only game for this project is fighting against a slime, which is based on the game dragon quest. I want to
# add more players to the party and I can, but I don't want the person to have to control all of them and press attack 4 times for a single turn,
# plus, 1 party member is enough for this project, as the slime is too weak. And it's somewhat easy to do it, I just made this project
# in its simplest form for you to get the idea

# I also want to add more items to the game, but I don't want to make the game too complicated.
# I also have it so the user gets their items back every time you load the game because if I didn't do that,
# I would have to create a whole story so they can wander around and get items, but that will go over the 400 lines of code limit 


class Item:
    def __init__(self, name, category, upStats):
        self.name = name
        self.category = category
        self.upStats = upStats


class Weapon(Item):
    def __init__(self, name, attack_bonus):
        super().__init__(name, category="weapon", upStats=f"Attack Bonus: {attack_bonus}")
        self.attack_bonus = attack_bonus

class Consumable(Item):
    def __init__(self, name, heal_amount):
        super().__init__(name, category="consumable", upStats=f"Heals {heal_amount} HP")
        self.heal_amount = heal_amount

class Player:
    def __init__(self, name, health, attack, defense, weapon, level=1, experience=0):
        self.name = name
        self.level = level
        self.experience = experience
        self.health = health
        self.max_health = 30
        self.attack = attack
        self.defense = defense
        self.weapon = weapon
        self.inventory = self.load_inventory()
        self.items = self.load_items()
# Warrior! strong attacks!
class Warrior(Player):
    def __init__(self, name):
        super().__init__(name, health=30, attack=15, defense=10, weapon="Sword")

# Mage, can heal at lvl 5 and shoot magic
class Mage(Player):
    def __init__(self, name):
        super().__init__(name, health=30, attack=20, defense=5, weapon="Wand")
# Priest (healer)

class Priest(Player):
    def __init__(self, name):
        super().__init__(name, health=30, attack=8, defense=7, weapon="Staff")

# Thief, who can steal from the enemy and has good attacks

class Thief(Player):
    def __init__(self, name):
        super().__init__(name, health=30, attack=12, defense=8, weapon="Daggers")

# Slime, the enemy
# The slime is the enemy that the player will fight against 
class Slime(Player):
    def __init__(self):
        super().__init__("Slime", health=60, attack=10, defense=2, weapon="Slime Body")

    def load_items(self):
        # Load items from the healing_items.json file
        try:
            with open("healing_items.json", "r") as file:
                items_data = json.load(file)
                items = {}
                for item_name, item_info in items_data.items():
                    items[item_name] = Item(item_info['name'], item_info['category'], item_info['upStats'])
                return items
        except FileNotFoundError:
            print("Healing items file not found!")
            return {}
    # Load the inventory file
    def load_inventory(self):
        try:
            with open("inventory.json", "r") as file:
                inventory_data = json.load(file)
                # Convert all items to Item objects
                inventory = {}
                for category, items in inventory_data.items():
                    inventory[category] = {}
                    for item_name, item_info in items.items():
                        # Create Item object and store it in the inventory
                        inventory[category][item_name] = Item(item_info['name'], item_info['category'], item_info['upStats'])
                return inventory
        except FileNotFoundError:
            return {
                "swords": {}, "armor": {}, "food": {}, "potions": {}, "daggers": {}, "wands": {}, "staffs": {}
            }
    # Saves inventory for the next game whenever you restart the game
    def save_inventory(self):
        with open("inventory.json", "w") as file:
            json.dump(self.inventory, file, indent=4)
# Saves all the information of the player, including the name you chose for your hero, the level you were at, experience, list goes on
    def save_player(self):
        player_data = {
            "name": self.name,
            "level": self.level,
            "experience": self.experience,
            "health": self.health,
            "max_health": self.max_health,
            "attack": self.attack,
            "defense": self.defense,
            "weapon": self.weapon,
        }
        with open("player_data.json", "w") as file:
            json.dump(player_data, file, indent=4)
        print(f"{self.name}'s data saved!")

# loads the player data from the file that it wrote to: player_data.json
    @classmethod
    def load_player(cls):
        try:
            with open("player_data.json", "r") as file:
                player_data = json.load(file)
                player = cls(
                    player_data["name"],
                    player_data["health"],
                    player_data["attack"],
                    player_data["defense"],
                    player_data["weapon"]
                )
                player.level = player_data["level"]
                player.experience = player_data["experience"]
                player.max_health = player_data["max_health"]
                return player
            # incase there is no file found, it will print out that there is no saved player data found
        except FileNotFoundError:
            print("No saved player data found!")
            return None
        # When the user wants to restart the game (yes/no)
    def reset_player(self):
        # Reset the player's stats and inventory to initial state
        self.name = "New Hero"
        self.level = 1
        self.experience = 0
        self.health = 30
        self.max_health = 30
        self.attack = 10
        self.defense = 5
        self.weapon = "Sword"
        self.inventory = {
            "swords": {}, "food": {}, "daggers": {}, "wands": {}, "staffs": {}, "potions": {}
        }
        # Save the reset player data to the file
        self.save_player()
    
    # allows hero to equip items
    def equip_item(self, item_name):
    # Equip weapons, armor, daggers, wands, and staffs based on class
        for category in ["swords", "daggers", "wands", "staffs", "armor"]:
            for stored_item_name, item in self.inventory[category].items():
                if item_name.lower() == stored_item_name.lower():  # Case-insensitive comparison
                    if item.category == "sword":
                        self.weapon = item_name
                        self.attack += 5  # Example: increase attack
                        print(f"{self.name} equips {item_name} and gains {item.upStats}!")
                    elif item.category == "dagger" and isinstance(self, Thief):
                        self.weapon = item_name
                        self.attack += 3  # Example: increase attack for Thief class
                        print(f"{self.name} equips {item_name} and gains {item.upStats}!")
                    elif item.category == "wand" and isinstance(self, Mage):
                        self.weapon = item_name
                        self.attack += 7  # Example: increase attack for Mage class
                        print(f"{self.name} equips {item_name} and gains {item.upStats}!")
                    elif item.category == "staff" and isinstance(self, Priest):
                        self.weapon = item_name
                        self.defense += 5  # Example: increase defense for Priest class
                        print(f"{self.name} equips {item_name} and gains {item.upStats}!")
                    elif item.category == "armor":
                        self.defense += 6  # Armor boosts defense
                        print(f"{self.name} equips {item_name} and gains {item.upStats}!")
                    del self.inventory[category][stored_item_name]  # Remove the item from inventory after equipping
                    return True
        print(f"{item_name} is not in your inventory or cannot be equipped by your class.")
        return False


    # shows the inventory when the user prompts it, does not take a turn
    def show_inventory(self):
        print("Inventory:")
        for category, items in self.inventory.items():
            print(f"{category.capitalize()}: {', '.join(items.keys()) if items else 'None'}")
        input("Press Enter to go back.")
    
    def use_item(self, item_name):
    # Use consumables (food, potions, etc.)
        for category in ["food", "potions"]:  # Check both food and potions categories
            # Iterate over items in the category and compare the name case-insensitively
            for stored_item_name, item in self.inventory[category].items():
                if item_name.lower() == stored_item_name.lower():  # Case-insensitive comparison
                    if item.category == "food":
                        # Example: Restores 10 HP for food
                        self.health = min(self.max_health, self.health + 10)
                        print(f"{self.name} uses {item_name} and restores health! Current health: {self.health}.")
                    elif item.category == "potion":
                        # Example: Restores 30 HP for potions
                        self.health = min(self.max_health, self.health + 30)
                        print(f"{self.name} uses {item_name} and restores health! Current health: {self.health}.")
                    # After using the item, remove it from the inventory
                    del self.inventory[category][stored_item_name]
                    return True
        print(f"Item {item_name} is not found or cannot be used.")
        return False

    # Take-damage function that allows the player and enemy to take damage
    def take_damage(self, damage):
        damage_taken = max(0, damage - self.defense)
        self.health -= damage_taken
        print(f"{self.name} takes {damage_taken} damage! Remaining health: {self.health}")
        if self.health <= 0:
            print(f"{self.name} has been defeated!")

    # allows hero to gain experience and level up
    def gain_experience(self, amount):
        if self.level == 99:
            print(f"{self.name} gains {amount} EXP but remains at level 99.")
            return
        self.experience += amount
        print(f"{self.name} gains {amount} EXP! Current EXP: {self.experience}")
        self.check_level_up()

    # Checks for level up and levels up hero if experience was reached
    def check_level_up(self):
        required_exp = self.level * 50
        while self.experience >= required_exp and self.level < 99:
            self.experience -= required_exp
            self.level += 1
            self.max_health = int(30 + (self.level - 1) * (550 / 98))
            self.health = self.max_health
            print(f"{self.name} leveled up to Level {self.level}! Max Health is now {self.max_health}.")
            required_exp = self.level * 50

    # Allows enemy to attack the player with a random weak attack damage
    def attack_enemy(self, enemy):
        damage = self.attack + random.randint(1, 5)
        print(f"{self.name} attacks {enemy.name} with {self.weapon} for {damage} damage! {enemy.name} has {enemy.health - damage} HP left.")
        enemy.take_damage(damage)
    
    # Allows hero to heal an ally (only works for priest and mage)
    def heal(self, ally):
        if self.level >= 5:
            heal_amount = 5
            ally.health = min(ally.max_health, ally.health + heal_amount)
            print(f"{self.name} heals {ally.name} for {heal_amount} health! {ally.name} now has {ally.health} HP.")
        else:
            print(f"{self.name} has not unlocked healing yet! (Requires level 5)")
    
    # allows heroes to attack the enemy
    def attack_enemy(self, player):
        # Generate damage based on the slime's attack, plus a random factor
        damage = self.attack + random.randint(1, 5)  # Increased random range for more variety
        print(f"{self.name} attacks {player.name} for {damage} damage!")
        player.take_damage(damage)

# Slow print for visual appeal in the game
def slow_print(text, delay=0.05):
    """Print text slowly one character at a time with a small delay."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Newline after the text is printed

# The game function where you battle against a slime

def battle(players, enemy):
    print("A Slime draws near!")
    for player in players:
        print(f"{player.name}: {player.health}/{player.max_health} HP")
    
    while enemy.health > 0 and any(player.health > 0 for player in players):
        for player in players:
            if player.health > 0:
                print("\n" + "-"*30)  # Add a separator for clarity
                print(f"{player.name}'s Turn:")
                # Asks for player's action
                while True:
                    action = input(f"{player.name}, choose your action (attack, heal, use item, inventory, equip): ").strip().lower()
                    if action in ["attack", "use item", "inventory", "equip"]:  # Valid actions
                        break
                    elif action == "heal":
                        if isinstance(player, (Priest, Mage)):  # Only Priests and Mages can heal
                            break
                        else:
                            print("Invalid choice! Only Priests and Mages can heal.")
                            continue  # Ask for action again
                    else:
                        print("Invalid choice, please try again.")
                        continue

                if action == "attack":
                    player.attack_enemy(enemy)
                elif action == "heal" and isinstance(player, (Priest, Mage)):
                    target = random.choice(players)
                    player.heal(target)
                elif action == "use item":
                    item_name = input("Which item would you like to use? (Medicinal Herb, Strong Medicine, Apple): ").strip()
                    if not player.use_item(item_name):
                        print("Item could not be used.")
                    else:
                        print(f"{player.name} uses {item_name}!")
                elif action == "inventory":
                    player.show_inventory()  # Show inventory without taking a turn
                    continue  # Don't break, allow the player to pick another action
                elif action == "equip":
                    item_name = input("Which item would you like to equip? (Copper Sword, Leather Armor, etc.): ").strip()
                    if not player.equip_item(item_name):
                        print("Item could not be equipped.")
                    else:
                        print(f"{player.name} equips {item_name}!")

                print("\n" + "-"*30)  # Add a separator for clarity

                # After player's action, the enemy attacks if still alive
                if enemy.health > 0:
                    print(f"{enemy.name}'s Turn:")
                    enemy.attack_enemy(player)
                if enemy.health <= 0:
                    print("The Slime is defeated!")
                    player.gain_experience(50)
                    return

                

# allows the game to be started
def main():
    print("Welcome, adventurer! Loading your saved game if available...")

    # Try to load the saved player
    player = Player.load_player()

    if not player:
        # If no saved player is found, ask for class selection
        print("No saved player found. Please choose your class.")
        hero_classes = {"warrior": Warrior, "mage": Mage, "priest": Priest, "thief": Thief}
        
        # asks for class selection
        while True:
            hero_type = input("Choose your class (Warrior, Mage, Priest, Thief): ").strip().lower()
            if hero_type in hero_classes:
                break
            print("Invalid choice, please try again.")
        
        hero_name = input("Enter your hero's name: ")
        player = hero_classes[hero_type](hero_name)  # Create new player based on the class chosen
    
    else:
        # If a saved player is loaded, prevent class change and just inform the user of their class
        print(f"Welcome back, {player.name}! You are playing as a {player.__class__.__name__.capitalize()}.")

        # Option to reset player data
        reset_choice = input("Would you like to reset your character and stats? (yes/no): ").strip().lower()
        if reset_choice == "yes":
            player.reset_player()
            print("Your game has been reset.")
            # Prompt user to select class and name again
            hero_classes = {"warrior": Warrior, "mage": Mage, "priest": Priest, "thief": Thief}
            
            while True:
                hero_type = input("Choose your class (Warrior, Mage, Priest, Thief): ").strip().lower()
                if hero_type in hero_classes:
                    break
                print("Invalid choice, please try again.")
            
            hero_name = input("Enter your hero's name: ")
            player = hero_classes[hero_type](hero_name)  # Create new player based on the class chosen

    print("Loading...")
    time.sleep(3)
    print("Your quest begins now!")
    battle([player], Slime())

    # Save player data after battle
    player.save_player()

if __name__ == "__main__":
    main()