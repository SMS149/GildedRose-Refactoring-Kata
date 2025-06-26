# -*- coding: utf-8 -*-
import unittest

# from gilded_rose import Item, GildedRose
from gilded_rose.gilded_rose import Item, GildedRose

class GildedRoseTest(unittest.TestCase):

    def setUp(self):
        """
        Runs before each test to print the name of the test, and allows us to
        inspect the current state of the test before it runs.
        """
        print(f"\n🔎 Running: {self.__class__.__name__}.{self._testMethodName}")

    def tearDown(self):
        print(f"✅ Finished: {self.__class__.__name__}.{self._testMethodName}")

    def test_item_naming_is_successful(self):
        # set up an Item with its sell_in and quality values
        """
        Test the update_quality method for a basic item.

        This test initializes an item with name "anything", sell_in of 0, and quality of 0.
        After updating the quality using the GildedRose class, it verifies that
        the name of the item has not changed to "fixme".
        """
        # Set up item
        items = [Item("anything", 0, 0)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("anything", items[0].name, "test_item_naming name should be anything")

    def test_update_quality_sell_in_greaterthanzero_is_successful(self):       
        """
        Test the update_quality method for an item with positive sell_in and quality.
        This test initializes an item with name "anything", sell_in of 1, and quality of 1.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item changes from its initial value.
        """
        items = [Item(name="anything", sell_in=1, quality=1)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertNotEqual(1, items[0].quality, "test_update_quality_sell_in_greaterthanzero quality should decrease from 1 to 0")   
        self.assertEqual(0, items[0].quality, "test_update_quality_sell_in_greaterthanzero quality should decrease from 1 to 0")   

    def test_quality_never_negative_is_successful(self):       
        """
        Test the update_quality method to ensure item quality is never negative.

        This test initializes an item with name "anything", sell_in of 0, and quality of 1.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item decreases to 0 and does not become negative
        even though a sell_in value of 0 means the quality will degrade by double the amount, ie 2.
        """
        items = [Item(name="anything", sell_in=0, quality=1)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertNotEqual(-1, items[0].quality, "test_quality_never_negative_is_successful quality should decrease from 1 to 0, not -1")   
        self.assertEqual(0, items[0].quality, "test_quality_never_negative_is_successful quality should decrease from 1 to 0 when sell_in is 0")


    def test_update_quality_sellinequaltozero_is_successful(self):       
        """
        Test the update_quality method for an item whose sell_in is equal to 0.

        This test initializes an item with name "past_sellin", sell_in of 0, and quality of 10.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item decreases by 2.
        """
        # set up an Item with its sell_in and quality values
        initial_quality = 10
        items = [Item(name="past_sellin", sell_in=0, quality=initial_quality)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertEqual(initial_quality-2, items[0].quality, "test_update_quality_sellinequaltozero quality should decrease from 10 to 8")

    def test_brie_quality_increase_is_successful(self):        
        """
        Test the update_quality method for Aged Brie.

        This test initializes an item with name "Aged Brie", sell_in of 5, and quality of 10.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item increases.
        """
        # set up an Item with its sell_in and quality values
        items = [Item(name="Aged Brie", sell_in=5, quality=10)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
                
        self.assertGreater(items[0].quality, 10, "test_brie_quality_increase quality should increase from 10 to 11")
        self.assertEqual(items[0].quality, 11, "test_brie_quality_increase quality should increase from 10 to 11")

    def test_Backstage_passes_not_exceeds_50_is_successful(self):               
        """
        Test the update_quality method for Backstage passes to a TAFKAL80ETC concert.
        This test initializes an item with name "Backstage passes to a TAFKAL80ETC concert", sell_in of 5, and quality of 50.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item does not exceed 50.
        """
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=50)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()       
        
        self.assertEqual(items[0].sell_in, 4, "test_Backstage_passes_not_exceeds_50 sell_in should be 4")
        self.assertEqual(items[0].quality, 50, "test_Backstage_passes_not_exceeds_50 quality should be 50")

    def test_Backstage_passes_quality_0_after_concert_is_successful(self):               
        """
        Test the update_quality method for Backstage passes to a TAFKAL80ETC concert that are past their sell date.
        This test initializes an item with name "Backstage passes to a TAFKAL80ETC concert", sell_in of 0, and quality of 10.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item is set to 0.
        """
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=10)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()       
        
        self.assertEqual(items[0].quality, 0, "test_Backstage_passes_quality_0_after_concert_quality should be 0 when sell_in is 0 or under")

    def test_Backstage_passes_quality_increases_correctly_when_sell_in_is_5_is_successful(self):               
        """
        Test the update_quality method for Backstage passes to a TAFKAL80ETC concert with 5 days to sell and initial quality of 2.
        This test initializes an item with name "Backstage passes to a TAFKAL80ETC concert", sell_in of 5, and quality of 2.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item increases by 3.
        """
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=2)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()       
        
        self.assertEqual(items[0].sell_in, 4, "test_Backstage_passes_quality_increases_correctly_when_sell_in_is_5 sell_in should be 4")
        self.assertEqual(items[0].quality, 5, "test_Backstage_passes_quality_increases_correctly_when_sell_in_is_5 quality should be 5 when sell_in is 5 or under")

    def test_Backstage_passes_quality_increases_correctly_when_sell_in_is_9_is_successful(self):               
        """
        Test the update_quality method for Backstage passes to a TAFKAL80ETC concert with 10 days to sell and initial quality of 2.
        This test initializes an item with name "Backstage passes to a TAFKAL80ETC concert", sell_in of 9, and quality of 2.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item increases by 2.
        """
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=9, quality=2)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()       
        
        self.assertEqual(items[0].sell_in, 8, "test_Backstage_passes_quality_increases_correctly_when_sell_in_is_9 sell_in should be 8")
        self.assertEqual(items[0].quality, 4, "test_Backstage_passes_quality_increases_correctly_when_sell_in_is_9 quality should be 4 when sell_in is 10 or under")

    def test_quality_never_greater_than_50_successful(self):               
        """
        Test the update_quality method for an item whose quality is 50.
        This test initializes an item with name "Aged Brie", sell_in of 5, and quality of 50.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item does not exceed 50.
        """
        items = [Item(name="Aged Brie", sell_in=5, quality=50)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
                
        self.assertLessEqual(items[0].sell_in, 50, "test_quality_never_greater_than_50 sell_in should be < 50")  # Asserts that a <= b

    def test_quality_never_less_than_0_successful(self):
        """
        Test the update_quality method for an item whose quality is 50.
        This test initializes an item with name "Aged Brie", sell_in of 5, and quality of 50.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item does not exceed 50.
        """
        items = [Item(name="Aged Brie", sell_in=5, quality=50)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
                
        self.assertLessEqual(items[0].sell_in, 50, "test_quality_never_greater_than_50 sell_in should be < 50")  # Asserts that a <= b

    def test_Sulfuras_is_80_successful(self):               

        # "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches;
        # Quality increases by 2 when there are 10 days or less and by 3 when there are 5 days or less but
        # Quality drops to 0 after the concert
        # set up an Item with its sell_in and quality values
        items = [Item(name="Sulfuras, Hand of Ragnaros", sell_in=5, quality=10)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
                
        self.assertEqual(items[0].sell_in, 0, "test_Sulfuras_is_80 sell_in should be 0, it never has to be sold ")
        self.assertEqual(items[0].quality, 80, "test_Sulfuras_is_80 quality should always be 80")

    def test_update_quality_conjured_is_double_is_successful(self):       
        """
        Test the update_quality method for Conjured items.

        This test initializes an item with name "Conjured", sell_in of 15, and quality of 30.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item decreases by 2, twice as fast as normal items.
        """
        items = [Item(name="Conjured", sell_in=15, quality=30)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertNotEqual(29, items[0].quality, "test_update_quality_conjured_is_double quality should decrease from 30 to 28")
        self.assertEqual(28, items[0].quality, "test_update_quality_conjured_is_double quality should decrease from 30 to 28")   

    def test_update_quality_conjured_is_double_when_sell_in_is_0_is_successful(self):       
        """
        Test the update_quality method for Conjured items when sell_in is 0.

        This test initializes an item with name "Conjured", sell_in of 0, and quality of 30.
        After updating the quality using the GildedRose class, it verifies that
        the quality of the item decreases by 4, twice as fast as normal items, since it has expired.
        """
        items = [Item(name="Conjured", sell_in=0, quality=30)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        
        self.assertEqual(26, items[0].quality, "test_update_quality_conjured_is_double_when_sell_in_is_0 quality should decrease from 30 to 26")  

    def test_Conjured_quality_never_less_than_0_is_successful(self):               
        items = [Item(name="Conjured", sell_in=0, quality=3)]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()       
        
        self.assertEqual(items[0].quality, 0, "test_Conjured_quality_never_less_than_0 quality should be 0 when sell_in is 0 or under")


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GildedRoseTest)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    print("\n=== Test Summary ===")
    print(f"Total tests run     : {result.testsRun}")
    print(f"Failures            : {len(result.failures)}")
    print(f"Errors              : {len(result.errors)}")
    print(f"Successful tests    : {result.testsRun - len(result.failures) - len(result.errors)}")