import json
from abc import ABC, abstractmethod

from db.connectors import MySqlConnector
from loggers import logger
from models import BaseProduct, ProductFactory


class ProductNotFoundError(Exception):
    pass


class BaseProductRepository(ABC):
    def __init__(self, storage, *args, **kwargs):
        self.storage = storage

    @abstractmethod
    def add(self, product):
        raise NotImplementedError

    @abstractmethod
    def get(self, product_id: int | str) -> BaseProduct | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> dict[str, BaseProduct]:
        raise NotImplementedError

    @abstractmethod
    def update(self, product: BaseProduct):
        raise NotImplementedError

    @abstractmethod
    def delete(self, product_id: int | str):
        raise NotImplementedError

    @staticmethod
    def get_product_types():
        return BaseProduct.get_product_types()


class ListProductRepository(BaseProductRepository):
    """Simple repository that stores products in a list"""

    def __init__(self, storage: list | None = None, *args, **kwargs):
        if storage is None:
            storage = []
        super().__init__(storage, *args, **kwargs)
        self.storage: list[dict]

    def add(self, product: BaseProduct):
        self.storage.append(product.to_dict())

    def get(self, product_id: int | str) -> BaseProduct | None:
        product_data = next((p for p in self.storage if p["code"] == product_id), None)
        if product_data:
            return self._deserialize_product(product_data)
        else:
            return None

    def list(self) -> dict[str, BaseProduct]:
        """Return a dictionary with the products indexed by code"""
        return {p["code"]: self._deserialize_product(p) for p in self.storage}

    def update(self, product: BaseProduct):
        product_to_update = self.get(product.code)
        if product_to_update:
            for product_dict in self.storage:
                if product_dict["code"] == product.code:
                    product_dict["name"] = product.name
                    product_dict["price"] = product.price
                    product_dict["description"] = product.description
                    product_dict["stock"] = product.stock
                    product_dict["available"] = product.available
        else:
            raise ValueError(f"Product with code {product.code} not found")

    def delete(self, product_id: int | str):
        product_to_delete = self.get(product_id)
        if product_to_delete:
            for product in self.storage:
                if product["code"] == product_id:
                    self.storage.remove(product)
        else:
            raise ValueError(f"Product with code {product_id} not found")

    def __str__(self):
        return f"ListProductRepository({self.storage})"

    def _serialize_product(self, product: BaseProduct):
        return product.to_dict()

    def _deserialize_product(self, product_data: dict):
        return ProductFactory().create_product(**product_data)


class DictProductRepository(BaseProductRepository):
    """Simple repository that stores products in a dictionary"""

    def __init__(self, storage: dict | None = None, *args, **kwargs):
        if storage is None:
            storage = {}
        super().__init__(storage, *args, **kwargs)
        self.storage: dict[str, dict]

    def add(self, product: BaseProduct):
        self.storage[product.code] = product.to_dict()

    def get(self, product_id: int | str) -> BaseProduct | None:
        product_dict = self.storage.get(str(product_id))
        if product_dict:
            return self._deserialize_product(product_dict)
        else:
            return None

    def list(self) -> dict[str, BaseProduct]:
        """Return a dictionary with the products indexed by code"""
        return {
            code: self._deserialize_product(product_dict)
            for code, product_dict in self.storage.items()
        }

    def update(self, product: BaseProduct):
        if product.code in self.storage:
            self.storage[product.code] = product.to_dict()
        else:
            raise ValueError(f"Product with code {product.code} not found")

    def delete(self, product_id: int | str):
        if product_id in self.storage:
            del self.storage[str(product_id)]
        else:
            raise ValueError(f"Product with code {product_id} not found")

    def __str__(self):
        return f"DictProductRepository({self.storage})"

    def _serialize_product(self, product: BaseProduct):
        return product.to_dict()

    def _deserialize_product(self, product_data: dict):
        return ProductFactory().create_product(**product_data)


class JsonProductRepository(BaseProductRepository):
    """Repository that stores products in a JSON file"""

    def __init__(self, filename: str):
        self.filename = filename
        self.storage: dict[str, dict] = self.load()

    def load(self) -> dict:
        """Load products from JSON file, call this to keep the storage up to date"""
        try:
            with open(self.filename, "r") as file:
                self.storage = json.load(file)
                return self.storage
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save(self):
        try:
            with open(self.filename, "w") as file:
                json.dump(self.storage, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.filename} not found")

    def add(self, product: BaseProduct):
        self.load()
        if product.code not in self.storage:
            self.storage[product.code] = product.to_dict()
            self.save()

    def get(self, product_id: int | str):
        self.load()
        product_data = self.storage.get(str(product_id))
        if product_data:
            return self._deserialize_product(product_data)
        return None

    def list(self):
        self.all_product_data = self.load()
        return {
            code: self._deserialize_product(product_data)
            for code, product_data in self.storage.items()
        }

    def update(self, product: BaseProduct):
        self.load()
        product_to_update = self.get(product.code)
        if product_to_update and product.code in self.storage:
            self.storage[product.code] = product.to_dict()
            self.save()
        else:
            raise ProductNotFoundError(f"Product with code {product.code} not found")

    def delete(self, product_id: int | str):
        self.load()
        product_to_delete = self.get(product_id)
        if product_to_delete:
            del self.storage[str(product_id)]
            self.save()
            return True
        else:
            raise ValueError(f"Product with code {product_id} not found")

    def __str__(self):
        return f"JsonProductRepository({self.storage})"

    def _serialize_product(self, product: BaseProduct):
        return product.to_dict()

    def _deserialize_product(self, product_data: dict):
        return ProductFactory().create_product(**product_data)


