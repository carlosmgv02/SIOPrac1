import random
from sqlalchemy.orm import sessionmaker
from config.warehouse_config import get_db_engine
from model.warehouse import User, Titles, UserInteractions

Session = sessionmaker(bind=get_db_engine())
session = Session()


def insert_random_interactions(num_interactions):
    # Obtener todos los usuarios y títulos disponibles
    users = session.query(User).all()
    titles = session.query(Titles).all()

    # Verificar que hay usuarios y títulos disponibles
    if not users or not titles:
        print("No hay usuarios o títulos suficientes para generar interacciones.")
        return

    for _ in range(num_interactions):
        user = random.choice(users)
        title = random.choice(titles)
        rating = random.randint(1, 5)  # Asume que la calificación va de 1 a 5
        watched = True

        # Crear una nueva interacción
        interaction = UserInteractions(
            user_id=user.id,
            title_id=title.id,
            rating=rating,
            watched=watched
        )

        session.add(interaction)

    # Comprometer las interacciones a la base de datos
    session.commit()
    print(f"{num_interactions} interacciones han sido generadas e insertadas.")

insert_random_interactions(10000)