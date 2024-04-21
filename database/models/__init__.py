from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry

Base = declarative_base()

from database.models.client import *
from database.models.transaction import *
from database.models.admin_groups import *
from database.models.feedback import *

mapper_registry = registry()