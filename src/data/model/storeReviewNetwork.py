from data.model.baseReviewNetwork import BaseReviewNetwork
from domain.model.storeReviewDomain import StoreReviewDomain
from fireo.fields import TextField

class StoreReviewNetwork(BaseReviewNetwork):
    user_id = TextField(column_name='userId')
    store_id = TextField(column_name='storeId')
    pagination_key = TextField(column_name='paginationKey')

    def to_domain(self) -> StoreReviewDomain:
        return StoreReviewDomain(
            id=self.id,
            user_id=self.user_id,
            store_id=self.store_id,
            rating=self.rating,
            comment=self.comment,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    class Meta:
        collection_name = 'store-reviews'
