from numbers import Number
from typing import Generator, Callable, Any, Iterable, NoReturn


class ArraysManagerAbstract:
    def create(self) -> list:
        raise NotImplementedError

    def delete(self, array_id: int) -> None:
        raise NotImplementedError

    @property
    def objects(self) -> list[list[Number]]:
        raise NotImplementedError


class ArraysManager(ArraysManagerAbstract):
    def __init__(self):
        self._objects: list[list[Number]] = list()

    def create(self, lst: list = None) -> list:
        lst: list = lst or list()
        self._objects.append(lst)
        return lst

    def delete(self, array_id: int) -> None:
        del self._objects[array_id]

    @property
    def objects(self) -> list[list[Number]]:
        return self._objects

    @objects.setter
    def objects(self, a) -> None:
        raise AttributeError('You can not set this attribute')

    @objects.deleter
    def objects(self) -> None:
        raise AttributeError('You can not delete this attribute')

    def is_last_elems_equal(self) -> bool:
        arrays_last_elems: set = set()
        for array in self._objects:
            arrays_last_elems.add(array[-1])

        return len(arrays_last_elems) == 1

    def get_arrays_with_last_elem_gt_len(self) -> Generator:
        for array in self._objects:
            if array[-1] > len(array):
                yield array

    def get_arrays_with_max_elems_sum(self) -> Generator:
        arrays_with_sums: dict = dict(zip(map(sum, self.objects), self.objects))
        max_sum_arrays: filter = filter(lambda item: item[0] == max(arrays_with_sums.keys()),
                                        arrays_with_sums.items())
        for array_sum, array in max_sum_arrays:
            yield array


class MenuAbstract:
    def serve(self) -> None:
        raise NotImplementedError

    def use_option(self, option_key: Any) -> None:
        raise NotImplementedError

    def serve_forever(self) -> NoReturn:
        while True:
            try:
                self.serve()
            except Exception:
                pass


class OptionsRenderer:
    def render(self, options: Iterable):
        raise NotImplementedError


class OptionsOutput:
    def show(self, options: Iterable):
        raise NotImplementedError


class Menu(MenuAbstract):
    def __init__(self, options: list[Callable], arrays_manager: ArraysManagerAbstract, renderer: OptionsRenderer,
                 output: OptionsOutput):
        self._options: list[Callable] = options
        self.arrays_manager: ArraysManagerAbstract = arrays_manager
        self.renderer: OptionsRenderer = renderer
        self.output: OptionsOutput = output

    def get_options(self) -> list[Callable]:
        return self._options

    def use_option(self, option_id: int) -> None:
        self.get_options()[option_id](self.arrays_manager)

    def render_options(self, renderer: OptionsRenderer = None) -> list[str]:
        renderer = renderer or self.renderer
        return renderer.render(self.get_options())

    def show_options(self, output: OptionsOutput = None) -> None:
        output = output or self.output
        output.show(self.render_options())

    def serve(self) -> None:
        self.show_options()
        choice: int = int(input('\n')) - 1

        print('')
        self.use_option(choice)
        print('')


class OptionMetaclass(type):
    options: list[Callable] = list()

    def __new__(cls, *args, **kwargs):
        new_class = super().__new__(cls, *args, **kwargs)
        cls.options.append(new_class())
        return new_class


class Option:
    def __call__(self, array_cls: ArraysManagerAbstract) -> Any:
        raise NotImplementedError

    @property
    def description(self) -> str:
        raise NotImplementedError


class ShowArrays(Option, metaclass=OptionMetaclass):
    description: str = '???????????????? ??????????????'

    def __call__(self, arrays_manager: ArraysManagerAbstract) -> None:
        for array in arrays_manager.objects:
            print(array)


class AddArray(Option, metaclass=OptionMetaclass):
    description: str = '???????????????? ????????????'

    def __call__(self, arrays_manager: ArraysManagerAbstract) -> list:
        array: list = arrays_manager.create()

        inp = input('?????????????? ??????????, ?????????? ???????????????? ?????? ?? ????????????, ?????? ???????????????? "????????", ?????????? ?????????????????? ????????\n')
        while inp.strip().lower() != '????????':
            inp = inp.strip().split()
            for i in inp:
                array.append(int(i))
            inp = input()

        return array


class DeleteArray(Option, metaclass=OptionMetaclass):
    description: str = '?????????????? ????????????'

    def __call__(self, arrays_manager: ArraysManagerAbstract) -> None:
        array_id = int(input('?????????????? ?????????? ??????????????, ?????????????? ???? ???????????? ??????????????\n')) - 1
        arrays_manager.delete(array_id)


class ProcessArrays(Option, metaclass=OptionMetaclass):
    description: str = '???????????????????? ??????????????'

    def __call__(self, arrays_manager: ArraysManager) -> None:
        if arrays_manager.is_last_elems_equal():
            for array in arrays_manager.get_arrays_with_max_elems_sum():
                array.sort()
        else:
            for array in arrays_manager.get_arrays_with_last_elem_gt_len():
                while 0 in array:
                    array.remove(0)


class RendererToStrs(OptionsRenderer):
    def render(self, options: Iterable[Option]) -> list[str]:
        result: list[str] = []
        for i, option in enumerate(options):
            result.append(f"{i+1}) {option.description}")

        return result


class ConsoleOutput(OptionsOutput):
    def show(self, options: Iterable[str]):
        for i in options:
            print(i)


def main():
    menu = Menu(OptionMetaclass.options, ArraysManager(), RendererToStrs(), ConsoleOutput())
    menu.serve_forever()


if __name__ == '__main__':
    main()
