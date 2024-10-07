from decouple import config

from controller import Controller
from db import TABLES, MySqlConnector
from models import ProductFactory
from repositories import MySQLProductRepository
from views import CLIView


def main():
    connector_options = {
        "conf": config,
        "table_definitions": TABLES,
    }
    connector = MySqlConnector(**connector_options)
    connector.create_database(config("DB_NAME"))  # Create database if it doesn't exist
    connector.create_tables()  # Create tables if they don't exist
    repository = MySQLProductRepository(connector)
    view = CLIView()
    product_factory = ProductFactory()
    controller = Controller(repository=repository, view=view, product_factory=product_factory)
    controller.run()


if __name__ == "__main__":
    main()