class MySQLProductRepository(BaseProductRepository):
    """Repository that stores products in a MySQL database"""

    def __init__(self, connector: MySqlConnector):
        self.connector = connector

    def create_tables(self):
        self.connector.create_database("products")
        self.connector.create_tables()

    def add(self, product: BaseProduct):
        _fields = product.get_common_field_names()

        try:
            query = f"""
            INSERT INTO products ({", ".join(_fields)})
            VALUES ({", ".join(["%s" for _ in _fields])})
            """.strip()
            query_args = (
                product.code,
                product.name,
                product.price,
                product.description,
                product.stock,
                product.available,
                product.type,
            )
            self.connector.run_query(query, query_args, commit=False)
            if product.type != "product":
                _extra_table_name = (
                    product.type + "s" if product.type == "electronic" else product.type
                )
                extra_fields = product.get_extra_field_names()
                extra_query = f"""
                INSERT INTO {_extra_table_name} (code, {", ".join(extra_fields)})
                VALUES (%s, {", ".join(["%s" for _ in extra_fields])})
                """.strip()
                extra_query_args = (
                    product.code,
                    *[getattr(product, field) for field in extra_fields],
                )
                self.connector.run_query(
                    extra_query,
                    extra_query_args,
                    commit=False,
                )
        except Exception as ex:
            logger.error("Error adding product: %s", ex, exc_info=True)
            self.connector.rollback()
            raise ex
        else:
            self.connector.commit()
        return self.connector.run_query(
            "select code from products where code = %s", (product.code,)
        )

    def get(self, product_id: int | str):
        product_data = self.connector.run_query(
            "SELECT * FROM products WHERE code = %s", (str(product_id),)
        )
        if product_data:
            product_type = product_data[0].get("product_type", "product")
            if product_type == "product":
                return self._deserialize_product(product_data[0])
            extra_product_data = self.connector.run_query(
                f"SELECT * FROM {product_type if product_type != 'electronic' else product_type + 's'} WHERE code = %s",
                (str(product_id),),
            )
            product_data[0].update(extra_product_data[0])
            return self._deserialize_product(product_data[0])
        return None

    def _deserialize_product(self, product_data: dict):
        product_data["available"] = bool(product_data["available"])
        return ProductFactory().create_product(**product_data)

    def _serialize_product(self, product: BaseProduct):
        return product.to_dict()

    def list(self):
        product_data = self.connector.run_query("SELECT * FROM products")
        for product in product_data:
            product_type = product.get("product_type", "product")
            _extra_table = (
                None
                if product_type == "product"
                else (
                    product_type + "s" if product_type == "electronic" else product_type
                )
            )
            if _extra_table:
                extra_product_data = self.connector.run_query(
                    f"SELECT * FROM {_extra_table} WHERE code = %s", (product["code"],)
                )
                product.update(extra_product_data[0])
        return {p["code"]: self._deserialize_product(p) for p in product_data}

    def update(self, product: BaseProduct):
        _fields = product.get_common_field_names()
        _fields = tuple([field for field in _fields if field != "code"])
        try:
            query = f"""
            UPDATE products
            SET {", ".join([f"{field} = %s" for field in _fields])}
            WHERE code = %s
            """.strip()
            query_args = (
                product.name,
                product.price,
                product.description,
                product.stock,
                product.available,
                product.type,
                product.code,
            )
            self.connector.run_query(
                query,
                query_args,
                commit=False,
            )
            if product.type != "product":
                _extra_table_name = (
                    product.type + "s" if product.type == "electronic" else product.type
                )
                extra_fields = product.get_extra_field_names()
                extra_query = f"""
                UPDATE {_extra_table_name}
                SET {", ".join([f"{field} = %s" for field in extra_fields])}
                WHERE code = %s
                """.strip()
                extra_query_args = (
                    *[getattr(product, field) for field in extra_fields],
                    product.code,
                )
                self.connector.run_query(
                    extra_query,
                    extra_query_args,
                    commit=False,
                )
        except Exception as ex:
            logger.error("Error updating product: %s", ex, exc_info=True)
            self.connector.rollback()
            raise ex
        else:
            self.connector.commit()
        return self.connector.run_query(
            "select code from products where code = %s", (product.code,)
        )

    def delete(self, product_id: int | str):
        query = "DELETE FROM products WHERE code = %s"
        try:
            affected_rows = self.connector.run_query(query, (str(product_id),))
            if affected_rows:
                return affected_rows
            raise ProductNotFoundError(f"Product with code {product_id} not found")
        except ProductNotFoundError:
            raise
        except Exception as ex:
            logger.error("Error deleting product: %s", ex, exc_info=True)
            raise ValueError(f"Product with code {product_id} not found")

    def __str__(self):
        return "MySQLProductRepository()"


