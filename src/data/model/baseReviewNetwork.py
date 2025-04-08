from fireo.models import Model
from fireo.fields import NumberField, TextField, DateTime

class BaseReviewNetwork(Model):
    rating = NumberField()
    comment = TextField()
    created_at = DateTime(column_name='createdAt')
    updated_at = DateTime(column_name='updatedAt')

    class Meta:
        abstract = True