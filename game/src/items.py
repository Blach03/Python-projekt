import time
import threading


class Item:
    def __init__(self, name, description, price, image, attack: float = 0, hp=0, defense=0,
                 attack_range: float = 0, attack_speed: float = 0, movement_speed: float = 0):
        self.name = name
        self.description = description
        self.image = image
        self.price = price
        self.attack = attack
        self.hp = hp
        self.defense = defense
        self.range = attack_range
        self.attack_speed = attack_speed
        self.movement_speed = movement_speed

    def __str__(self):
        return f"{self.name}: {self.description}"
    

class Potion:
    def __init__(self, name, image, description, count, price, stat):
        self.name = name
        self.description = description
        self.image = image
        self.count = count
        self.price = price
        self.stat = stat

    def use(self, player):
        self.count -= 1
        if self.name == "Healing potion":
            player.current_hp = min(player.current_hp + self.stat, player.hp)
        elif self.name == "Defence potion":
            player.defense += self.stat

            def remove_def():
                time.sleep(180)
                player.defense -= self.stat

            threading.Thread(target=remove_def).start()

        elif self.name == "Attack potion":
            player.attack += self.stat

            def remove_atk():
                time.sleep(180)
                player.attack -= self.stat

            threading.Thread(target=remove_atk).start()

        elif self.name == "Regeneration potion":
            def regenerate():
                for _ in range(60):
                    player.current_hp = min(player.current_hp + self.stat, player.hp)
                    time.sleep(1)

            threading.Thread(target=regenerate).start()


all_items = [Item("Sentinel Aegis", "Prevents first incoming \nstrike in every room", 1500, '../resources/shield.png',
                  defense=10, hp=30),
             Item("Sword", "Does nothing", 1000, '../resources/sword.png', attack=10, hp=10, attack_speed=0.2),
             Item("Thornforge Armor", "Damages enemies for 30% damage \ndealt to you", 2000,
                  '../resources/thornforge.png', defense=15, movement_speed=-1),
             Item("Wings", "Allows flying over terrain", 5000, '../resources/wings.png', movement_speed=1),
             Item("Soulthirster Blade", "Heals for 5% of damage dealt", 2500, '../resources/soulthirster.png',
                  attack=20),
             Item("Vorpal Shard", "Gives additional 20% attack", 3000, '../resources/dagger.png', attack=20,
                  movement_speed=0.5),
             Item("Wyrmblade", "Deals additional 5% max health \nper hit (1% to bosses)", 2000, '../resources/wyrmblade.png', attack=15, hp=20, attack_range=0.2,
                  movement_speed=- 0.5),
             Item("Guardian's Edge", "Deals more damage to enemies \nwith lower health than you", 2000, '../resources/guardians edge.png', attack=10, hp=20, defense=10),
             Item("Arcane Halo", "Deals damage around you", 1800, '../resources/disc.png', attack=5, hp=20),
             Item("Scythe", "Deals triple damage \non the first strike", 2800, '../resources/scythe.png', attack=35),
             Item("Healing amulet", "Heals some missing health \nafter killing enemy", 1200, '../resources/amulet.png',
                  defense=5, hp=20),
             Item("Polearm", "Has 30% chance to deal \ndouble damage", 2000, '../resources/polearm.png', attack=20, attack_speed=0.3,
                  movement_speed=0.5),
             Item("Retaliation Raiment", "Once per room after getting damaged \ndeals damage to all enemies", 2200,
                  '../resources/retaliation.png', hp=30),
             Item("Heartguard", "After each enemy killed \ngives you 1 HP", 3000,
                  '../resources/heartguard.png', hp=40),
             Item("Phantom boots", "Has 20% chance \nto dodge an attack", 2600,
                  '../resources/phantom.png', hp=10, defense = 10),

            
             Potion("Healing potion", '../resources/health_potion.png', 'Heals 50 HP', 5, 750, 50),
             Potion("Defence potion", '../resources/defence_potion.png', 'Gives 20 defence for 3 min', 3, 750, 20), 
             Potion("Attack potion", '../resources/attack_potion.png', 'Gives 30 attack for 3 min', 3, 750, 30), 
             Potion("Regeneration potion", '../resources/regen_potion.png', 'Restores 1 HP per secound for 1 min', 3, 750, 1)
             ]
