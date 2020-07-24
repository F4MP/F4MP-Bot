import contextlib
import logging

from F4MPBot.bot import F4MPBot


@contextlib.contextmanager
def setup_logging():
    try:
        # __enter__
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)

        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = logging.FileHandler(filename="F4MPBot.log", encoding="utf-8", mode="w")
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        fmt = logging.Formatter("[{asctime}] [{levelname:<7}] {name}: {message}", dt_fmt, style="{")
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        # __exit__
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)


def main():
    with setup_logging():
        bot = F4MPBot()
        bot.run()

if __name__ == '__main__':
    main()