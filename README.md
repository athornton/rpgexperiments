# RPG Experiments

## [Fallout](https://github.com/athornton/rpgexperiments/tree/master/Fallout)

Fallout pen-and-paper RPG.

### Fallout/[FalloutArmor](https://github.com/athornton/rpgexperiments/tree/master/Fallout/FalloutArmor)

Working on a damage-reduction armor system for my homebrew Fallout
system.  It's a class (FalloutArmor.py) and a little harness
(fallout-armor.py).  It requires Python 3.4 (for the statistics module)
and you need matplotlib to get the graphs (but it will run without it).

### Fallout/[FalloutBattle](https://github.com/athornton/rpgexperiments/tree/master/Fallout/FalloutBattle)

Incremental progress towards a simulator for a battle in the Fallout
system.

Things implemented:

* Physical, burn, radiation, and poison damage
* Splash damage (mostly)
* Ongoing, decreasing-over-time effects.
* Morale checks and fleeing the arena
* Factions

Things not implemented:
* Aiming/aiming bonuses
* Reasonable, complex strategies
* Inventory items
* Healing
* Cover
* Actors occupying space/Actors blocking shots
* Splash damage on misses
