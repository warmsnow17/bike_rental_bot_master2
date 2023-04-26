import logging
from client_bot import executor


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

if __name__ == '__main__':
    executor.start_polling(relax=0, timeout=5)
