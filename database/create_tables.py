from database.database import engine
from database.database import Base

import database.models

Base.metadata.create_all(bind=engine)

print("Database Tables Created Successfully!")