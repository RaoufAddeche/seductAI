# test_models.py
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

# 👤 User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)

    # 🔁 Relation avec Interaction
    interactions = relationship("Interaction", back_populates="user")

# 💬 Interaction model
class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # clé étrangère OK
    message = Column(String)

    # 🔁 Relation avec User
    user = relationship("User", back_populates="interactions")


# 🔧 Test de création des tables + insertion
if __name__ == "__main__":
    # BDD SQLite en mémoire
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)  # Création des tables

    with Session(engine) as session:
        # Création d'un utilisateur
        user = User(username="Raouf")
        session.add(user)
        session.commit()

        # Création d'une interaction liée
        interaction = Interaction(user_id=user.id, message="Hello coach")
        session.add(interaction)
        session.commit()

        # Vérification
        result = session.query(Interaction).first()
        print("Contenu Interaction:", result.message)
        print("Utilisateur lié :", result.user.username)
