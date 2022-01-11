import logging

from system import OneProcessSystem

logging.basicConfig(format="%(name)-30s %(message)s", level=logging.INFO)

if __name__ == "__main__":
    with OneProcessSystem() as system:
        system.run_simulation()
