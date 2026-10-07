class Item:
    def __init__(self, name):
        self.name = name


class Player:
    def __init__(self, name):
        self.name = name
        self.bag = []

    def has(self, item_name):
        return item_name in self.bag

    def collect(self, item):
        if item is None:
            print("There is nothing to collect here.")
            return False

        if self.has(item.name):
            print(f"You already have the {item.name}.")
            return False

        self.bag.append(item.name)
        print(f"You collected the {item.name}.")
        return True

    def show_bag(self):
        if self.bag:
            print("Your bag contains:", ", ".join(self.bag))
        else:
            print("Your bag is empty.")


class Place:
    def __init__(self, name, description, item=None, chest=None):
        self.name = name
        self.description = description
        self.item = item
        self.chest = chest

    def visit(self, player):
        print(f"\nYou visit the {self.name}.")
        print(self.description)

        if self.item:
            print(f"You can see a {self.item.name} here.")

        if self.chest:
            print("There is a trophy chest here.")

        return True


class LockedPlace(Place):
    def __init__(self, name, description, required_item, item=None):
        super().__init__(name, description, item)
        self.required_item = required_item
        self.unlocked = False

    def visit(self, player):
        if not self.unlocked:
            if not player.has(self.required_item.name):
                print(f"\nThe {self.name} is locked.")
                print(f"You need the {self.required_item.name} to enter.")
                return False

            self.unlocked = True
            print(f"\nYou unlock the {self.name} with the {self.required_item.name}.")

        print(f"You enter the {self.name}.")
        print(self.description)

        if self.item:
            print(f"You can see a {self.item.name} here.")

        return True


class Chest:
    def __init__(self, required_code):
        self.required_code = required_code
        self.opened = False

    def open(self, player):
        if self.opened:
            print("The trophy chest is already open.")
            return

        if not player.has(self.required_code):
            print("The chest is locked. You need the secret code.")
            return

        self.opened = True
        print("\nThe secret code works!")
        print("The trophy chest opens.")
        print("🏆 Congratulations! You found the winning trophy!")


# --------------------------------------------------
# CREATE A FRESH GAME WORLD
# --------------------------------------------------

def setup():
    key = Item("key")
    code = Item("secret code")

    trophy_chest = Chest("secret code")

    canteen = Place(
        "Canteen",
        "The canteen is almost empty after the final-hour rush.",
        item=key
    )

    computer_lab = LockedPlace(
        "Computer Lab",
        "Computers hum quietly. A secret code is hidden here.",
        required_item=key,
        item=code
    )

    main_stage = Place(
        "Main Stage",
        "The stage is decorated for the closing ceremony.",
        chest=trophy_chest
    )

    return canteen, computer_lab, main_stage, code


# ==================================================
# POLYMORPHISM DEMO
# ==================================================

print("========== POLYMORPHISM DEMO ==========")

canteen, computer_lab, main_stage, code = setup()
visitor = Player("Visitor")

# Same method call, different behaviour depending on the kind of place
for place in [canteen, computer_lab]:
    result = place.visit(visitor)
    print(f"-> {place.name}: entered = {result}")


# ==================================================
# FAILED ROUTE
# ==================================================

print("\n========== FAILED ROUTE ==========")

canteen, computer_lab, main_stage, code = setup()
player1 = Player("Player 1")

# Player goes directly to the stage
main_stage.visit(player1)

# Player tries to open the chest without the code
main_stage.chest.open(player1)

# Player tries to enter the lab without the key
computer_lab.visit(player1)

player1.show_bag()


# ==================================================
# WINNING ROUTE
# ==================================================

print("\n========== WINNING ROUTE ==========")

canteen, computer_lab, main_stage, code = setup()
player2 = Player("Player 2")

# 1. Visit the canteen
canteen.visit(player2)

# 2. Collect the key
if player2.collect(canteen.item):
    canteen.item = None

player2.show_bag()

# 3. Enter the computer lab
if computer_lab.visit(player2):

    # 4. Collect the secret code
    if player2.collect(computer_lab.item):
        computer_lab.item = None

player2.show_bag()

# 5. Go to the main stage
main_stage.visit(player2)

# 6. Open the trophy chest
main_stage.chest.open(player2)

# Try collecting the same code again
player2.collect(code)
