# AI Use Log: Treasure Hunt Assignment

**Tool used:** Claude (AI assistant, Claude Code desktop app)
**Date:** 2026-09-29

This log records every time I used AI during this assignment: what I asked, what it suggested (including any code), what I changed, and why the change works.

> **How this log was written:** I wrote my own first design and first working version of the code. The "Why it works" explanations below are based on my own program description of the game. I used AI to shorten them and match each one to its fix.

## 1. Review of my first design

**My design (written before using AI):**

| Class       | Attributes                           | Methods               |
| ----------- | ------------------------------------ | --------------------- |
| Place       | name, description, item              | visit()               |
| LockedPlace | inherited attributes + required_item | visit()               |
| Item        | name                                 | none                  |
| Player      | name, bag                            | collect(), show_bag() |
| Chest       | required_code, opened                | open()                |

**What I asked:** I shared the table above for feedback.

**Suggestions received (no code):**

1. `visit()` can't check the player's bag unless the player is passed in.
2. The `Chest` wasn't connected to any place.
3. `collect()` needs to receive the item, and I had to decide whether the place still has the item afterwards.
4. **Trap:** two different `Item` objects are not equal by default, even with the same name, so `if key in bag` can fail.
5. I had to decide which method holds the duplicate-item check.
6. Optional: an `unlocked` attribute so the lab stays open after the first entry.
7. I still needed to answer design questions 3 (going straight to the stage) and 4 (winning order).

---

## 2. Suggested design

**What I asked:** "What do you suggest as the design?"

**Suggestion received:** A revised version of **my** table (no code):

| Class                       | Attributes                              | Methods                                         |
| --------------------------- | --------------------------------------- | ----------------------------------------------- |
| `Item`                      | `name`                                  | none                                            |
| `Player`                    | `name`, `bag`                           | `collect(item)`, `has(item_name)`, `show_bag()` |
| `Place`                     | `name`, `description`, `item`           | `visit(player)`                                 |
| `LockedPlace(Place)`        | inherited + `required_item`, `unlocked` | `visit(player)` (overrides)                     |
| `Chest`                     | `required_code`, `opened`               | `open(player)`                                  |
| `Stage(Place)` _(optional)_ | inherited + `chest`                     | `visit(player)`                                 |

The AI left design questions 3 and 4 for me to answer myself.

**What I did with it:** I didn't create a separate `Stage` class. Instead I gave `Place` an optional `chest` attribute, so the Main Stage is an ordinary `Place` object. I answered questions 3 and 4 myself:

- **Going straight to the stage:** the player can enter, but `main_stage.chest.open(player)` fails because the bag has no secret code.
- **Winning order:** visit canteen → collect key → visit lab → collect code → visit stage → open chest.

---

## 3. Review of my updated design

**What I asked:** I sent my updated design decisions (the list above, plus: clear `place.item` to `None` after collecting, duplicate check in `Player.collect()`, compare `item.name` values).

**Three issues found (no code):**

1. If `place.item` becomes `None` after pickup, visiting again passes `None` to `collect()`, so the duplicate message never appears. I needed to handle `None` separately.
2. If `Player` reaches into `Place` to clear the item, the two classes get tangled together. Suggestion: `collect()` returns `True`/`False` and the caller clears the item.
3. **Biggest issue:** `player.collect(lab.item)` would let the player take the code without the key. Collecting from the lab must only happen after `visit()` succeeds.

**How I handled it (in my own code):**

- `collect()` checks `if item is None` first, then checks for duplicates, and returns `True` or `False`.
- The main program clears the item only when collection works: `if player2.collect(canteen.item): canteen.item = None`.
- The lab's code is only collected inside `if computer_lab.visit(player2):`.
- The duplicate case is shown at the end with `player2.collect(code)`.

---

## 4. Python docs and code skeleton

**What I asked:** "Use Python official docs and model this problem statement."

**Response:** The AI again declined to write the full program, because of the assignment rule. It gave me links to the official Python docs:

| Topic                        | Link                                                                          |
| ---------------------------- | ----------------------------------------------------------------------------- |
| Classes, `__init__`, `self`  | https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes       |
| Class vs. instance variables | https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables  |
| Inheritance                  | https://docs.python.org/3/tutorial/classes.html#inheritance                   |
| `super()`                    | https://docs.python.org/3/library/functions.html#super                        |
| Lists                        | https://docs.python.org/3/tutorial/datastructures.html#more-on-lists          |
| `any()`                      | https://docs.python.org/3/library/functions.html#any                          |
| `if` statements              | https://docs.python.org/3/tutorial/controlflow.html#if-statements             |
| f-strings                    | https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals |

**Code suggested:** an empty skeleton built from my design. Every method body was a `TODO` for me to fill in:

