from controller import Controller
from models import ProductFactory
from views import CLIView


def main():
    from repositories import JsonProductRepository

    repository_options = {
        "filename": "products.json",
    }
    repository = JsonProductRepository(**repository_options)
    view = CLIView()
    product_factory = ProductFactory()
    controller = Controller(repository=repository, view=view, product_factory=product_factory)
    controller.run()


if __name__ == "__main__":
    main()
