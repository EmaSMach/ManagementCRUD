# CRUD: Products management v0.1.0

## Description:

This is a simple application to perform CRUD operations on products. It is written in python.
It attempts to make it easy to switch the storage option in the future.
It has a console interface for the moment (CLI), but I want to add a GUI later.

## Requirements:

Written in python version 3.12. It may also work with older python versions.

## Setup:

Even though it does not have specific requirements, it is always a good idea to create a virtual environment:

For linux:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
. ./venv/bin/activate
```

## Environment variables and other necessary data
Create a .env file with the following lines and values to make it possible to connect to the database (MySql):
```
DB_HOST=<your_db_host>
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_NAME=<your_db_name>
DB_PORT=<your_db_port>
```
Place it in the root folder of the project.

You can create the database and execute the `create_tables.sql` script, or just supply a user with enough privileges in the `.env` file, the app will create the database and the tables for you.
## Usage:

```bash
python main.py
```
