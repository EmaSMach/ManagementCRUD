from models import BaseProduct
from typing import Literal

import os


PRODUCT_TYPES = Literal["generic", "electronic", "food", "clothing"]


class Menu:
    def __init__(self, title: str, options: list[str], back_option: str = "Back"):
        self.title = title
        self.options = options
        self.back_option = back_option


class CLIView:
    def show_menu(self, menu: Menu | list[str], back_text: str = "Back"):
        self.clear_screen()
        if isinstance(menu, Menu):
            print(f"{menu.title}\n")
            for i, option in enumerate(menu.options):
                print(f"{i+1}. {option}")
            print(f"0. {back_text or menu.back_option}\n")
            return input("Select an option: ")
        if isinstance(menu, list):
            for i, option in enumerate(menu):
                print(f"{i+1}. {option}")
            print("0. Cancel\n")
            selected = input("Select an option: ")
            if selected == "0":
                return None
            return menu[int(selected) - 1]
        raise ValueError("Invalid menu type")

    def clear_screen(slef):
        os.system("cls" if os.name == "nt" else "clear")

    def main_menu(self):
        main_menu = Menu(
            "Products",
            [
                "Add Product",
                "List Products",
                "Search Product",
                "Update Product",
                "Delete Product",
            ],
        )
        while True:
            try:
                return self.show_menu(main_menu, back_text="Exit")
            except ValueError:
                print("Invalid option")
                input()

    def wait_for_user(self):
        input("Press enter to continue...")

    def delete_product(self):
        return input("Enter the product ID to delete: ")

    def update_product(self, product_data):
        self.clear_screen()
        print("Update Product")
        update_data = {}
        print("Enter new product data. Leave blank to keep the original value.")
        for key, value in product_data.items():
            if key in ("product_type", "code"):
                continue
            new_value = input(f"{key} ({value}): ")
            if new_value:
                update_data[key] = new_value
        return update_data

    def search_product(self):
        self.clear_screen()
        self.show_message("Search Product", "\n")
        return input("Enter the product code to search: ")

    def get_product_fields(self, product_type: PRODUCT_TYPES):
        pass

    def show_message(self, message: str, *args):
        print(message, *args)

    def add_product(self, fields: list[str]):
        product_data = {}
        for field in fields:
            if field == "product_type":
                continue
            product_data[field] = input(f"Enter {field}: ")
        return product_data

    def list_products(self, products: dict[str, BaseProduct]):
        self.clear_screen()
        self.show_message("Products")
        for product in products.values():
            print(f"{product.code}, {product.name}, {product.type}")
        input("Press enter to continue...")

    def show_product_details(self, product: BaseProduct):
        print(product)
        input("Press enter to continue...")
        return None


if __name__ == "__main__":
    view = CLIView()
    selected_option = view.main_menu()
