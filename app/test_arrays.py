import unittest
from functools import partial
from typing import Generator, Callable
from unittest.mock import patch, MagicMock, call

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


class TestMenu(unittest.TestCase):
    def setUp(self) -> None:
        self.menu = arrays.Menu(
            options=MagicMock(list),
            arrays_manager=MagicMock(arrays.ArraysManager()),
            renderer=MagicMock(arrays.RendererToStrs()),
            output=MagicMock(arrays.ConsoleOutput()),
        )

    def test_get_options(self):
        self.assertIsInstance(self.menu.get_options(), list)

    def test_use_option(self):
        with patch.object(self.menu,
                          '_options',
                          [MagicMock(arrays.Option) for _ in range(3)]
        ):
            self.menu.use_option(0)
            self.menu._options[0].assert_called_once()

            with self.assertRaises(IndexError):
                self.menu.use_option(len(self.menu.get_options()))

    def test_render_options(self):
        self.menu.render_options()
        self.menu.renderer.render.assert_called_once()

        renderer: MagicMock = MagicMock(arrays.OptionsRenderer)
        self.menu.render_options(renderer)
        renderer.render.assert_called_once_with(self.menu.get_options())

    def test_show_options(self):
        self.menu.show_options()

        self.menu.renderer.render.assert_called_once()
        self.menu.output.show.assert_called_once_with(self.menu.render_options())

        self.menu.output.reset_mock()
        self.menu.renderer.render.reset_mock()

        options_list: list = [
            'First',
            'Second',
            'Third',
        ]

        self.menu._options = options_list

        self.menu.show_options()

        self.menu.renderer.render.assert_called_once_with(options_list)
        self.menu.output.show.assert_called_once()

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('app.arrays.Menu.use_option')
    @patch('app.arrays.Menu.show_options')
    def test_serve(self, show_options_mock: MagicMock, use_option_mock: MagicMock, print_mock: MagicMock, input_mock: MagicMock):
        self.menu.serve()

        input_mock.assert_called_once()
        show_options_mock.assert_called_once()
        use_option_mock.assert_called_once_with(0)


class TestOptionMetaclass(unittest.TestCase):
    def setUp(self) -> None:
        self.metaclass = arrays.OptionMetaclass
        self.metaclass.options = MagicMock(spec=list)

    def test_new(self):
        class Test(metaclass=self.metaclass):
            pass

        self.metaclass.options.append.assert_called_once()


class TestDeleteArray(unittest.TestCase):
    def setUp(self) -> None:
        self.option = arrays.DeleteArray()
        self.manager = MagicMock(arrays.ArraysManager)

    @patch('builtins.input')
    def test_delete(self, input_mock: MagicMock):
        self.option(self.manager)

        self.manager.delete.assert_called_once_with(0)


class TestShowArrays(unittest.TestCase):
    def setUp(self) -> None:
        self.option = arrays.ShowArrays()
        self.manager = MagicMock(arrays.ArraysManager)

    @patch('builtins.print')
    def test_show_arrays(self, print_mock: MagicMock):
        with patch.object(self.manager, 'objects', [1, 2]):
            self.option(self.manager)

            self.assertEqual(print_mock.call_args_list, [call(1), call(2)])


class TestAddArray(unittest.TestCase):
    def setUp(self) -> None:
        self.option = arrays.AddArray()
        self.manager = MagicMock(arrays.ArraysManager)

    @patch('builtins.input', return_value='стоп')
    def test_add_array(self, input_mock: MagicMock):
        self.option(self.manager)
        self.manager.create.assert_called_once_with()


class TestProcessArrays(unittest.TestCase):
    def setUp(self) -> None:
        self.option = arrays.ProcessArrays()
        self.manager = MagicMock(arrays.ArraysManager())

    def test_process_arrays(self):
        arrs: list[MagicMock] = [MagicMock(list) for _ in range(3)]
        self.manager.get_arrays_with_max_elems_sum.return_value = arrs
        self.manager.is_last_elems_equal.return_value = True

        self.option(self.manager)

        for arr in arrs:
            arr.sort.assert_called_once()

        arrs: list[list[int]] = [
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 3]
        ]
        self.manager.get_arrays_with_last_elem_gt_len.return_value = arrs
        self.manager.is_last_elems_equal.return_value = False

        self.option(self.manager)

        for arr in arrs:
            self.assertNotIn(0, arr)


class TestRendererToStrs(unittest.TestCase):
    def setUp(self) -> None:
        self.renderer = arrays.RendererToStrs()
        self.option = MagicMock(arrays.Option)
        self.option.description.return_value = "Description"

    def test_render(self):
        options_count: int = 3

        options: list[MagicMock] = [self.option() for _ in range(options_count)]
        rendered_options: list[str] = self.renderer.render(options)

        self.assertEqual(len(rendered_options), options_count)


class TestConsoleOutput(unittest.TestCase):
    def setUp(self) -> None:
        self.output = arrays.ConsoleOutput()

    @patch('builtins.print')
    def test_show(self, print_mock: MagicMock):
        options: list[str] = [
            '1) Description',
            '2) Description',
            '3) Description',
        ]

        self.output.show(options)

        self.assertEqual(print_mock.call_args_list, [call(i) for i in options])


if __name__ == '__main__':
    unittest.main()
