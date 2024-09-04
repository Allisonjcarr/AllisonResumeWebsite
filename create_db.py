from allison_resume.models import Base, engine

Base.metadata.create_all(bind=engine)
