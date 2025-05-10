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
FAST_MODE = False  # Fast printing mode
import random
import json
import time

def slow_print(text: str, delay: float = 0.05, enabled: bool = True):
    """Print text slowly unless fast mode is enabled."""
    if enabled and not FAST_MODE:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    else:
        print(text)


class Item:
    def __init__(self, name: str, category: str, upStats: str = ""):
        self.name = name
        self.category = category
        self.upStats = upStats or {}

class Weapon(Item):
    def __init__(self, name: str, attack_bonus: int):
        super().__init__(name, category="weapon", upStats=f"Attack Bonus: {attack_bonus}")
        self.attack_bonus = attack_bonus

class Consumable(Item):
    def __init__(self, name: str, heal_amount: int):
        super().__init__(name, category="consumable", upStats=f"Heals {heal_amount} HP")
        self.heal_amount = heal_amount

# Player class

class Player:
    def __init__(self, name: str, health: int, attack: int, defense: int, weapon: str, level: int = 1, experience: int = 0):
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

    def load_inventory(self) -> dict:
        """Loads the player's inventory from a JSON file."""
        try:
            with open("inventory.json", "r") as file:
                inventory_data = json.load(file)
                inventory = {category: {item_name: Item(**item_info) for item_name, item_info in items.items()} for category, items in inventory_data.items()}
                return inventory
        except FileNotFoundError:
            return {"swords": {}, "armor": {}, "food": {}, "potions": {}, "daggers": {}, "wands": {}, "staffs": {}}

    def save_inventory(self):
        with open("inventory.json", "w") as file:
            json.dump({cat: {name: vars(item) for name, item in items.items()} for cat, items in self.inventory.items()}, file, indent=4)
# Load items from the healing_items.json file
    def load_items(self) -> dict:
        try:
            with open("healing_items.json", "r") as file:
                items_data = json.load(file)
                return {item_name: Item(**item_info) for item_name, item_info in items_data.items()}
        except FileNotFoundError:
            print("Healing items file not found!")
            return {}

    def save_player(self):
        data = {
            "name": self.name,
            "level": self.level,
            "experience": self.experience,
            "health": self.health,
            "max_health": self.max_health,
            "attack": self.attack,
            "defense": self.defense,
            "weapon": self.weapon
        }
        with open("player_data.json", "w") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load_player(cls):
        try:
            with open("player_data.json", "r") as file:
                data = json.load(file)
                return cls(**data)
        except FileNotFoundError:
            print("No saved player data found!")
            return None

    def reset_player(self):
        self.level = 1
        self.experience = 0
        self.health = self.max_health
        self.attack = 10
        self.defense = 5
        self.weapon = "Sword"

    def take_damage(self, damage: int):
        damage_taken = max(0, damage - self.defense)
        self.health -= damage_taken
        self.health = max(0, self.health)
        slow_print(f"{self.name} takes {damage_taken} damage! Remaining health: {self.health}")
        if self.health == 0:
            slow_print(f"{self.name} has been defeated!")

    def gain_experience(self, amount: int):
        if self.level == 99:
            slow_print(f"{self.name} gains {amount} EXP but remains at level 99.")
            return
        self.experience += amount
        self.check_level_up()

    def check_level_up(self):
        required_exp = self.level * 50
        while self.experience >= required_exp and self.level < 99:
            self.experience -= required_exp
            self.level += 1
            self.max_health = int(30 + (self.level - 1) * (550 / 98))
            self.health = self.max_health
            slow_print(f"{self.name} leveled up to Level {self.level}! Max Health is now {self.max_health}.")
            required_exp = self.level * 50

    def show_inventory(self):
        slow_print("Inventory:")
        for category, items in self.inventory.items():
            item_list = ', '.join(items.keys()) if items else 'None'
            slow_print(f"{category.capitalize()}: {item_list}")
        input("Press Enter to continue...")

    def equip_item(self, item_name: str):
        for category in ["swords", "daggers", "wands", "staffs", "armor"]:
            for stored_item_name, item in self.inventory[category].items():
                if item_name.lower() == stored_item_name.lower():
                    if item.category == "armor":
                        self.defense += 5
                    else:
                        self.attack += 5
                        self.weapon = item.name
                    del self.inventory[category][stored_item_name]
                    slow_print(f"{self.name} equips {item.name}! Stats improved.")
                    return True
        slow_print(f"Cannot equip {item_name}.")
        return False

    def use_item(self, item_name: str):
        for category in ["potions", "food"]:
            for stored_item_name, item in self.inventory[category].items():
                if item_name.lower() == stored_item_name.lower():
                    if item.category == "potions":
                        heal = 30
                    else:
                        heal = 10
                    self.health = min(self.max_health, self.health + heal)
                    slow_print(f"{self.name} uses {stored_item_name} and heals {heal} HP!")
                    del self.inventory[category][stored_item_name]
                    return True
        slow_print(f"Item {item_name} could not be used.")
        return False

    def attack_enemy(self, enemy):
        damage = self.attack + random.randint(1, 5)
        slow_print(f"{self.name} attacks {enemy.name} with {self.weapon} for {damage} damage!")
        enemy.take_damage(damage)

