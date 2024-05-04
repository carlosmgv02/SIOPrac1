import sqlalchemy.orm
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv
import os

from config.warehouse_config import get_db_session

Base = sqlalchemy.orm.declarative_base()
session = get_db_session()

'''
    Tabla de relación M:N para TitleGenres
'''
TitleGenres = Table('titlegenres', Base.metadata,
    Column('title_id', String, ForeignKey('titles.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

'''
    Tabla de relación M:N para TitleCountries
'''
TitleCountries = Table('titlecountries', Base.metadata,
    Column('title_id', String, ForeignKey('titles.id'), primary_key=True),
    Column('country_id', Integer, ForeignKey('productioncountries.id'), primary_key=True)
)

'''
    Clase que representa la tabla de títulos.
'''
class Titles(Base):
    __tablename__ = 'titles'
    id = Column(String, primary_key=True)
    title = Column(String)
    type = Column(String)
    description = Column(String)
    release_year = Column(Integer)
    runtime = Column(Integer)
    seasons = Column(Integer)
    imdb_id = Column(String)
    imdb_score = Column(Float)
    imdb_votes = Column(Integer)
    tmdb_popularity = Column(Float)
    tmdb_score = Column(Float)
    age_certification_id = Column(Integer, ForeignKey('agecertifications.id'))
    platform_id = Column(Integer, ForeignKey('platforms.id'))

    # Relaciones actualizadas
    genres = relationship('Genres', secondary=TitleGenres, back_populates='titles')
    countries = relationship('ProductionCountries', secondary=TitleCountries, back_populates='titles')
    credits = relationship('Credits', back_populates='title')
    age_certification = relationship('AgeCertifications')
    platform = relationship('Platforms')
    interactions = relationship("UserInteractions", back_populates="title")

'''
    Clase que representa la tabla de géneros.
'''
class Genres(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    # Relación inversa
    titles = relationship('Titles', secondary=TitleGenres, back_populates='genres')

'''
    Clase que representa la tabla de países de producción.
'''
class ProductionCountries(Base):
    __tablename__ = 'productioncountries'
    id = Column(Integer, primary_key=True)
    country_code = Column(String)
    # Relación inversa
    titles = relationship('Titles', secondary=TitleCountries, back_populates='countries')

'''
    Clase que representa la tabla de créditos.
'''


class Credits(Base):
    __tablename__ = 'credits'
    # Cambia la definición de person_id para que ya no sea la clave primaria por sí sola.
    person_id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    title_id = Column(String, ForeignKey('titles.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    # Añade una columna para el nombre del personaje si es necesario
    character = Column(String)

    # Relaciones
    title = relationship('Titles', back_populates='credits')
    role = relationship('Roles', back_populates='credits')


class AgeCertifications(Base):
    __tablename__ = 'agecertifications'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

class Platforms(Base):
    __tablename__ = 'platforms'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)


class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    # Relación inversa con Credits
    credits = relationship('Credits', back_populates='role')

class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # Asegúrate de que el nombre es único si lo usas para evitar duplicados


class UserPreferences(Base):
    __tablename__ = 'user_preferences'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    preferred_type = Column(String)
    favorite_genre_id = Column(Integer, ForeignKey('genres.id'))
    preferred_certification_id = Column(Integer, ForeignKey('agecertifications.id'))
    preferred_platform_id = Column(Integer, ForeignKey('platforms.id'))
    preferred_duration_min = Column(Integer)
    preferred_duration_max = Column(Integer)

    user = relationship('User', back_populates='preferences')
    favorite_genre = relationship('Genres')
    preferred_certification = relationship('AgeCertifications')
    preferred_platform = relationship('Platforms')

class UserInteractions(Base):
    __tablename__ = 'user_interactions'
    interaction_id = Column(Integer, primary_key=True, autoincrement=True)  # Ensure this is defined
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title_id = Column(String, ForeignKey('titles.id'), nullable=False)
    rating = Column(Integer)
    watched = Column(Boolean, default=False)

    user = relationship("User", back_populates="interactions")
    title = relationship("Titles", back_populates="interactions")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    preferences = relationship('UserPreferences', back_populates='user', uselist=False)
    interactions = relationship('UserInteractions', back_populates='user')



Base.metadata.create_all(session.bind)
