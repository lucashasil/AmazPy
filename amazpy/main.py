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
        help="Whether to run the app in headless mode or not.",
    )

    parser.add_argument(
        "--email-credentials",
        dest="email_credentials",
        action="store",
        help=(
            "The email address and it's application password used to send and receive"
            " emails. This should be supplied in <email>:<password> format."
        ),
    )

    args = parser.parse_args()

    if args.headless:
        headless = Headless(args.email_credentials)
    else:
        app = App()
        app.mainloop()
