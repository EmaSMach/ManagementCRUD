from repositories import BaseProductRepository
from models import BaseProduct


class ProductService:
    def __init__(self, product_repository: BaseProductRepository):
        self.product_repository = product_repository

    def list(self):
        return self.product_repository.list()

    def get(self, product_id: int | str):
        return self.product_repository.get(product_id)

    def add(self, product: BaseProduct):
        return self.product_repository.add(product)

    def update(self, product: BaseProduct):
        return self.product_repository.update(product)

    def delete(self, product_id: int | str):
        return self.product_repository.delete(product_id)
