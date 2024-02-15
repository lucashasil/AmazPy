<a name="readme-top"></a>

<h3 align="center">AmazPy</h3>
  <p align="center">
     A Python Based Amazon Product Scraper and Alerting System
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#gui-mode">GUI Mode</a></li>
        <li><a href="#headless-mode">Headless Mode</a></li>
        <li><a href="#formatting-and-linting">Formatting and Linting</a></li>
        <li><a href="#tests">Tests</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## About The Project

This project a Python based Amazon Product Scraper and Price alerting tool.

This tool allows Users to define a number a Amazon product listings which they want to scrape various product information for,
as well as setting up email alerts for when product prices drop below a certain discount threshold.

Furthermore, this project has two different launch modes:
1. GUI Mode - a basic GUI version of the project for better product information visualisation but less alerting functionality
2. Headless Mode - a non-GUI version of the project aimed at users who want longterm scraping with better alerting functionality

Product information is saved to a user's local disk using a basic `SQLite` database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python]][Python-url]
* [![SQLite][SQLite]][SQLite-url]
* [![pytest][pytest]][pytest-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

Getting the project running locally is simple and can be accomplished by following these simple steps.

### Prerequisites

* Python `>= 3.10`
  * This project requires a minimum Python version of `3.10`
* pip
  ```sh
  python -m pip install --upgrade pip
  ```

#### Optional

For email alerting, you are required to provide the tool with email credentials in the form of an environment variable OR an optional command line flag.
The choice on how you'd like to pass the credentials is up you, steps to complete each are as follows:

Both of these steps will require the generation of a Google app password as opposed to passing your email password directly. Instructions on how to generate an app password can be followed at [Google app passwords](https://support.google.com/accounts/answer/185833?hl=en).

* Environment variable:
    1. set an environment variable named `AMAZPY_EMAIL_CREDENTIALS` with value `"<email>:<app_password>"` format
* Command line flag:
    1. simply pass in the correct command line flag with value `--email-credentials=<email>:"<app_password>"`

### Installation

1. Clone the repo to your local drive
   ```sh
   git clone https://github.com/lucashasil/AmazPy.git
   ```
2. Install required pip packages or install AmazPy as a complete package:
    - To run the project directly without installation as a package, run the following:
      ```sh
      pip install -r requirements.txt
      ```
    - Alternatively, to install the project as an entire package, run the following in the project root:
      ```sh
      pip install .
      ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Running this project is simple but will depend on how you decided to install the project requirements in the previous step, as well as which mode you want to run in.

### GUI Mode

If you chose to install the required packages separately, you can launch in GUI mode by running:
```sh
python -m amazpy.main
```

Alternatively, if you installed the project as an entire package, you can simply run:
```sh
amazpy
```

### Headless Mode

Running the project in Headless mode is extremely simple due to the help of command line flags. The only catch here is that you remember to provide email credentials for email alerting (see above for how to do that).

Depending on how you're going to pass your email credentials, the project will be run in one of two ways:

1. With credentials in an environment variable:
    ```sh
    python -m amazpy.main --headless
    ```
    OR
    ```sh
    amazpy --headless
    ```
2. With credentials passed in via a command line flag:
    ```sh
    python -m amazpy.main --headless --email-credentials=<email>"<app_password>"
    ```
    OR
    ```sh
    amazpy --headless --email-credentials=<email>"<app_password>"
    ```

### Formatting and Linting

For development, a number of code formatting and linting tools are used, however these are not installed by default, tools with how they can be installed and run are as follows:

* `Black` for code formatting
    * Install with:
      ```sh
      pip install black
      ```
      And run on the project with:
      ```sh
      black --preview amazpy
      ```
* `Pylint` for static code analysis (linting)
    * Install with:
      ```sh
      pip install pylint
      ```
      And run on the project with:
      ```sh
      pylint amazpy
      ```
* `Mypy` for optional type checking enforcement
    * Install with:
      ```sh
      pip install mypy
      ```
      And run on the project with:
      ```sh
      mypy amazpy
      ```

### Tests

This project includes a number of unit and integration tests implemented with `pytest`. To run all tests, navigate to the root project directory and run:
```sh
pytest .
```

Alternatively feel free to specify specific test files in the `/tests` directory instead of running them all.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See [LICENSE](https://github.com/lucashasil/AmazPy/blob/main/LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[SQLite]: https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://www.sqlite.org/
[pytest]: https://img.shields.io/badge/pytest-323330?style=for-the-badge&logo=testing-library&logoColor=red
[pytest-url]: https://docs.pytest.org/
