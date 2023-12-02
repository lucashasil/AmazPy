"""Handle the main entry point for the application."""
import argparse
import os
import sys

from amazpy.app import App
from amazpy.headless import Headless


def main():
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
            "The email address and it's application password used to send and"
            " receive emails. This should be supplied in <email>:<password>"
            " format."
        ),
    )

    # Parse command line arguments
    args = parser.parse_args()

    # Run the application in appropriate mode based on (optional) input flag
    if args.headless:
        # If the application is running in headless mode, we need to ensure that
        # email credentials are supplied OR available elsewhere (env var)
        email_credentials = args.email_credentials

        # Try and fetch email credentials from an environment variable if they are not supplied
        # via flag
        if email_credentials is None:
            _email_credentials = os.environ.get("AMAZPY_EMAIL_CREDENTIALS")

            # Update variable if we found a value for the environment variable
            if _email_credentials is not None:
                email_credentials = _email_credentials
            else:
                sys.exit(
                    "Please supply email credentials via the --email-credentials flag"
                    " or AMAZPY_EMAIL_CREDENTIALS environment variable."
                )

        Headless(email_credentials)
    else:
        # Otherwise just run the GUI application
        app = App()
        app.mainloop()


if __name__ == "__main__":
    main()
