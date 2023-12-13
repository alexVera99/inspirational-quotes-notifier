from datetime import datetime


class Logger:
    filename = "log.txt"

    def write_to_log_file(self, message: str) -> None:
        my_file = open(self.filename, "a")

        today_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        message = today_datetime + ":\n" + message
        my_file.write(message + "\n\n")

        my_file.close()


def main() -> None:
    logger = Logger()

    logger.write_to_log_file("Mum! I'm writing to a file :PP")


if __name__ == "__main__":
    main()
