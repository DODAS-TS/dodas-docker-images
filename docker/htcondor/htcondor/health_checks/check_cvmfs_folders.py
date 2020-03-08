#!/usr/bin/env python
import os


def main():
    try:
        for folder in os.listdir("/cvmfs"):
            os.listdir(os.path.join("/cvmfs", folder))
    except OSError as err:
        if err.errno == 107:  # transport endpoint is not connected
            return 1
    return 0


if __name__ == '__main__':
    exit(main())
