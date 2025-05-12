from enum import Enum
from typing import Tuple, Optional


class Color(Enum):
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 0


class Font:
    def __init__(self, font_file: str) -> None:
        self.font_map = self.load_font(font_file)

    @staticmethod
    def load_font(font_file: str) -> dict[str, list[str]]:
        font_map = {}
        with open(font_file, 'r') as f:
            letter = ''
            lines = f.read().splitlines()
            for line in lines:
                if line.endswith(':'):
                    letter = line[:-1]
                    font_map[letter] = []
                elif letter:
                    font_map[letter].append(line)
        return font_map

    def get_char(self, char: str) -> list[str]:
        return self.font_map.get(char.upper(), [])


class Printer:
    def __init__(self, color: Color, position: Tuple[int, int], symbol: str, font: Font) -> None:
        self.color = color
        self.position = position
        self.symbol = symbol
        self.font = font
        self.reset_console()

    @staticmethod
    def reset_console() -> None:
        print("\033[0m", end='')

    def print(self, text: str) -> None:
        y, x = self.position
        for line_idx in range(5):
            line = ""
            for char in text:
                lines = self.font.get_char(char)
                if line_idx < len(lines) and lines[line_idx]:
                    line += lines[line_idx].replace("*", self.symbol) + "  "
            if line:  # Only print if line is not empty
                print(f"\033[{y + line_idx};{x}H\033[{self.color.value}m{line}\033[0m")

    def __enter__(self) -> 'Printer':
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[object]) -> None:
        self.reset_console()

    @classmethod
    def print_static(cls, text: str, color: Color, position: Tuple[int, int], symbol: str, font: Font):
        with cls(color, position, symbol, font) as printer_instance:  # Changed name to avoid shadowing
            printer_instance.print(text)


if __name__ == "__main__":
    loaded_font = Font("letters.txt")

    Printer.print_static("ABRRTERYEYEY"
                         "OBA", Color.RED, (10, 10), "*", loaded_font)

    with Printer(Color.GREEN, (10, 10), "#", loaded_font) as printer:
        printer.print("HELLO")