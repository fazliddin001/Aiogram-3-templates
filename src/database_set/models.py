from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from .base import BaseModel

# Here is the place where you can write your Models.
# Name your models descriptively and use the suffix 'Model'.

# For example:
# - UsersModel
# - ProductsModel

# You can write services for your models in the following location:
# Location:
#   src/database_services/services/user_services
#
# The directory structure for services is as follows:
# src/
#   database_services/
#     services/
#       user_services.py  # For user-related database operations
#       product_services.py  # For product-related database operations
#
# Service files should be named descriptively, e.g.:
# - user_services.py
# - product_services.py


# e.g.
# also the BaseModel adds the fields created_at, updated_at, id
class UsersModel(BaseModel):
    __tablename__ = 'users'

    full_name: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column(SMALLINT)
