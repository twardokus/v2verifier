import argparse
import os

from Local import Local
from Remote import Remote

if __name__ == "__main__":

    if os.geteuid() != 0:
        raise Exception("Error - you must be root! Try running with sudo")

    description = "Run a V2V security experiment using V2Verifier."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("perspective",
                        help="choice of perspective",
                        choices=["local", "remote"]
                        )

    args = parser.parse_args()

    if args.perspective == "local":
        program = Local()
        program.run_local()

    elif args.perspective == "remote":
        program = Remote()
        program.run_remote()