# Enemy classes 

class Slime(Player):
    def __init__(self):
        super().__init__("Slime", health=60, attack=10, defense=2, weapon="Slime Body")
        self.drops = ["Potion", "Apple"]

    def attack_enemy(self, player):
        damage = self.attack + random.randint(1, 5)
        slow_print(f"{self.name} attacks {player.name} for {damage} damage!")
        player.take_damage(damage)

    def drop_item(self):
        if random.random() < 0.3:
            return random.choice(self.drops)
        return None

# game functions

def battle(player: Player, enemy: Player):
    slow_print("A wild Slime appears!")
    while player.health > 0 and enemy.health > 0:
        slow_print("\n--- Your Turn ---")
        action = input("Choose action (attack, use item, inventory, equip): ").strip().lower()

        if action == "attack":
            player.attack_enemy(enemy)
        elif action == "use item":
            item = input("Which item would you like to use? ").strip()
            player.use_item(item)
        elif action == "inventory":
            player.show_inventory()
            continue
        elif action == "equip":
            item = input("Which item would you like to equip? ").strip()
            player.equip_item(item)
        else:
            slow_print("Invalid action.")
            continue

        if enemy.health > 0:
            slow_print("\n--- Enemy's Turn ---")
            enemy.attack_enemy(player)

    if player.health > 0:
        slow_print("Victory!")
        player.gain_experience(50)
        drop = enemy.drop_item()
        if drop:
            slow_print(f"The Slime dropped a {drop}!")
            player.inventory["potions"][drop] = Item(drop, "potion", "Heals 30 HP")
    else:
        slow_print("You were defeated...")

def create_new_player() -> Player:
    hero_classes = {"warrior": Warrior, "mage": Mage, "priest": Priest, "thief": Thief}
    while True:
        hero_type = input("Choose your class (Warrior, Mage, Priest, Thief): ").strip().lower()
        if hero_type in hero_classes:
            break
        slow_print("Invalid choice, try again.")
    hero_name = input("Enter your hero's name: ").strip()
    return hero_classes[hero_type](hero_name)

class Warrior(Player):
    def __init__(self, name: str):
        super().__init__(name, health=30, attack=15, defense=10, weapon="Sword")

class Mage(Player):
    def __init__(self, name: str):
        super().__init__(name, health=30, attack=20, defense=5, weapon="Wand")

class Priest(Player):
    def __init__(self, name: str):
        super().__init__(name, health=30, attack=8, defense=7, weapon="Staff")

class Thief(Player):
    def __init__(self, name: str):
        super().__init__(name, health=30, attack=12, defense=8, weapon="Dagger")

#Calling the game to start

def main():
    slow_print("Welcome, adventurer!")
    player = Player.load_player()

    if not player:
        player = create_new_player()

    input("Loading complete! Press Enter to begin your quest!")
    battle(player, Slime())

    player.save_player()
    player.save_inventory()

if __name__ == "__main__":
    main()

    # new changes to project #3
