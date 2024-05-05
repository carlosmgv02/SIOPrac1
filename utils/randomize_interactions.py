import random
from sqlalchemy.orm import sessionmaker
from config.warehouse_config import get_db_engine
from model.warehouse import User, Titles, UserInteractions

Session = sessionmaker(bind=get_db_engine())
session = Session()


def insert_random_interactions(num_interactions):
    users = session.query(User).all()
    titles = session.query(Titles).all()
    inserted_interactions = []

    if not users or not titles:
        print("No hay usuarios o títulos suficientes para generar interacciones.")
        return inserted_interactions

    for _ in range(num_interactions):
        user = random.choice(users)
        title = random.choice(titles)
        rating = random.randint(1, 5)
        watched = True

        interaction = UserInteractions(user_id=user.id, title_id=title.id, rating=rating, watched=watched)
        session.add(interaction)
        session.flush()  # Esto asegura que se asigna un ID sin tener que hacer commit inmediatamente
        inserted_interactions.append(interaction.interaction_id)

    session.commit()
    print(f"{num_interactions} interacciones han sido generadas e insertadas.")
    return inserted_interactions

def delete_interactions(interaction_ids):
    for interaction_id in interaction_ids:
        interaction = session.query(UserInteractions).get(interaction_id)
        if interaction:
            session.delete(interaction)
    session.commit()
    print(f"{len(interaction_ids)} interacciones han sido eliminadas.")

