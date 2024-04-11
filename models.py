import sqlalchemy.orm
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DB_URI = os.getenv('DB_URI')

Base = sqlalchemy.orm.declarative_base()
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
session = Session()

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

Base.metadata.create_all(engine)