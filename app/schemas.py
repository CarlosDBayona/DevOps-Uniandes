from . import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Blacklist


class BlacklistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        load_instance = True


