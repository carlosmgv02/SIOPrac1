from lightfm.data import Dataset
from matplotlib import pyplot as plt
from lightfm import LightFM
from lightfm.evaluation import auc_score, precision_at_k
from sqlalchemy.orm import sessionmaker
from config.warehouse_config import get_db_engine
from model.warehouse import UserInteractions, User, Titles
from utils.randomize_interactions import insert_random_interactions, delete_interactions

# Configuración de la sesión de SQLAlchemy
Session = sessionmaker(bind=get_db_engine())
session = Session()


def prepare_dataset():
    users = session.query(User).all()
    titles = session.query(Titles).all()

    dataset = Dataset()
    dataset.fit(users=(user.id for user in users), items=(title.id for title in titles))

    interactions, _ = dataset.build_interactions(
        ((interaction.user_id, interaction.title_id, interaction.rating)
         for interaction in session.query(UserInteractions).all())
    )
    return dataset, interactions


def refresh_interactions(dataset):
    interactions, _ = dataset.build_interactions(
        ((interaction.user_id, interaction.title_id, interaction.rating)
         for interaction in session.query(UserInteractions).all())
    )
    return interactions


def evaluate_model(model, interactions, item_features, user_features, num_threads=2):
    auc = auc_score(model, interactions, item_features=item_features, user_features=user_features,
                    num_threads=num_threads).mean()
    precision = precision_at_k(model, interactions, item_features=item_features, user_features=user_features, k=5,
                               num_threads=num_threads).mean()
    return auc, precision


def train_model(interactions, item_features, user_features, num_epochs=30, num_threads=2, loss='warp'):
    model = LightFM(loss=loss)
    model.fit(interactions, item_features=item_features, user_features=user_features, epochs=num_epochs, num_threads=num_threads)
    return model


# Preparación del dataset
dataset, interactions = prepare_dataset()

# Entrenamiento y evaluación inicial del modelo
model = train_model(interactions, None, None)
train_auc, train_precision = evaluate_model(model, interactions, None, None)

# Almacenamiento de resultados
auc_results = [train_auc]
precision_results = [train_precision]

# Experimento incrementando las interacciones
interaction_steps = [0, 10, 20, 50, 100, 200, 500, 1000, 10000]
for step in interaction_steps:
    inserted_ids = insert_random_interactions(step)
    interactions = refresh_interactions(dataset)  # Actualiza las interacciones
    model = train_model(interactions, None, None)  # Reentrenar con nuevas interacciones
    auc, precision = evaluate_model(model, interactions, None, None)
    auc_results.append(auc)
    precision_results.append(precision)
    delete_interactions(inserted_ids)

# Asegúrate de que los resultados están correctamente indexados y mostrados
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].plot(['Inicio'] + [f'+{x}' for x in interaction_steps], auc_results, marker='o', linestyle='-')
ax[0].set_title('Comparación de AUC')
ax[0].set_xlabel('Número de Interacciones Adicionales')
ax[0].set_ylabel('AUC Score')

ax[1].plot(['Inicio'] + [f'+{x}' for x in interaction_steps], precision_results, marker='o', linestyle='-')
ax[1].set_title('Comparación de Precision@k')
ax[1].set_xlabel('Número de Interacciones Adicionales')
ax[1].set_ylabel('Precision@k Score')

plt.tight_layout()
plt.show()

