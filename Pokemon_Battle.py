import math
import json

with open("Pokedex.txt", encoding='utf8') as pokedex:
  my_pokedex = json.load(pokedex)

with open("Types.txt", encoding='utf8') as types:
  my_types = json.load(types)

class Pokemon:
  type_advantages = {"Fire": "Grass", "Water": "Fire", "Grass": "Water"}
  type_disadvantages = {"Water": ["Grass","Water"] , "Fire": ["Water", "Fire"], "Grass": ["Fire", "Grass"]}

  def __init__(self, name, level, type_, base_stats, maximum_health, current_health, is_knocked_out, xp=0):
    self.name = name
    self.level = level
    self.type_ = type_
    self.base_stats = base_stats
    self.maximum_health = maximum_health + level
    self.current_health = current_health + level
    self.is_knocked_out = is_knocked_out
    self.xp = xp
    self.xp_level_up = 72 * level
    

  def __repr__(self):
    return "Name {name}\nLevel: {level}\nType: {type}\nBase Stats: {base_stats}\nMax Health: {max_health}\nCurrent Health: {current_health}\nKnocked Out: {knocked_out}\nXp: {xp}".format(name=self.name, 
    level=self.level, type=self.type_,base_stats=self.base_stats, max_health=self.maximum_health, 
    current_health=self.current_health, knocked_out=self.is_knocked_out, xp=self.xp)
    

  def lose_health(self, damage):
    self.current_health -= damage
    if self.current_health <= 0:
      self.current_health = 0
    print("{name} took {damage} damage and current health is {health}".format(name=self.name, damage = damage, health=self.current_health))
    
  
  def gain_health(self, regen):
    self.current_health += regen
    if self.current_health > self.maximum_health:
      self.current_health = self.maximum_health
    print("{name} current health is {health}".format(name=self.name, health=self.current_health))

  def knocked_out(self, other_pokemon):
    if self.current_health <=0:
      self.is_knocked_out is True
      print("{name} got knocked out!".format(name=self.name))
      other_pokemon.gain_xp(self.level *15)

  def revive(self, regen):
    if self.is_knocked_out:
      self.current_health += regen
      self.is_knocked_out = False
    print("{name} got revived!".format(name=self.name))

  def attack_pokemon(self, other_pokemon):
    damage = self.base_stats["Attack"] - (math.floor(other_pokemon.base_stats["Defense"] /2))
    for attacker_type in self.type_:
      for defending_type in other_pokemon.type_:
        if defending_type in my_types[attacker_type]["strengths"]:
          damage*=2
        elif defending_type in my_types[attacker_type]["weaknesses"]:
          damage = math.floor(damage/2)
        elif defending_type in my_types[attacker_type]["immunes"]:
          damage = 0
    other_pokemon.lose_health(damage)

#TRAINENRERER
class Trainer:
  def __init__(self, pokemon, name, potions, current_pokemon):     
    self.pokemon = pokemon
    self.name = name
    self.potions = potions
    self.current_pokemon = current_pokemon
  
  def use_potion(self, regen):
    print("{name} used a potion!".format(name=self.name))
    self.pokemon[self.current_pokemon].gain_health(regen)
  
  def attack_trainer(self, other_trainer):
    print("{name} attacked {other_trainer} with {pokemon}!".format(name=self.name, other_trainer = other_trainer.name, pokemon = self.pokemon[self.current_pokemon].name))
    self.pokemon[self.current_pokemon].attack_pokemon(other_trainer.pokemon[other_trainer.current_pokemon])
    other_trainer.pokemon[other_trainer.current_pokemon].knocked_out(self.pokemon[self.current_pokemon])
  
  def switch_pokemon(self, new_pokemon):
    if self.pokemon[new_pokemon].is_knocked_out is not True:
      self.current_pokemon = new_pokemon 
      print("{name} switched to {new_pokemon}!".format(name=self.name, new_pokemon=self.pokemon[new_pokemon].name))
    else:
      print("{name} is fainted, can't swicht out!".format(name = self.pokemon[new_pokemon].name))
  def gain_xp(self, xp_gained):
    self.xp += xp_gained
    print("{name} gained {xp} experience!".format(name=self.name, xp=xp_gained))
    while self.xp >= self.xp_level_up:
      self.xp-=self.xp_level_up
      self.level += 1
      print("{name} is now level {level}".format(name=self.name, level=self.level))
      self.xp_level_up = 72 * self.level


def add_pokemon(*args):
  party_pokemon = []
  for arg in args:
    party_pokemon.append(get_pokemon(arg))
  return party_pokemon

def get_pokemon(pokedex_id):
  pokemon = Pokemon(my_pokedex[pokedex_id-1]["name"]["english"], 50, my_pokedex[pokedex_id-1]["type"],my_pokedex[pokedex_id-1]["base"], my_pokedex[pokedex_id-1]["base"]["HP"], my_pokedex[pokedex_id-1]["base"]["HP"], False)
  return pokemon







     