```python
class Item:
    def __init__(self, name):
        # TODO: store the name
        pass


class Player:
    def __init__(self, name):
        # TODO: name, and an empty bag
        pass

    def has(self, item_name):
        # TODO: True if any item in the bag has this name (see any())
        pass

    def collect(self, item):
        # TODO: handle None, refuse duplicates, otherwise add to bag
        # Return True/False so the caller knows whether it worked
        pass

    def show_bag(self):
        # TODO: print the bag contents, or say it's empty
        pass


class Place:
    def __init__(self, name, description, item=None):
        # TODO
        pass

    def visit(self, player):
        # TODO: print the description; return True (ordinary places always let you in)
        pass


class LockedPlace(Place):
    def __init__(self, name, description, required_item, item=None):
        # TODO: call the parent's __init__ with super(), then add the extra attributes
        pass

    def visit(self, player):
        # TODO: already unlocked? has the required item? otherwise refuse
        # Same signature as Place.visit -> polymorphism
        pass


class Chest:
    def __init__(self, required_code):
        # TODO
        pass

    def open(self, player):
        # TODO: already open? has the code? -> win; otherwise refuse
        pass
```

Three tips came with it: only collect from the lab if `visit()` returned `True`; run the code after finishing each class; and use a fresh player for each route.

**What I did differently from the skeleton:**

- I stored item **names** (strings) in the bag instead of `Item` objects.
- I didn't write `has()`. I used `in self.bag` directly in three places. (This was added later as fix 5.)
- I added an optional `chest` parameter to `Place` so the Main Stage can hold the chest.
- I wrote every method body, all the object creation, and both routes myself.

---

## 5. Review of my first working code

**What I asked:** I pasted my complete first version of `treasure_hunt.py` for review.

**Result:** The AI ran it. Both routes worked and all four required cases were handled. It then reported:

| Priority   | #   | Problem                                                                             | Evidence                                                                        |
| ---------- | --- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Must fix   | 1   | `Place.visit()` returned `None` while `LockedPlace.visit()` returned `True`/`False` | Test loop printed `returned: None` (Canteen) and `returned: True` (Lab)         |
| Must fix   | 2   | No explicit polymorphism demonstration                                              | `visit()` was never called on both kinds of place side by side                  |
| Should fix | 3   | "with the key" hard-coded in `LockedPlace.visit()`                                  | Wrong if a different item unlocks the door                                      |
| Should fix | 4   | `unlocked` stayed `True` across different players                                   | A new player with an empty bag entered the Lab after another player unlocked it |
| Optional   | 5   | The same bag check was written three times                                          | `in player.bag` in `collect()`, `LockedPlace.visit()` and `Chest.open()`        |

---

## 6. Fixed code: each change, before and after

**What I asked:** "Write the fixed code with explanation. Create the class diagram also."

The AI kept my code and made only the five changes below. Everything else in `treasure_hunt.py` is my original code.

### Fix 1: `Place.visit()` returns `True`

**Before (mine):**

```python
    def visit(self, player):
        print(f"\nYou visit the {self.name}.")
        print(self.description)

        if self.item:
            print(f"You can see a {self.item.name} here.")

        if self.chest:
            print("There is a trophy chest here.")
```

**After:**

```python
        if self.chest:
            print("There is a trophy chest here.")

        return True
```

**Why it works:** A normal place lets the player in directly, so its `visit()` should report success. Before, `Place.visit()` returned `None` while `LockedPlace.visit()` returned `True` or `False`. Now both return the same kind of answer, so the program can treat any place the same way, e.g. `if place.visit(player):`, whether it's the Canteen or the Computer Lab. This is what lets polymorphism work: different kinds of place can be used interchangeably.

---

### Fix 2: Adding a polymorphism demo

**Before:** no code. `visit()` was never called on both kinds of place side by side.

**After:**

```python
print("========== POLYMORPHISM DEMO ==========")

canteen, computer_lab, main_stage, code = setup()
visitor = Player("Visitor")

# Same method call, different behaviour depending on the kind of place
for place in [canteen, computer_lab]:
    result = place.visit(visitor)
    print(f"-> {place.name}: entered = {result}")
```

**Output:**

```
You visit the Canteen.
The canteen is almost empty after the final-hour rush.
You can see a key here.
-> Canteen: entered = True

The Computer Lab is locked.
You need the key to enter.
-> Computer Lab: entered = False
```

**Why it works:** The Canteen (a `Place`) and the Computer Lab (a `LockedPlace`) are stored together in one list, and the loop makes the same call, `place.visit(visitor)`, on each. Python picks the method from the object's actual class. For the Canteen it runs `Place.visit()`, which lets the visitor in. For the Computer Lab it runs the overridden `LockedPlace.visit()`, which checks for the key first and refuses. It's the same method call with different behaviour, which is exactly what the assignment asks me to show.

---

### Fix 3: Unlock message uses the required item's name

**Before (mine):**

```python
            print(f"\nYou unlock the {self.name} with the key.")
```

**After:**

```python
            print(f"\nYou unlock the {self.name} with the {self.required_item.name}.")
```

**Why it works:** The locked place already knows which item it needs, because it's stored in `self.required_item`. Reading the name from that attribute means the message always matches the item that actually unlocked the door. If I change the lab to need a different item during the in-class exercise, I only change `required_item=` in `setup()`, and the message updates by itself.

