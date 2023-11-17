import argparse
from amazpy.app import App
from amazpy.headless import Headless

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="A Python based Amazon price tracker and scraper."
    )

    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        required=False,
        help="Whether to run the app in headless mode or not.",
    )

    args = parser.parse_args()

    if args.headless:
        headless = Headless()
    else:
        app = App()
        app.mainloop()
