## BorsdataAPI
Our simple Python console test client to get a quick start with Börsdata API.
[More details about API is found here](https://github.com/Borsdata-Sweden/API)

## Api Key
If you dont have an API Key, you need to Apply for an API key on [Börsdata webbpage](https://borsdata.se/).
You need to be a Pro member to get Access to API.

## Installation
Python 3+ needed!
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.
```bash
pip3 install -r requirements.txt
```

## How to get started with Client
Download project and run it from a terminal or any Python-IDE [PyCharm](https://www.jetbrains.com/pycharm/).
In constants.py you replace xxxx with your unique API Key.
Run borsdata_client.py (or excel_exporter.py)

## Database updater
A local installation of MySQL is needed, see instructions [here](https://www.dataquest.io/blog/install-mysql-windows/).
Set your MySQL-credentials in [constants.py](borsdata/constants.py) and your preferred database name. Port is assumed to be the standard one (3306).
Run the [database_updater.py](borsdata/database_updater.py) script and make sure to remove the **create_database** call after first run (it can't create the database again).

If you're using a data-exploration tool such as MySQL-workbench don't forget to right click your schemas and "refresh all" to get your newly created
database to appear.

Both of the updating functions utilizes the new "list-calls" which is less time consuming and is rather fast, it will take a few minutes if you make a dry run (grabbing all the data). After that you can use the function parameters to limit the daily updates.

## Database API
Examples on how to retrieve data from the created MySQL database are shown in [database_api.py](borsdata/database_api.py).
Run the file and explore the functions!

## License
[MIT](https://choosealicense.com/licenses/mit/)
