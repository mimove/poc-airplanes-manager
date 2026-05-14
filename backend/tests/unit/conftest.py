# Import all models so that SQLAlchemy can resolve relationship strings
# and configure_mappers() can succeed when tests construct bare ORM instances.
from sqlalchemy.orm import configure_mappers

import app.models.airplane  # noqa: F401
import app.models.flight  # noqa: F401
import app.models.flight_passenger  # noqa: F401
import app.models.hangar  # noqa: F401
import app.models.passenger  # noqa: F401

configure_mappers()
