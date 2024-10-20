from allison_resume.db import Base, engine

Base.metadata.create_all(bind=engine)
