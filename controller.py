from datetime import datetime

from repositories import (BaseProductRepository, ProductFactory,
                          ProductNotFoundError)
from views import CLIView


class Controller:
    def __init__(self, repository: BaseProductRepository, view: CLIView, product_factory: ProductFactory) -> None:
        self.repository = repository
        self.view = view
        self.product_factory = product_factory

    def convert_data(self, data: dict):
        for key, value in data.items():
            if key == "price":
                data[key] = float(value)
            if key == "stock":
                data[key] = int(value)
            if key == "available":
                if not value or value.lower() in ("true", "yes", "1"):
                    data[key] = True
                else:
                    data[key] = False
            if key == "warranty":
                data[key] = int(value)
            if key == "expiration_date":
                data[key] = datetime.strptime(value, "%Y-%m-%d")
        return data

    def add_product(self):
        product_types = self.repository.get_product_types()
        while True:
            try:
                selected_product_type = self.view.show_menu(product_types)
                break
            except ValueError:
                self.view.show_message("Invalid option")
                self.view.wait_for_user()
        if not selected_product_type:
            return False
        product_fields = self.product_factory.get_product_class(selected_product_type).get_field_names()
        product_data = self.view.add_product(product_fields)
        product_data["product_type"] = selected_product_type
        if not product_data:
            return
        try:
            product_data = self.convert_data(product_data)
            new_product = self.product_factory.create_product(**product_data)
            self.repository.add(new_product)
        except Exception as ex:
            self.view.show_message("Error adding product:", ex)
            self.view.wait_for_user()

    def list_products(self):
        products = self.repository.list()
        return self.view.list_products(products)

    def show_product_details(self):
        product_code = self.view.search_product()
        product = self.repository.get(product_code)
        if not product:
            self.view.show_message("Product not found")
            self.view.wait_for_user()
            return
        self.view.show_product_details(product)

    def update_product(self):
        product_code = input("Enter the product code to update: ")
        if not product_code:
            self.view.show_message("No code entered")
            self.view.wait_for_user()
            return
        try:
            product = self.repository.get(product_code)
        except ProductNotFoundError:
            self.view.show_message("Product does not exist: ", product_code)
            self.view.wait_for_user()
            return
        except Exception:
            self.view.show_message("Error updating product: ", product_code)
            self.view.wait_for_user()
            return
        # rare cases
        if product is None:
            self.view.show_message("Product not found")
            self.view.wait_for_user()
            return
        original_data = product.to_dict()
        updated_data = self.view.update_product(original_data)
        if not updated_data:
            self.view.show_message("No changes made")
            self.view.wait_for_user()
            return
        original_data.update(updated_data)
        try:
            product_data = self.convert_data(original_data)
            updated_product = self.product_factory.create_product(**product_data)
            self.repository.update(updated_product)
            self.view.show_message("Product updated")
            self.view.wait_for_user()
        except Exception as ex:
            self.view.show_message("Error updating product: ", product_code, ex)
            self.view.wait_for_user()

    def delete_product(self):
        product_code = self.view.delete_product()
        if product_code:
            try:
                self.repository.delete(product_code)
            except ProductNotFoundError:
                self.view.show_message("Product does not exist: ", product_code)
                self.view.wait_for_user()
                return False
            except Exception:
                self.view.show_message("Error deleting product: ", product_code)
                self.view.wait_for_user()
                return False
            self.view.show_message("Product deleted")
            self.view.wait_for_user()
            return True
        self.view.show_message("No code entered")
        self.view.wait_for_user()
        return False

    def run(self):
        while True:
            main_menu_selected_option = self.view.main_menu()
            if main_menu_selected_option == "0":
                break
            if main_menu_selected_option == "1":
                self.add_product()
            elif main_menu_selected_option == "2":
                self.list_products()
            elif main_menu_selected_option == "3":
                self.show_product_details()
            elif main_menu_selected_option == "4":
                self.update_product()
            elif main_menu_selected_option == "5":
                self.delete_product()
