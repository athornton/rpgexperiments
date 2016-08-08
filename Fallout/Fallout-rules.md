# Fallout PNP Rules

## S.P.E.C.I.A.L. Characteristics

* Strength
* Perception
* Endurance
* Charisma
* Intelligence
* Agility
* Luck

These range from a minimum of `1` to a maximum of `10`.

## Skills

* Melee ( `S` )
* Small Guns ( `A` )
* Big Guns ( `(E + A ) / 2`)
* Explosives ( `( A + P ) / 2`)
* Repair ( `( I + A ) / 2` )
* Lockpick ( `( I + A ) / 2` )
* Science ( `I` )
* Speech ( `C` )
* Medic ( `( I + C ) / 2` )
* Sneak ( `A` )
* Observe ( `P` )

Skills range from a minumum of `0` to a maximum of `100`.

The letter or letters after the skill indicate the S.P.E.C.I.A.L.
characteristics that define the base skill level in that particular
skill.  For instance, `Melee` depends on `Strength`.

Base skill in a score is `5` times the controlling characteristic
(or average of characteristics, for something like `Medic`, which is
controlled by both `Intelligence` and `Charisma`), plus `Luck`
characteristic.

## Character Creation

Start with `1` point in each S.P.E.C.I.A.L. characteristic.  Distribute
`15` more points between them; `10` is the maximum you can have in a
characteristic. 

Calculate your base skill levels.  Then pick any three skills to `Tag!`.
Add `15` points to each of those skills.  Then distribute `20` more
points between your skills as you choose.  No skill may go above `100`.

Initial hit points are `20 + ( 2 * END)`.

## Mechanics

### Hit Points and Radiation Points

Hit points are reduced when you take damage.  At `0` Hit Points you're dead.

Radiation points ("Rads") reduce your maximum hit points.  If radiation
damage would cause your current hit points to exceed your new maximum,
your hit points drop to the new maximum.

If you are hit with an attack that does both hit point and rad damage,
apply the hit point damage first.

### Saving Throws

A Saving Throw is a `1d10` roll.  You want to roll under or equal to the
S.P.E.C.I.A.L. characteristic you are saving against.  The roll may be
modified by the save's difficulty. 

### Skill Checks

A skill check is a `1d100` roll; you want to roll under or equal to your
skill.  This may be modified by task difficulty.  An `01` is a critical
success; a `00` is a critical failure.  The degree by which you make or
fail the roll is likely to inform how well or poorly you did: a roll
right under your skill is  a just-barely success, while a roll far above
it is an ignominious (though not catastrophic) failure.

### Combat

Combat is effectively a series of skill checks against your Melee, Small
Guns, Big Guns, or Explosives skill.

Thrown weapons always use Explosives skill, even if the projectile
thrown is not, in fact, explosive.  Laying a mine uses Explosives skill,
modified by the weight of the creature stepping on it.  Flying creatures
do not set off mines, and a radroach is much less likely to than is a
Super Mutant.  Fortunately, this usually works out for the players,
since deadlier opponents also tend to be bigger ones.

#### Attacks

Start with the appropriate percentile skill.

