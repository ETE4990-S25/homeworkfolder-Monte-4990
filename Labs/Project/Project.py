import random
import json

class Player: # This class is for any character that is in the game, even NPCs and enemies
    def __init__(self, name, health, attack, defense, weapon):
        self.name = name
        self.experience = 0
        self.health = health
        self.attack = attack
        self.defense = defense
        self.weapon = weapon
        self.inventory = self.load_inventory()
    
    def load_inventory(self): # This function loads the inventory from a JSON file
        try:
            with open("inventory.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"swords": [], "food": [], "daggers": [], "wands": [], "staffs": [], "potions": []}
    
    def save_inventory(self): # This function saves the inventory to a JSON file
        with open("inventory.json", "w") as file:
            json.dump(self.inventory, file, indent=4)
    
    def equip_weapon(self, weapon_name): # This functions allows a player to equip a weapon when called
        for category in ["swords", "daggers", "wands", "staffs"]:
            if weapon_name in self.inventory[category]:
                self.weapon = weapon_name
                print(f"{self.name} equips {weapon_name}!")
                return
        print("Weapon not found in inventory!")
    
    def use_item(self, item_name): # This function allows a player to use an item when called
        if item_name in self.inventory["food"] or item_name in self.inventory["potions"]:
            self.health += 20
            print(f"{self.name} uses {item_name} and restores health! Current health: {self.health}")
            self.inventory["food"].remove(item_name) if item_name in self.inventory["food"] else self.inventory["potions"].remove(item_name)
            self.save_inventory()
        else:
            print("Item not found in inventory!")
    
    def take_damage(self, damage): # This function calculates the damage taken by a player
        damage_taken = max(0, damage - self.defense)
        self.health -= damage_taken
        print(f"{self.name} takes {damage_taken} damage! Remaining health: {self.health}")

    def attack_enemy(self, enemy):
        damage = self.attack + random.randint(1, 5)
        print(f"{self.name} attacks {enemy.name} with {self.weapon} for {damage} damage!")
        enemy.take_damage(damage)

class Warrior(Player):
    def __init__(self, name):
        super().__init__(name, health=120, attack=15, defense=10, weapon="Sword")

class Mage(Player):
    def __init__(self, name):
        super().__init__(name, health=80, attack=20, defense=5, weapon="Wand")
    
    def cast_spell(self, enemy):
        spell_damage = self.attack + random.randint(5, 10)
        print(f"{self.name} casts a fireball at {enemy.name} for {spell_damage} damage!")
        enemy.take_damage(spell_damage)

class Priest(Player):
    def __init__(self, name):
        super().__init__(name, health=90, attack=10, defense=7, weapon="Staff")
    
    def heal(self, ally):
        heal_amount = random.randint(10, 20)
        ally.health += heal_amount
        print(f"{self.name} heals {ally.name} with {self.weapon} for {heal_amount} health! {ally.name} now has {ally.health} HP.")

class Thief(Player):
    def __init__(self, name):
        super().__init__(name, health=100, attack=12, defense=8, weapon="Daggers")
    
    def steal(self, enemy):
        success = random.choice([True, False])
        if success:
            print(f"{self.name} successfully steals gold from {enemy.name}!")
        else:
            print(f"{self.name} fails to steal from {enemy.name}.")

class Slime(Player):
    def __init__(self):
        super().__init__("Slime", health=60, attack=5, defense=2, weapon="Slime Body")

# Example gameplay
def main():
    warrior = Warrior("Anthony")
    mage = Mage("Gandalf")
    priest = Priest("Healer")
    thief = Thief("Rogue")
    
    # Main enemy
    enemy = Slime()
    
    warrior.attack_enemy(enemy)
    mage.cast_spell(enemy)
    thief.steal(enemy)
    priest.heal(warrior)
    
    # Equip and use items
    warrior.equip_weapon("Excalibur")
    warrior.use_item("Health Potion")

if __name__ == "__main__":
    main()

# Anthony = Warrior("Anthony", 100)
print(Anthony.status())
Anthony.take_damage(25)
print(Anthony.__str__())
print(Anthony.status())
Anthony.take_damage(100)
print(Anthony.status())

