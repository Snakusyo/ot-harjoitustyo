
import unittest
from game import StrategyGame

class TestStrategyGame(unittest.TestCase):

    def setUp(self):

        self.camera_position = [10,10]
        self.mapdata = [[0,0,0,0], [0,1,1,0], [0,1,1,0], [0,0,0,0]]

    def test_map_is_correct_length(self):

        map = StrategyGame.create_map(self.mapdata)
        self.assertEqual(len(map), self.mapdata)


