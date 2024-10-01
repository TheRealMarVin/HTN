import argparse


def main():
    print("Hello World!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Camping Experiment")
    args = parser.parse_args()

    main()