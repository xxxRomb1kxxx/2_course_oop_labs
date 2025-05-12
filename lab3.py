import re
from typing import List, Protocol


class LogFilterProtocol(Protocol):
    def match(self, text: str) -> bool:
        pass


class LogHandlerProtocol(Protocol):
    def handle(self, text: str) -> None:
        pass


class SimpleLogFilter:
    def __init__(self, pattern: str):
        self.pattern = pattern

    def match(self, text: str) -> bool:
        return self.pattern in text


class ReLogFilter:
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)

    def match(self, text: str) -> bool:
        return bool(self.pattern.search(text))


class ConsoleHandler:
    def handle(self, text: str) -> None:
        print(f"CONSOLE: {text}")


class FileHandler:
    def __init__(self, filename: str):
        self.filename = filename

    def handle(self, text: str) -> None:
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(f"{text}\n")


class SocketHandler:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def handle(self, text: str) -> None:
        print(f"[MOCK SOCKET] Лог отправлен: {text}")


class SyslogHandler:
    def __init__(self, facility: str = "user"):
        self.facility = facility

    def handle(self, text: str) -> None:
        print(f"SYSLOG ({self.facility}): {text}")


class Logger:
    def __init__(self, filters: List[LogFilterProtocol], handlers: List[LogHandlerProtocol]) -> None:
        self.filters = filters
        self.handlers = handlers

    def log(self, text: str) -> None:
        for log_filter in self.filters:
            if not log_filter.match(text):
                return

        for handler in self.handlers:
            handler.handle(text)


if __name__ == "__main__":
    error_filter = SimpleLogFilter("ERROR")
    warn_filter = SimpleLogFilter("WARN")
    http_filter = ReLogFilter(r"HTTP/\d\.\d")
    console_handler = ConsoleHandler()
    file_handler = FileHandler("app.log")
    socket_handler = SocketHandler("localhost", 12345)
    syslog_handler = SyslogHandler()

    error_logger = Logger(filters=[error_filter], handlers=[console_handler, file_handler, syslog_handler])
    warn_logger = Logger(filters=[warn_filter], handlers=[console_handler, file_handler])
    http_logger = Logger(filters=[http_filter], handlers=[socket_handler])

    print("=== Testing error logger ===")
    error_logger.log("ERROR: Database connection failed")
    error_logger.log("WARN: Disk space low")

    print("\n=== Testing warn logger ===")
    warn_logger.log("WARN: Memory usage high")
    print("\n=== Testing HTTP logger ===")
    http_logger.log("HTTP/1.1 GET /index.html")
    http_logger.log("TCP connection established")
