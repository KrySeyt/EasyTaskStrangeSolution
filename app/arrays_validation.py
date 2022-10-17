import re


def clear_array(array: str) -> list[int | float]:
    return re.findall(r'-?\d+\.\d+|\d+', array)


def main():
    clear_array('2fghfgdhfg53hdfg2.16543654654fghfghfg2hfgh')


if __name__ == '__main__':
    main()
