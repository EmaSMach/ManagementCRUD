import datetime


class BaseProduct:
    """Base class for products"""

    def __init__(
        self,
        code: str,
        name: str,
        price: float,
        description: str | None = None,
        stock: int = 0,
        available: bool = True,
        product_type: str = "product",
    ):
        self.__code: str = self.validate_code(code)
        self.__name: str = self.validate_name(name)
        self.__price: float = self.validate_price(price)
        self.__description: str | None = self.validate_description(description)
        self.__stock: int = self.validate_stock(stock)
        self.__available: bool = self.validate_available(available)
        self.__type: str = product_type

    def __str__(self):
        return f"{self.code}) Product(code={self.code}), name={self.name}, type={self.type}, stock={self.stock}, price={self.price}"

    def __repr__(self):
        return f"Product({self.code}, {self.name}, {self.price}, {self.description}, {self.stock}, {self.available})"

    @classmethod
    def get_field_names(cls):
        return (
            "code",
            "name",
            "price",
            "description",
            "stock",
            "available",
            "product_type",
        )

    @staticmethod
    def get_product_types():
        return ["product", "electronic", "food", "clothing"]

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value: str):
        """Check there are no duplicated codes"""
        self.__code = self.validate_code(value)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self.__name = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value: str | None):
        if not isinstance(value, (str, type(None))):
            raise ValueError("Description must be a string")
        self.__description = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value: float | int):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, value: int):
        if value < 0:
            raise ValueError("Stock cannot be negative")
        self.__stock = value

    @property
    def available(self):
        return self.__available

    @available.setter
    def available(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Available must be a boolean")
        if self.stock == 0:
            value = False
        else:
            self.__available = value

    # validations
    @staticmethod
    def validate_code(value: str):
        if not isinstance(value, str):
            raise ValueError("Code must be a string")
        return value

    @staticmethod
    def validate_name(value: str):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        return value

    @staticmethod
    def validate_description(value: str | None):
        if not isinstance(value, (str, type(None))):
            raise ValueError("Description must be a string")
        return value

    @staticmethod
    def validate_price(value: float | int):
        try:
            value = float(value)
        except (ValueError, TypeError):
            print("Valor", value)
            raise ValueError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        return value

    @staticmethod
    def validate_stock(value: int):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValueError("Stock must be an integer")
        if value < 0:
            raise ValueError("Stock cannot be negative")
        return value

    @staticmethod
    def validate_available(value: bool):
        if not isinstance(value, bool):
            raise ValueError("Available must be a boolean")
        return value

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "stock": self.stock,
            "available": self.available,
            "product_type": self.type,
        }


class Product(BaseProduct):
    """Generic product"""