---

### Fix 4: Creating a fresh world with `setup()`

**Before (mine):** all objects were created once at the top level, and both routes shared them:

```python
key = Item("key")
code = Item("secret code")
trophy_chest = Chest("secret code")
canteen = Place(...)
computer_lab = LockedPlace(...)
main_stage = Place(...)
```

**After:** the same objects are created inside a function, and each demo calls it:

```python
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

# before each route:
canteen, computer_lab, main_stage, code = setup()
```

**Why it works:** Objects remember their state. Once the lab's `unlocked` becomes `True`, or the chest's `opened` becomes `True`, those objects stay that way. Every call to `setup()` builds a brand-new game world with new places, items and chest. Player 1's failed route and Player 2's winning route therefore each get their own objects, and nothing one player does can affect the other's game. Without this, a later player could walk into a lab that an earlier player had already unlocked.

---

### Fix 5: Adding `Player.has()`

**Before (mine):** the same bag check was written in three different classes:

```python
# Player.collect()
if item.name in self.bag:
# LockedPlace.visit()
if self.required_item.name not in player.bag:
# Chest.open()
if self.required_code not in player.bag:
```

**After:**

```python
# Player
def has(self, item_name):
    return item_name in self.bag

# Player.collect()
if self.has(item.name):
# LockedPlace.visit()
if not player.has(self.required_item.name):
# Chest.open()
if not player.has(self.required_code):
```

**Why it works:** The bag belongs to the player, so the player should be the one to answer "do you have this item?". Other classes now ask the player through `has()` instead of looking inside `player.bag` themselves. That keeps the bag's details inside the `Player` class (encapsulation), and the check is written once. If I later changed how the bag is stored, I would only need to update `has()`.

---

## 8. How the AI handled the fixes

This is how the AI found and checked each fix, so I can explain where they came from:

1. **It ran my original code first.** It copied my code into a temporary file and ran it. Both routes worked and all four required cases printed correctly: lab without key, chest without code, duplicate item, and the win.
2. **It added a test loop to look for hidden bugs.** It appended a loop that called `visit()` on the Canteen and the Lab with a brand-new player. That test showed two problems:
   - `returned: None` for the Canteen and `returned: True` for the Lab, so the two methods returned different kinds of values (fix 1).
   - The new player with an **empty bag** got into the Lab, because an earlier player had already unlocked it (fix 4).
3. **It compared my code with the assignment's requirements.** It found there was no side-by-side polymorphism demo (fix 2), and that the hard-coded "key" would break the in-class "change which item unlocks a door" exercise (fix 3).
4. **It sent me the review before changing anything.** The issues went back to me as a list ("must fix" / "should fix" / "fine to keep"). Code changes only happened after I asked for the fixed version.
5. **It made small changes and kept my code.** It kept my class structure, messages, variable names and comments, and only added the five changes above.
6. **It ran the fixed code.** It confirmed the polymorphism demo now prints `entered = True` for the Canteen and `entered = False` for the Lab, and that both routes still produce the correct output. The final output is saved in `output.txt`.

**Suggestions I kept as they were (reviewed, not changed):**

- Storing names (strings) in the bag instead of `Item` objects. This avoids the object-comparison trap. `Item` is kept so items can be extended later, e.g. by adding a description.

---

## 9. Class diagram and project setup

**What I asked:** a class diagram, and to put everything in a `treasureHunt` folder with a `uv` virtual environment.

**What the AI did:**

- Drew the class diagram from my final code (`class_diagram.svg`). It shows all five classes with their attributes and methods, the inheritance arrow from `LockedPlace` to `Place`, and which classes hold which objects.
- Created a virtual environment with `uv venv` (Python 3.13.2). The program only uses built-in Python, so no packages were installed.
- Ran the program and saved the output of all three demos to `output.txt`.

**Project folder:**

```
treasureHunt/
├── .venv/               uv virtual environment
├── treasure_hunt.py     final code
├── output.txt           output of the polymorphism demo, failed route and winning route
├── class_diagram.svg    class diagram
└── AI_LOG.md            this log
```

---

## 10. Summary: who did what

| Part                                                                   | Who did it                                              |
| ---------------------------------------------------------------------- | ------------------------------------------------------- |
| First design (class table)                                             | Me                                                      |
| Design answers (going straight to stage, winning order)                | Me                                                      |
| Choosing to put the chest on `Place` instead of making a `Stage` class | Me                                                      |
| First working code (all classes, both routes)                          | Me                                                      |
| Program description explaining the OOP concepts                        | Me                                                      |
| Syntax example, design review, docs links, code skeleton               | AI                                                      |
| Code review and bug finding                                            | AI                                                      |
| The five fixes in section 7                                            | AI, reviewed and explained by me                        |
| "Why it works" explanations                                            | Based on my program description, shortened with AI help |
| Class diagram,                                                         | AI                                                      |
