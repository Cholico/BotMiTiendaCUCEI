from data.model.baseReviewNetwork import BaseReviewNetwork
from domain.model.productReviewDomain import ProductReviewDomain
from fireo.fields import TextField

class ProductReviewNetwork(BaseReviewNetwork):
    user_id = TextField(column_name='userId')
    product_id = TextField(column_name='productId')
    pagination_key = TextField(column_name='paginationKey')

    def to_domain(self) -> ProductReviewDomain:
        return ProductReviewDomain(
            id=self.id,
            user_id=self.user_id,
            product_id=self.product_id,
            rating=self.rating,
            comment=self.comment,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    class Meta:
        collection_name = 'product-reviews'