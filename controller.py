from repositories import BaseProductRepository, ProductFactory, ProductNotFoundError
from views import CLIView


class Controller:
    def __init__(self, repository: BaseProductRepository, view: CLIView, product_factory: ProductFactory) -> None:
        self.repository = repository
        self.view = view
        self.product_factory = product_factory

    def add_product(self):
        product_types = self.repository.get_product_types()
        selected_product_type = self.view.show_menu(product_types)
        if not selected_product_type:
            return False
        product_fields = self.product_factory.get_product_class(selected_product_type).get_field_names()
        product_data = self.view.add_product(product_fields)
        if not product_data:
            return
        try:
            new_product = self.product_factory.create_product(**product_data)
            self.repository.add(new_product)
        except Exception:
            self.view.show_message("Error adding product")

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
        product_id = self.view.get_product_id()
        product = self.repository.get(product_id)
        updated_product = self.view.get_product_data(product.product_type)
        self.repository.update(product_id, updated_product)

    def delete_product(self):
        product_code = self.view.delete_product()
        if product_code:
            try:
                print(self.repository.delete(product_code))
            except ProductNotFoundError:
                self.view.show_message("Product does not exist: ", product_code)
                self.view.wait_for_user()
                return False
            except Exception:
                self.view.show_message("Error deleting product: ", product_code)
                self.view.wait_for_user()
                return False
            print("Product deleted")
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
                pass
            elif main_menu_selected_option == "5":
                self.delete_product()


if __name__ == "__main__":
    from repositories import JsonProductRepository

    repository_options = {
        "filename": "products.json",
    }
    repository = JsonProductRepository(**repository_options)
    view = CLIView()
    product_factory = ProductFactory()
    controller = Controller(repository=repository, view=view, product_factory=product_factory)
    controller.run()
