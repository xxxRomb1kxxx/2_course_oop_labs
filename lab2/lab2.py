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
    def __init__(
        self,
        color: Color,
        position: Tuple[int, int],
        symbol: str,
        font: Font,
        scale: int = 1
    ) -> None:
        self.color = color
        self.position = position
        self.symbol = symbol
        self.font = font
        self.scale = scale
        self.reset_console()

    @staticmethod
    def reset_console() -> None:
        print("\033[0m", end='')

    def scale_line(self, line: str) -> list[str]:
        scaled = []
        for _ in range(self.scale):
            scaled_line = ''
            for ch in line:
                scaled_line += (self.symbol if ch == '*' else ' ') * self.scale
            scaled.append(scaled_line)
        return scaled

    def print(self, text: str) -> None:
        y, x = self.position
        output_lines = []
        for line_idx in range(5):
            line_parts = []
            for char in text:
                lines = self.font.get_char(char)
                if line_idx < len(lines):
                    scaled = self.scale_line(lines[line_idx])
                    line_parts.append(scaled)
            if line_parts:
                for row_offset in range(self.scale):
                    combined = "  ".join(part[row_offset] for part in line_parts)
                    output_lines.append(combined)

        for i, line in enumerate(output_lines):
            print(f"\033[{y + i};{x}H\033[{self.color.value}m{line}\033[0m")

    def __enter__(self) -> 'Printer':
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[object]) -> None:
        self.reset_console()

    @classmethod
    def print_static(
        cls,
        text: str,
        color: Color,
        position: Tuple[int, int],
        symbol: str,
        font: Font,
        scale: int = 1
    ):
        with cls(color, position, symbol, font, scale) as printer_instance:
            printer_instance.print(text)


if __name__ == "__main__":
    loaded_font = Font("letters.txt")

    Printer.print_static("AB", Color.RED, (10, 10), "*", loaded_font, scale=2)

    with Printer(Color.GREEN, (20, 10), "#", loaded_font, scale=10) as printer:
        printer.print("HELLO")
