#%%
import pickle
from entity.armor import Armor
# %%
armor = Armor()
datas = {
    'name': '철 검',
    'description': '강철로 만든 철 검이다.',
    'required_stat': {"STR": 10},
    'required_class': ['Warrior'],
    'up_stat': {'STR':10},
    'attack': 50,3
    'defense': 0,
    'hp': 0,
    'mp': 0,
    'drop': 0 ,
    'type': '무기'
}
armor.AddItem(datas)
# %%
from entity.armor import Armor

armor = Armor()
armor.output()
# %%
from entity.money import Money
money = Money()
money.output()

#%%
from glob import glob
glob('./UI/ui_files/*')