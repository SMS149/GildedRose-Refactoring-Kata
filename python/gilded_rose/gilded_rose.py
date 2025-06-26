# -*- coding: utf-8 -*-

import select
from abc import ABC, ABCMeta, abstractmethod
from tkinter import N

class GildedRose(object):

    def __init__(self, items):
        """
        Initialize the GildedRose with a list of items.
        :param items: A list of Item objects representing the inventory.
        :return: None
        """
        self.items = items

    def get_ItemHandler(self, item):
        """
        Returns an ItemHandler object corresponding to the type of item given.

        :param item: An Item object
        :return: An ItemHandler object
        """
        match item.name:
            case "Aged Brie":
                return AgedBrieItemHandler(item)
            case "Backstage passes to a TAFKAL80ETC concert":
                return BackstagePassesItemHandler(item)
            case "Sulfuras, Hand of Ragnaros":
                return SulfurasItemHandler(item)
            case "Conjured":
                return ConjuredItemHandler(item)
            case _:
                return NormalItemHandler(item)
            
    def update_quality(self):
        """
        Update the quality of all items in the inventory.

        This method iterates over all items in the inventory and calls the UpdateItem method
        of the ItemHandler associated with the item. The ItemHandler is responsible for updating
        the quality and sell-in of the item according to its type and current state.

        :return: None
        """
        for item in self.items:
            itemHandler = self.get_ItemHandler(item)
            itemHandler.UpdateItem()
class Item:
    def __init__(self, name, sell_in, quality):
        """
        Initialize an item with given name, sell-in and quality.

        :param name: The name of the item.
        :param sell_in: The sell-in value of the item.
        :param quality: The quality of the item.
        :return: None
        """
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        """
        Return a string representation of the item, which is in the format of
        "<name>, <sell_in>, <quality>"
        :return: string
        """
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
    
class ItemHandler(ABC):
    def __init__(self, item: Item):
        """
        Initialize the ItemHandler with a given item.
        :param item: An instance of the Item class to be managed by the handler.
        """
        self.item = item

    def increase_quality(self, amount=1):
        """
        Increase the quality of the managed item by the given amount.
        The quality of an item can never be more than 50, so if the item's
        quality after the increase would be more than 50, it will be capped at 50.
        :param amount: The amount to increase the quality by. Defaults to 1.
        :return: None
        """
        self.item.quality = min(self.item.quality + amount, 50)

    def decrease_quality(self, amount=1):
        """
        Decrease the quality of the managed item by the given amount.
        The quality of an item can never be less than 0, so if the item's
        quality after the decrease would be less than 0, it will be capped at 0.
        :param amount: The amount to decrease the quality by. Defaults to 1.
        :return: None
        """
        self.item.quality = max(self.item.quality - amount, 0)

    def decrement_sell_in(self):
        """
        Decrement the sell-in of the managed item by 1.
        This is called by the UpdateItem method of the ItemHandler classes.
        :return: None
        """
        self.item.sell_in -= 1

    # Abstract method - different ItemHandler types which inherit from this class will each update differently
    @abstractmethod
    def UpdateItem(self):
        """
        Abstract method to be implemented by the concrete ItemHandler classes.
        This method is called by the update_quality method of the GildedRose class.
        It should update the quality and sell-in of the managed item according to
        the item's type and current state.
        :return: None
        """
        pass

class NormalItemHandler(ItemHandler):    
    def UpdateItem(self):
        """
        Update the quality and sell-in of a normal item.
        This method decreases the sell-in value by 1. If the sell-in value is less
        than 0, it decreases the quality by 2. Otherwise, it decreases the quality
        by 1. The quality is never allowed to go below 0.
        """
        if self.item.sell_in <= 0:        
            self.decrease_quality(amount=2)
        else:
            self.decrease_quality(amount=1) 
        
        # decrement the sell_in value after the quality calculations
        self.decrement_sell_in()        

class ConjuredItemHandler(ItemHandler):    
    def UpdateItem(self):
        """
        Update the quality and sell-in of a conjured item.
        "Conjured" items degrade in Quality twice as fast as normal items. If the sell-in value is less
        than 0, it decreases the quality by 4. Otherwise, it decreases the quality
        by 2. The quality is never allowed to go below 0.
        """
        if self.item.sell_in <= 0:        
            self.decrease_quality(amount=4)
        else:
            self.decrease_quality(amount=2) 

        self.decrement_sell_in()                

class AgedBrieItemHandler(ItemHandler):
    def UpdateItem(self):        
        """
        Update the quality and sell-in of an Aged Brie item.
        This method increases the quality by 1 and decreases the sell-in value by 1.
        The quality of an item can never be more than 50, so if the quality after the
        increase would be more than 50, it will be capped at 50.
        :return: None
        """
        self.increase_quality()        
        self.decrement_sell_in()

class SulfurasItemHandler(ItemHandler):
    def UpdateItem(self):
        """
        Update the quality and sell-in of a Sulfuras item.
        This method does not make any changes to the quality or sell-in of the item, as
        Sulfuras is a legendary item and as such its Quality is 80 and it never alters.
        Default the sell_in to 0 since the item never has to be sold.
        :return: None
        """
        self.item.quality = 80
        self.item.sell_in = 0

class BackstagePassesItemHandler(ItemHandler):
    def UpdateItem(self): 
        """
        Update the quality and sell-in of a Backstage Passes item.
        This method decreases the sell-in value by 1. If the sell-in value is greater than 0,
        it increases the quality by 3 when there are 5 days or less to the concert, by 2 when
        there are 10 days or less, and by 1 otherwise. If the sell-in value is less than 0, 
        the quality drops to 0. The quality is never allowed to exceed 50.
        :return: None
        """      
        # quality increases by 3 when there are 5 days or less to the concert
        # or quality increases by 2 when there are 10 days or less to the concert
        if self.item.sell_in > 0:
            if self.item.sell_in < 6:            
                self.increase_quality(amount=3)         
            elif self.item.sell_in < 11:
                self.increase_quality(amount=2)
            else:
                self.increase_quality(amount=1)
            

        # quality of the backstage passes to the concert drops to 0 after the concert         
        if self.item.sell_in <= 0:
            self.item.quality = 0

        # decrement the sell_in value after the quality calculations
        self.decrement_sell_in()        