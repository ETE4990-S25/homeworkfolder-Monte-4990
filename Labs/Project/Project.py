
class Warrior(object): # Hero class
    def __init__(self, name, health): # Constructor
        self.name = name
        self.health = health

    def take_damage(self, damage): # Method
        self.health -= damage
        print(self.name + " has taken " + str(damage) + " damage!")

    def is_alive(self): # Method
        return self.health > 0
    def status(self):
        return self.name + " is " + ("alive!" if self.is_alive() else "dead!")
    def __str__(self): # Method
        return self.name + " has " + str(self.health) + " health!"
    

Anthony = Warrior("Anthony", 100)
print(Anthony.status())
Anthony.take_damage(25)
print(Anthony.__str__())
print(Anthony.status())
Anthony.take_damage(100)
print(Anthony.status())