Factor in the target's agility: `+ 10 - ( 2 x target's AGI)`

(So there's no modifier for an `AGI 5` target, a `+8` modifier for an
`AGI 1` target (and `+10` for an immobile target), and a `-10` modifier
against an `AGI 10` target.)

##### Melee

Melee attacks get the point-blank range modifier of `+20`.

Melee attacks also all have a damage modifier based on strength:
`(STR - 5) / 2` (round down)

##### Weapon Ranges

Point-blank range is anything under 2 meters.

These ranges may vary by particular weapon, but in general:

    Weapon Type: Short Range  Medium Range  Long Range  Maximum Range
    Pistols:     10 meters    25 meters     50 meters   100 meters
    Rifles:      20 m         50 m          100 m       400 m
    Shotguns:    5 m          10 m          20 m        25 m
    Flamers:     3 m           5 m          10 m        15 m
    Thrown:      5 m          10 m          25 m        25 + (5 * STR) m     

##### Weapon Attack Modifiers

Weapon ranges have the following modifiers applied:

  * point-blank `+20`
  * short `+5`
  * medium `0`
  * long `-20`
  * extreme `-40`

###### Scopes

`1` round aiming gives you `+20` (you can't use a scope at point-blank
range).  Rounds `2` and `3` each give you a further `+10`.

###### Called Shots

`-30%`, or `half your hit chance`, whichever is less, after
range and scope modifiers (so `25%` goes to `12%`, not `-5%`). Called
shot effects are:
  
* Headshot: target loses next action; save versus `END` or ignore armor. 
* Weapon arm: save versus `END` or lose weapon.
* Other arm: No mechanical effect; but on something with 2 claw attacks...
* Leg: speed reduced by `1/4` (save vs. `END` or `1/2`)
* Other Leg: further `1/4` / `1/2`

Note that these too may vary by target: headshots against robots are
notoriously ineffectual, and, for instance, you want to try to shoot
Deathclaws in the legs or in the belly rather than their skulls,
usually.

###### Pip-Boy Aiming

Should you be so fortunate as to have a Pip-Boy, you may take a round to
aim with it, and any range will be treated as the next lower one for
purposes of aiming (so short range is treated as point-blank, medium as
short, et cetera).  Melee and point-blank range are unaffected, except
that you lose a turn to aiming.  Thrown weapons do not get a Pip-Boy
aiming bonus.  You cannot use both a scope and a Pip-Boy to aim; it's
one or the other.

#### Ammunition

There are three ranges of ammunition capacity: `plenty`, `some`, and
`3-2-1`.  What these mean are:

* At `plenty` and `some`, you roll each time you fire a shot.  `Plenty`
  rolls a d20 for small, single-shot arms, and d12 for automatic or
  heavy weaponry.  If you roll a `1` your ammo capacity decreases to
  `some`.

* At `some` you roll a d6 (d4 for automatic or heavy weaponry).  If you
  roll a `1`, your ammo capacity decreases to `3-2-1`.

* `3-2-1` is how many shots (or bursts, for auto) you have left.

This works out to, on average, 20 shots from small arms from "plenty",
and

Ammo basically comes in units of "one or two loose rounds", "a clip",
and "a box".  These represent `3-2-1`, `some`, and `plenty`.

* If your current amount of ammo is less than what you find, you now
  have what you found. 

* If you are in `3-2-1` and you find loose rounds, if your total ammo
  count is 4 or greated, you have `some`.

* If you have `some` and you find a clip, roll d6.  On a `6`, you now
  have `plenty`; otherwise, you still have `some`.

#### Splash damage

Out to the first splash range increment, remove the highest die from the
damage result, and apply remaining damage to anyone within the splash
range.  Remove the next highest die and repeat for anyone within the
next range increment.  Repeat until you're out of dice.  This applies to
all damage types.

#### Burn damage

Burn damage functions somewhat like splash damage: on the second round,
discard the highest die from the damage result, and take the remainder
as damage on that round.  Repeat until out of dice.

If you are on fire, you may take an action to douse the flames.  That
removes another die from the damage result.

#### Poison damage

Some enemies, such as Radscorpions, make envenomed attacks.  The damage
will be given as the product of two die rolls (e.g. `1d8 x 1d4`).  The
first die roll is the damage; the second is the duration.  Each round of
the duration, the poisoned creature must make an `END` save (modified by
poison toxicity) or take the amount of damage indicated.  This damage is
re-rolled each round until the duration has expired.

If you are hit by a poisoned attack, but your armor causes you to take
no damage, you are not affected by the poison either.

#### Shotguns

Double damage at point-blank range, half damage at medium range,
one-quarter damage at long and extreme ranges.  This factor is applied
after any armor modifiers.

#### Misses (Splash and Collateral Damage)

Roll `1d8` to determine the direction in which you missed, `1` being
long, proceeding clockwise around to `5` being short, and so on.  The
amount by which you missed determines how much you missed by, although
there is no set formula for modifying distance by range.  The GM will
decide whether you might have caught the target (or someone else) in the
splash damage, or hit something that wasn't your intended target.

### Armor

Armor functions by removing certain damage dice from the pool.  If the
number to be ignored is larger than the largest number the die can roll,
the highest roll on that die is removed instead.  For instance, any
armor type will ignore a `3` rolled as the result of an unarmed attack.
Note that this means that you simply cannot cause damage to someone
wearing power armor with an unarmed punch.

* Light Armor: ignore all damage dice which are `4`s (or highest)
* Medium Armor: ignore all damage dice which are `6`s (or highest)
* Heavy: ignore all `8`s (or highest)
* Power: ignore all `powers of 2`, and highest.

A little bit of Python to allow experimentation with armor is
[here](https://github.com/athornton/rpgexperiments/tree/master/Fallout/FalloutArmor).

If a die is blocked, any modifier to that die is discarded as well.
Thus if a Super Mutant with a Nail Board (`1d6+1`) hit a player wearing
Light Armor, and rolled a `4` on his damage die,  that `5`-point hit
would do no damage, because both the `4` and the `+1` would be
discarded.

For purposes of simplicity, impact, burn, and radiation damage are all
treated identically for purposes of armor reduction.

### Morale

Most enemies encountered will have a morale score.  This is typically
rolled when a creature first takes damage and again when it has taken
half its hit points worth of damage.  For creatures in groups, if the
leader is defeated or flees, the remaining creatures should make a
morale check.  This may be modified based on circumstances; for
instance, a Raider high on Psycho will not need to check morale.

A morale check is `2d6` against the morale score.  If the roll is
higher than the morale score, the enemy will attempt to flee.  Typical
enemy morale scores are:

    Enemy              Morale
    Radstag            3
    Mole Rat           5
    Raider             6
    Feral Ghoul        8
    Super Mutant       9
    Deathclaw          12
    Robot              12

Leaders tend to have better morale than typical enemies of their type. 

### Weaponry

This section shows the weapon damage done on a successful hit with the
indicated weapon.  For weapons not shown, interpolate based on what it's
most like.  In general, multi-projectile weapons should do multiple
smaller dice worth of damage.

#### Melee

* Fist/Kick: `1d3`
* Brass Knuckles: `1d3 + 1`
* Switchblade/small knife: `1d4`
* Combat knife/Machete: `1d6`
* Baseball Bat: `1d6`
* Sledgehammer: `1d8`
* Ripper: `1d10`
* Super Sledge: `1d10`
  
#### Ranged

* 5mm: `1d4`
* .38/9mm: `1d6`
* 10mm/.45: `1d8`
* 20 ga.: `2d4`
* 5.56/.44: `1d10`
* 12 ga.: `3d4`
* .308: `2d6`
* .50: `2d10`
  
#### Thrown

* Grenade: `3d6`/splash (`2m`)
* Nuka Grenade: `4d8` + `1d6` rad/splash (`3m`)
* Molotov Cocktail: `6d4` burn/splash (`1m`)

#### Mines

* Frag Mine: `4d6`/splash (`1m`)
* Bottlecap Mine: `5d8`/splash (`1m`)
* Nuka Mine: `3d12` + `2d12` rad/splash (`2m`)

#### Energy

* Laser pistol: `1d6`
* Laser rifle: `1d10`
* Plasma pistol: `3d4` + `1d4` rad
* Plasma rifle: `2d8` + `1d6` rad
  
#### Heavy

* Flamer: `4d4` burn
* Missile: `5d6`/splash (`2m`) (`10m`/`30m`/`50m`/`200m`)
* Fat Man: `6d20` + `4d12` rad/splash(`5m`) (`15m`/`50m`/`100m`/`500m`)

## Healing

* Radiation damage decreases maximum HP until healed
 (with RadAway, a rad scrubber, or certain food items).
* Stimpaks heal `25 + Medic skill` HP
* Radaway heals `25 + Medic skill` Rad points
* Sleeping in a bed heals all HP up to current maximum HP.  No rad healing.

## Experience

At level `N`, you need `100 * N` more experience to get to the next one:

    Level     XP
    1         0
    2         100
    3         300
    4         600
    5         1000
    6         1500
    7         2100
       ...

When you level up, you can either: 
* add `1` point to a S.P.E.C.I.A.L. characteristic (up to a maximum of `10`)
* add `10 + INT + LCK` points to skills (up to a maximum of `100`)
 
At each level, you get `5 + Endurance` additional hit points.  Endurance
gains do not retroactively boost hit points, but only increase hit
points for that level and all subsequent levels.
