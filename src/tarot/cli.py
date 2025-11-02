"""Small CLI helper to run tarot draws."""
from .tarot import draw


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Tarot CLI")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of cards to draw")
    args = parser.parse_args()
    cards = draw(args.count)
    for c in cards:
        print(f"{c['card']}\n  {c['meaning']}\n")


if __name__ == "__main__":
    main()
