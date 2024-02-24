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

TitleGenres = Table('titlegenres', Base.metadata,
    Column('title_id', String, ForeignKey('titles.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

# Tabla de relación M:N para TitleCountries
TitleCountries = Table('titlecountries', Base.metadata,
    Column('title_id', String, ForeignKey('titles.id'), primary_key=True),
    Column('country_id', Integer, ForeignKey('productioncountries.id'), primary_key=True)
)

class Titles(Base):
    __tablename__ = 'titles'
    id = Column(String, primary_key=True)
    title = Column(String)
    type = Column(String)
    description = Column(String)
    release_year = Column(Integer)
    age_certification = Column(String)
    runtime = Column(Integer)
    seasons = Column(Integer)
    imdb_id = Column(String)
    imdb_score = Column(Float)
    imdb_votes = Column(Integer)
    tmdb_popularity = Column(Float)
    tmdb_score = Column(Float)
    # Relaciones
    genres = relationship('Genres', secondary=TitleGenres, back_populates='titles')
    countries = relationship('ProductionCountries', secondary=TitleCountries, back_populates='titles')
    credits = relationship('Credits', back_populates='title')

class Genres(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    # Relación inversa
    titles = relationship('Titles', secondary=TitleGenres, back_populates='genres')

class ProductionCountries(Base):
    __tablename__ = 'productioncountries'
    id = Column(Integer, primary_key=True)
    country_code = Column(String)
    # Relación inversa
    titles = relationship('Titles', secondary=TitleCountries, back_populates='countries')

class Credits(Base):
    __tablename__ = 'credits'
    person_id = Column(Integer, primary_key=True)
    title_id = Column(String, ForeignKey('titles.id'))
    name = Column(String)
    character = Column(String)
    role = Column(String)
    # Relación con Titles
    title = relationship('Titles', back_populates='credits')

Base.metadata.create_all(engine)