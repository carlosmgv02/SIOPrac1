from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_
from sqlalchemy.exc import NoResultFound

# Configuración de conexión
from config.warehouse_config import POSTGRES_URI

engine = create_engine(POSTGRES_URI)
Session = sessionmaker(bind=engine)

class DatabaseUtility:
    def __init__(self, model):
        self.model = model
        self.session = Session()

    def get_all(self):
        """Obtiene todos los registros del modelo especificado."""
        return self.session.query(self.model).all()

    def get_by_id(self, id):
        """Obtiene un registro por su ID."""
        try:
            return self.session.query(self.model).filter(self.model.id == id).one()
        except NoResultFound:
            return None

    def get_explicit_preferences(self, user_id):
        """Obtiene las preferencias explícitas de un usuario."""
        try:
            return self.session.query(UserPreferences).filter(UserPreferences.user_id == user_id).one()
        except NoResultFound:
            return None

    def get_user_history(self, user_id):
        """Obtiene el historial de visualización de un usuario."""
        return self.session.query(UserHistory).filter(UserHistory.user_id == user_id).all()

    def add(self, **kwargs):
        """Agrega un nuevo registro al modelo especificado."""
        new_entry = self.model(**kwargs)
        self.session.add(new_entry)
        self.session.commit()
        return new_entry

    def update_by_id(self, id, **kwargs):
        """Actualiza un registro por su ID."""
        entry = self.session.query(self.model).get(id)
        if entry:
            for key, value in kwargs.items():
                setattr(entry, key, value)
            self.session.commit()
            return entry

    def delete_by_id(self, id):
        """Elimina un registro por su ID."""
        entry = self.session.query(self.model).get(id)
        if entry:
            self.session.delete(entry)
            self.session.commit()
            return True
        return False

    def __del__(self):
        """Cierra la sesión al destruir la instancia de la clase."""
        self.session.close()
