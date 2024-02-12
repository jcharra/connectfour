import unittest
from main import App


class TestMyModule(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def test_winner_diagonal_asc_1(self):
        self.app.fields = [[0, 0, 0, 0, 0, 0, 1],
                           [0, 0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(self.app.check_winner(), [
                         (3, 3), (2, 4), (1, 5), (0, 6)])

    def test_winner_diagonal_asc_2(self):
        self.app.fields = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 2, 0, 0, 0],
                           [0, 0, 2, 0, 0, 0, 0],
                           [0, 2, 0, 0, 0, 0, 0],
                           [2, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(self.app.check_winner(), [
                         (5, 0), (4, 1), (3, 2), (2, 3)])

    def test_winner_diagonal_desc_1(self):
        self.app.fields = [[1, 0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0, 0],
                           [0, 0, 1, 0, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(self.app.check_winner(), [
                         (0, 0), (1, 1), (2, 2), (3, 3)])

    def test_winner_diagonal_desc_2(self):
        self.app.fields = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 2, 0, 0, 0],
                           [0, 0, 0, 0, 2, 0, 0],
                           [0, 0, 0, 0, 0, 2, 0],
                           [0, 0, 0, 0, 0, 0, 2]]
        self.assertEqual(self.app.check_winner(), [
                         (2, 3), (3, 4), (4, 5), (5, 6)])

    def test_winner_row_1(self):
        self.app.fields = [[0, 0, 0, 1, 1, 1, 1],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(self.app.check_winner(), [
                         (0, 3), (0, 4), (0, 5), (0, 6)])

    def test_winner_row_2(self):
        self.app.fields = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [2, 2, 2, 2, 0, 0, 0]]
        self.assertEqual(self.app.check_winner(), [
                         (5, 0), (5, 1), (5, 2), (5, 3)])

    def test_winner_column_1(self):
        self.app.fields = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(self.app.check_winner(), [
                         (2, 0), (3, 0), (4, 0), (5, 0)])

    def test_winner_column_2(self):
        self.app.fields = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 2],
                           [0, 0, 0, 0, 0, 0, 2],
                           [0, 0, 0, 0, 0, 0, 2],
                           [0, 0, 0, 0, 0, 0, 2]]
        self.assertEqual(self.app.check_winner(), [
                         (2, 6), (3, 6), (4, 6), (5, 6)])

    def test_no_winner_yet(self):
        self.app.fields = [[0, 2, 1, 2, 1, 2, 1],
                           [1, 2, 1, 1, 1, 2, 1],
                           [2, 1, 2, 1, 2, 1, 2],
                           [2, 1, 2, 1, 2, 1, 2],
                           [1, 2, 1, 2, 1, 2, 1],
                           [1, 2, 1, 1, 1, 2, 1]]
        self.assertEqual(self.app.check_winner(), None)
        self.assertFalse(self.app.board_full())

    def test_draw(self):
        self.app.fields = [[1, 2, 1, 2, 1, 2, 1],
                           [1, 2, 1, 1, 1, 2, 1],
                           [2, 1, 2, 1, 2, 1, 2],
                           [2, 1, 2, 1, 2, 1, 2],
                           [1, 2, 1, 2, 1, 2, 1],
                           [1, 2, 1, 1, 1, 2, 1]]
        self.assertEqual(self.app.check_winner(), None)
        self.assertTrue(self.app.board_full())


if __name__ == '__main__':
    unittest.main()
