
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.inventory = []
    
    def is_alive(self):
        return self.health > 0
    
    def attack(self, target):
        print(f"{self.name} attacks {target.name} for {self.attack_power} damage")
        target.health -= self.attack_power

"""class Player(Character):
    - level
    - experience

    + gain_experience(xp): increase XP; if >= threshold, call level_up()
    + level_up(): level += 1, reset XP, boost stats
    + use_item(item): apply effect to self (e.g., heal)"""


class Player(Character):
    def __init__(self, name):
        super().__init__(name, health = 100, attack_power = 10)
        self.experience = 0
        self.level = 1
        self.max_health = 100
    
    def gain_experience(self, xp):
        print(f"{self.name} gains {xp} xp")
        self.experience += xp
        if self.experience >= 100:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.attack_power += 5
        self.health = health
        self.experience = 0
        print(f"{self.name} is now at level {self.level}. Long way to go.")
    
    def use_item(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                print(f" {self.name} uses {item.name} for boost!")
                item.apply(self)
                self.inventory.remove(item)
                return
        print(f"{item_name} not found in the inventory!")


"""class Enemy(Character):
    - loot (list of Item objects)
    - difficulty_level
"""

class Enemy(Character):

    def __init__(self, name, health, attack_power, difficulty_level = 1, loot = None):
        super().__init__(name, health = 80, attack_power = 8)
        self.difficulty_level = difficulty_level
        self.loot = loot if loot is not None else []
    
    def drop_loot(self):
        if self.loot:
            print(f"{self.loot} dropped!")
            for item in self.loot:
                print(f"-{item.name}")
            return self.loot
        else:
            print("no loot!")
            return []
    
    def decide_action(self, player):
        if self.is_alive():
            self.attack(player)
    

"""class Item:
    - name
    - effect (function or description)
    - type (e.g., "healing", "buff")

    + apply(target): based on type, modify target's attributes
"""

class Item:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value
    
    def apply(self, target):
        if self.type == "healing":
            healed = min(target.max_health - target.health, self.value)
            target.health += healed
            print(f"{target.name} healed for {healed} xp.")

        elif self.type == "buff":
            target.attack_power += self.value
            print(f"{target.name}'s attack power increases by {self.value}.")
        else:
            print(f"{self.name} has no effect.")
        





"""class Room:
    - description
    - enemy (optional)
    - item (optional)
    - is_exit (bool)
    - neighbors (dict with directions: Room)

    + enter(player): describe, trigger enemy or item interaction"""

    
    
class Room:
    def __init__(self, description, enemy = None, item = None, is_exit = False):
        self.description = description
        self.enemy = enemy
        self.item = item
        self.is_exit = is_exit
        self.neighbors = {}
    
    def enter(self, player):
        print(" \nYou enter a room")
        print(self.description)

        if self.enemy and self.enemy.is_alive():
            print(f"You see an enemy named {self.enemy.name}")
            return "combat"
        
        if self.item:
            print(f"you encountered an item named {self.item.name}")
            pick = input("Pick it up: Yes/ No - ").strip().lower()
            if pick == "yes":
                player.inventory.append(self.item)
                print(f"You picked up {self.item.name}")
                self.item = None
        
        if self.is_exit:
            print(f"Unlike your toxic relationship, You've found the exit! Congrats.")
            return "exit" 
        return "explore"



    """class Game:
    - player
    - rooms (maybe as graph/map)
    - current_room

    + start(): greet player, init player, set first room
    + game_loop(): while player is alive:
        - describe room
        - get player input (move, attack, use item)
        - resolve actions
"""

class Game:
    def __init__(self):
        self.player = None
        self.rooms = []
        self.current_room = None
    
    def start(self):
        name = input("Enter your name: ")
        self.player = Player(name)

        #items
        potion = Item("Health Potion", "healing", 25)
        sword = Item("Sword of strength", "buff", 5)
        #enemies
        goblin = Enemy("Goblin", 30, 10, difficulty_level= 1, loot = [potion])
        orc = Enemy("Orc", 50, 8, difficulty_level= 2, loot = [sword])
        #create rooms
        room1 = Room("A dark damp cave.", enemy = goblin)
        room2 = Room("Chamber with glowing mushrooms", item = sword)
        room3 = Room("Smelly and bitter noisy corner.", enemy= orc)
        exit_room = Room("Hallway type leading out", is_exit = True)
        
        room1.neighbors["east"] = room2
        room2.neighbors["west"] = room1
        room2.neighbors["north"] = room3
        room3.neighbors["south"] = room2
        room3.neighbors["east"] = exit_room
        exit_room.neighbors["west"] = room3

        self.rooms = [room1, room2, room3, exit_room]
        self.current_room = room1

        print(f"\n Welcome {self.player.name}, to the dungeon of trials muhahahaha....")
        self.game_loop()

    """while player and enemy are both alive:
    player attacks enemy
    if enemy is still alive:
        enemy attacks player
if player is dead:
    game over
if enemy is dead:
    player gains XP
    maybe loot
"""
    
    def game_loop(self):
        while self.player.is_alive():
            result = self.current_room.enter(self.player)
            if result == "exit":
                print("Congratulations! You escaped the trial!")
                break
            
            elif result == "combat":
                enemy = self.current_room.enemy
                while enemy.is_alive() and self.player.is_alive():
                    print(f"\nYour HP is: {self.player.health}")
                    print(f"\n{enemy.name}'s health: {enemy.health}")
                    action = input("do you want to [attack] [use item] or [run]?").strip().lower()

                    if action == "attack":
                        self.player.attack(enemy)

                        if enemy.is_alive():
                            enemy.attack(self.player)
                        
                        else:
                            print(f"{enemy.name} is defeated")
                            loot = enemy.drop_loot()
                            self.player.inventory.extend(loot)
                            self.player.gain_experience(50)
                    
                    elif action == "use item":
                        if not self.player.inventory:
                            print("You have no items.")
                            continue
                        print("Inventory:")
                        for i, item in enumerate(self.player.inventory):
                            print(f"{i+1}. {item.name}")
                        choice = input("Which item number? ").strip()
                        if choice.isdigit():
                            idx = int(choice) - 1
                            if 0 <= idx < len(self.player.inventory):
                                self.player.use_item(self.player.inventory[idx].name)
                            else:
                                print("Invalid choice.")
                        else:
                            print("Invalid input.")

                    elif action == "run":
                        print("You flee back to the previous room!")
                        break

                    else:
                        print("Invalid action.")
                    


                if not self.player.is_alive():
                    print("💀 You have been defeated. Game Over.")
                    break

                #Directions
            print("\nAvailable Directions: ")
            for direction in self.current_room.neighbors:
                    print(f"-{direction}")
            move = input("Where do you want to go? ").strip().lower()

            if move in self.current_room.neighbors:
                self.current_room = self.current_room.neighbors[move]

            else:
                print("Unfortunately, You can't go that way.")
                    

if __name__ == "__main__":
    game = Game()
    game.start()







        


