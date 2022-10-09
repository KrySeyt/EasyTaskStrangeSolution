import unittest
from functools import partial
from typing import Generator
from unittest.mock import patch

from app import arrays


class TestArraysManager(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = arrays.ArraysManager()
        self.mock_objects = partial(patch.object, self.manager, '_objects')

    def test_objects(self):
        with self.assertRaises(AttributeError):
            self.manager.objects = []

        with self.assertRaises(AttributeError):
            del self.manager.objects

    def test_create(self):
        with self.mock_objects(list()):
            obj_count: int = len(self.manager.objects)
            array: list

            self.assertIsInstance(array := self.manager.create(), list)
            self.assertEqual(len(self.manager.objects), obj_count + 1)
            self.assertIs(self.manager.objects[-1], array)

    def test_delete(self):
        with self.mock_objects([
            list(),
            list(),
            list(),
        ]):
            self.manager.delete(0)

            self.assertEqual(len(self.manager.objects), 2)
            self.assertEqual(self.manager.objects, [list(), list()])

            self.manager.delete(1)

            self.assertEqual(self.manager.objects, [list()])

    def test_is_last_elems_equal(self):
        with self.mock_objects(list()) as mocked_objects:
            mocked_objects.extend([
                [1, 2, 3],
                [0, 4, 3],
                [6, 18, 3],
            ])

            self.assertTrue(self.manager.is_last_elems_equal())

            mocked_objects.clear()
            mocked_objects.extend([
                [1, 2, 0],
                [0, 4, 5],
                [6, 18, 10],
            ])

            self.assertFalse(self.manager.is_last_elems_equal())

    def test_get_arrays_with_last_elem_gt_len(self):
        with self.mock_objects([
            [1, 3, 10],
            [15, 5, 8],
            [1, 0, 1],
        ]):

            for array in self.manager.get_arrays_with_last_elem_gt_len():
                self.assertGreater(array[-1], len(array))

    def test_get_arrays_with_max_elems_sum(self):
        with self.mock_objects([
            [1, 3, 10],
            [15, 5, 8],
            [1, 0, 1],
        ]):

            gen: Generator = self.manager.get_arrays_with_max_elems_sum()

            self.assertEqual(next(gen), [15, 5, 8])


if __name__ == '__main__':
    unittest.main()