class RepositoryFactory:
    @staticmethod
    def get_repository(repository_type: str, *args, **kwargs):
        if repository_type == "list":
            return ListProductRepository(*args, **kwargs)
        elif repository_type == "dict":
            return DictProductRepository(*args, **kwargs)
        elif repository_type == "json":
            return JsonProductRepository(*args, **kwargs)
        else:
            raise ValueError(f"Unknown repository type: {repository_type}")


if __name__ == "__main__":
    import unittest
    from unittest import mock

    from models import Product

    class TestListProductRepository(unittest.TestCase):
        def setUp(self):
            self.product = Product("1", "Product", 10)
            self.repository = ListProductRepository()
            self.repository.add(self.product)

        def test_add_product(self):
            for product in self.repository.list().values():
                self.assertEqual(product.to_dict(), self.product.to_dict())

        def test_get_product(self):
            self.assertEqual(self.repository.get("1").to_dict(), self.product.to_dict())

        def test_list_products(self):
            for product in self.repository.list().values():
                self.assertEqual(product.to_dict(), self.product.to_dict())

        def test_update_product(self):
            new_product = Product("1", "New Product", 20)
            self.repository.update(new_product)
            self.assertEqual(self.repository.get("1").name, "New Product")
            self.assertEqual(self.repository.get("1").price, 20)

        def test_delete_product(self):
            self.repository.delete("1")
            self.assertEqual(self.repository.list(), {})

        def test_delete_product_not_found(self):
            with self.assertRaises(ValueError):
                self.repository.delete("2")

    class TestDictProductRepository(unittest.TestCase):
        def setUp(self):
            self.product = Product("1", "Product", 10)
            self.repository = DictProductRepository()
            self.repository.add(self.product)

        def test_add_product(self):
            for product_data in self.repository.list().values():
                self.assertEqual(product_data.to_dict(), self.product.to_dict())

        def test_get_product(self):
            self.assertEqual(self.repository.get("1").to_dict(), self.product.to_dict())

        def test_list_products(self):
            for product_data in self.repository.list().values():
                self.assertEqual(product_data.to_dict(), self.product.to_dict())

        def test_update_product(self):
            new_product = Product("1", "New Product", 20)
            self.repository.update(new_product)
            self.assertEqual(self.repository.get("1").name, "New Product")
            self.assertEqual(self.repository.get("1").price, 20)

        def test_delete_product(self):
            self.repository.delete("1")
            self.assertEqual(self.repository.list(), {})

        def test_delete_product_not_found(self):
            with self.assertRaises(ValueError):
                self.repository.delete("2")

    class TestJsonProductRepository(unittest.TestCase):
        def setUp(self):
            self.product = Product("1", "Product", 10)
            with mock.patch("__main__.open", mock.mock_open(read_data="{}")):
                self.repository = JsonProductRepository(filename="sample.json")
                self.repository.add(self.product)

        def test_add_product(self):
            with mock.patch("__main__.open", mock.mock_open()):
                for product in self.repository.list().values():
                    self.assertEqual(product.to_dict(), self.product.to_dict())

        def test_get_product(self):
            with mock.patch("__main__.open", mock.mock_open()):
                self.assertEqual(
                    self.repository.get("1").to_dict(), self.product.to_dict()
                )

        def test_list_products(self):
            with mock.patch("__main__.open", mock.mock_open()):
                for product in self.repository.list().values():
                    self.assertEqual(product.to_dict(), self.product.to_dict())

        def test_update_product(self):
            with mock.patch("__main__.open", mock.mock_open()):
                new_product = Product("1", "New Product", 20)
                self.repository.update(new_product)
                self.assertEqual(self.repository.get("1").name, "New Product")
                self.assertEqual(self.repository.get("1").price, 20)

        def test_delete_product(self):
            with mock.patch("__main__.open", mock.mock_open()):
                self.repository.delete("1")
                self.assertEqual(self.repository.list(), {})

        def test_delete_product_not_found(self):
            with mock.patch("__main__.open", mock.mock_open()):
                with self.assertRaises(ValueError):
                    self.repository.delete("2")

    unittest.main()