class ElectronicProduct(BaseProduct):
    """Electronic product"""

    def __init__(self, *args, warranty: int = 0, **kwargs):
        super().__init__(*args, **kwargs)
        self.__warranty = self.validate_warranty(warranty)

    @classmethod
    def get_field_names(cls):
        return super().get_field_names() + ("warranty",)

    @property
    def warranty(self):
        return self.__warranty

    @warranty.setter
    def warranty(self, value: int):
        self.__warranty = self.validate_warranty(value)

    def validate_warranty(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Warranty must be an integer")
        if value < 0:
            raise ValueError("Warranty cannot be negative")
        return value

    def to_dict(self):
        return {**super().to_dict(), "warranty": self.warranty}

    def __str__(self):
        return f"{self.code}) Product(code={self.code}, name={self.name}, stock={self.stock}, price={self.price}, warranty={self.warranty})"

    def __repr__(self):
        return f"ElectronicProduct({self.code}, {self.name}, {self.price}, {self.description}, {self.stock}, {self.available}, {self.warranty})"


class FoodProduct(BaseProduct):
    """Food product"""

    def __init__(
        self, *args, expiration_date: str | datetime.date | None = None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.__expiration_date = self.validate_expiration_date(expiration_date)

    @classmethod
    def get_field_names(cls):
        return super().get_field_names() + ("expiration_date",)

    @property
    def expiration_date(self):
        return self.__expiration_date.strftime("%Y-%m-%d")

    @expiration_date.setter
    def expiration_date(self, value: str | datetime.date):
        self.__expiration_date = self.validate_expiration_date(value)

    def validate_expiration_date(self, value: str | datetime.date | None):
        if value is None:
            return None
        if not isinstance(value, (str, datetime.date)):
            raise TypeError("Expiration date must be a string")
        if isinstance(value, str):
            try:
                value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format")
        return value

    def to_dict(self):
        return {**super().to_dict(), "expiration_date": self.expiration_date}

    def __str__(self):
        return f"{self.code}) FoodProduct(code={self.code}, name={self.name}, stock={self.stock}, price={self.price}, expiration_date={self.expiration_date})"

    def __repr__(self):
        return f"FoodProduct({self.code}, {self.name}, {self.price}, {self.description}, {self.stock}, {self.available}, {self.expiration_date})"


class ClothingProduct(BaseProduct):
    """Clothing product"""

    def __init__(self, *args, size: str = "", color: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__size = self.validate_size(size)
        self.__color = self.validate_color(color)

    @classmethod
    def get_field_names(cls):
        return super().get_field_names() + ("size", "color")

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Color must be a string")
        self.__color = value

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Size must be a string")
        self.__size = self.validate_size(value)

    def validate_size(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Size must be a string")
        return value

    def validate_color(self, value: str | None):
        if not isinstance(value, (str, type(None))):
            raise TypeError("Color must be a string")
        return value

    def to_dict(self):
        return {**super().to_dict(), "size": self.size, "color": self.color}

    def __str__(self):
        return f"{self.code}) ClothingProduct(code={self.code}, name={self.name}, stock={self.stock}, price={self.price}, size={self.size}, color={self.color})"

    def __repr__(self):
        return f"ClothingProduct({self.code}, {self.name}, {self.price}, {self.description}, {self.stock}, {self.available}, {self.size}, {self.color})"


class ProductFactory:
    """Factory class for creating products"""

    @staticmethod
    def create_product(*args, **kwargs):
        product_type = kwargs.get("product_type", "product")
        if product_type == "product":
            return Product(*args, **kwargs)
        elif product_type == "electronic":
            return ElectronicProduct(*args, **kwargs)
        elif product_type == "food":
            return FoodProduct(*args, **kwargs)
        elif product_type == "clothing":
            return ClothingProduct(*args, **kwargs)
        else:
            raise ValueError("Invalid product type")

    def get_product_class(self, product_type: str):
        if product_type == "product":
            return Product
        elif product_type == "electronic":
            return ElectronicProduct
        elif product_type == "food":
            return FoodProduct
        elif product_type == "clothing":
            return ClothingProduct
        else:
            return None


if __name__ == "__main__":
    import unittest


    class TestBaseProduct(unittest.TestCase):
        def test_code(self):
            product = BaseProduct("123", "Product", 10)
            self.assertEqual(product.code, "123")
            with self.assertRaises(ValueError):
                product.code = 123

        def test_name(self):
            product = BaseProduct("123", "Product", 10)
            self.assertEqual(product.name, "Product")
            with self.assertRaises(ValueError):
                product.name = 123

        def test_description(self):
            product = BaseProduct("123", "Product", 10, "Description")
            self.assertEqual(product.description, "Description")
            with self.assertRaises(ValueError):
                product.description = 123

        def test_price(self):
            product = BaseProduct("123", "Product", 10)
            self.assertEqual(product.price, 10)
            with self.assertRaises(ValueError):
                product.price = -10

        def test_stock(self):
            product = BaseProduct("123", "Product", 10)
            self.assertEqual(product.stock, 0)
            with self.assertRaises(ValueError):
                product.stock = -10

        def test_available(self):
            product = BaseProduct("123", "Product", 10)
            self.assertEqual(product.available, True)
            with self.assertRaises(ValueError):
                product.available = 1

        def test_to_dict(self):
            product = BaseProduct("123", "Product", 10, "Description", 5, True)
            self.assertEqual(
                product.to_dict(),
                {
                    "code": "123",
                    "name": "Product",
                    "price": float(10),
                    "description": "Description",
                    "stock": 5,
                    "available": True,
                    "product_type": "product",
                },
            )


    class TestProduct(unittest.TestCase):
        def test_product(self):
            product = Product("123", "Product", 10)
            self.assertEqual(product.code, "123")
            self.assertEqual(product.name, "Product")
            self.assertEqual(product.price, float(10))
            self.assertEqual(product.description, None)
            self.assertEqual(product.stock, 0)
            self.assertEqual(product.available, True)

        def test_to_dict(self):
            product = Product("123", "Product", 10, "Description", 5, True)
            self.assertEqual(
                product.to_dict(),
                {
                    "code": "123",
                    "name": "Product",
                    "price": float(10),
                    "description": "Description",
                    "stock": 5,
                    "available": True,
                    "product_type": "product",
                },
            )


    class TestElectronicProduct(unittest.TestCase):
        def test_electronic_product(self):
            product = ElectronicProduct("123", "Product", 10, warranty=1)
            self.assertEqual(product.code, "123")
            self.assertEqual(product.name, "Product")
            self.assertEqual(product.price, float(10))
            self.assertEqual(product.description, None)
            self.assertEqual(product.stock, 0)
            self.assertEqual(product.available, True)
            self.assertEqual(product.warranty, 1)

        def test_to_dict(self):
            product = ElectronicProduct(
                "123", "Product", 10, "Description", 5, True, warranty=1
            )
            self.assertEqual(
                product.to_dict(),
                {
                    "code": "123",
                    "name": "Product",
                    "price": float(10),
                    "description": "Description",
                    "stock": 5,
                    "available": True,
                    "warranty": 1,
                    "product_type": "product",
                },
            )


    class TestFoodProduct(unittest.TestCase):
        def test_food_product(self):
            product = FoodProduct("123", "Product", 10, expiration_date="2022-12-31")
            self.assertEqual(product.code, "123")
            self.assertEqual(product.name, "Product")
            self.assertEqual(product.price, 10)
            self.assertEqual(product.description, None)
            self.assertEqual(product.stock, 0)
            self.assertEqual(product.available, True)
            self.assertEqual(
                product.expiration_date,
                datetime.date(2022, 12, 31).strftime("%Y-%m-%d"),
            )

        def test_to_dict(self):
            product = FoodProduct(
                "123",
                "Product",
                10,
                "Description",
                5,
                True,
                expiration_date="2022-12-31",
            )
            self.assertEqual(
                product.to_dict(),
                {
                    "code": "123",
                    "name": "Product",
                    "price": float(10),
                    "description": "Description",
                    "stock": 5,
                    "available": True,
                    "expiration_date": datetime.date(2022, 12, 31).strftime("%Y-%m-%d"),
                    "product_type": "product",
                },
            )


    class TestClothingProduct(unittest.TestCase):
        def test_clothing_product(self):
            product = ClothingProduct("123", "Product", 10, size="M", color="blue")
            self.assertEqual(product.code, "123")
            self.assertEqual(product.name, "Product")
            self.assertEqual(product.price, 10)
            self.assertEqual(product.description, None)
            self.assertEqual(product.stock, 0)
            self.assertEqual(product.available, True)
            self.assertEqual(product.size, "M")
            self.assertEqual(product.color, "blue")

        def test_to_dict(self):
            product = ClothingProduct(
                "123", "Product", 10, "Description", 5, True, size="M", color="blue"
            )
            self.assertEqual(
                product.to_dict(),
                {
                    "code": "123",
                    "name": "Product",
                    "price": float(10),
                    "description": "Description",
                    "stock": 5,
                    "available": True,
                    "size": "M",
                    "color": "blue",
                    "product_type": "product",
                },
            )


    unittest.main()
