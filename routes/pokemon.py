from fastapi import Depends, APIRouter, File, UploadFile
from typing import Annotated
from schemas.pokemon import Pokemon, PokemonStats
from database.connection import get_db
from database.pokemonmodel import Pokemon as PokemonTableModel
from database.pokemonmodel import PokemonStats as PokemonStatsModel
from sqlalchemy.orm import Session, subqueryload
import csv

router = APIRouter(prefix='/pokemon', tags=['pokemon'])


@router.get('/')
def import_all_pokemon(db: Session = Depends(get_db)):
    pokemons = db.query(PokemonTableModel).options(
        subqueryload(PokemonTableModel.stats)).all()
    return pokemons


@router.get('/{pokemon_name}')
def find_specific_pokemon(pokemon_name: str, db: Session = Depends(get_db)):
    item = db.query(PokemonTableModel).filter(
        PokemonTableModel.name.ilike(f"%{pokemon_name}%")).first()
    if item:
        stats = item.stats
        return item
    return {'message': 'Nothing Found'}


@router.post('/pokemons/')
def uploadCSVFileToPokemonDatabase(file: UploadFile, db: Session = Depends(get_db)):
    fileContent = file.file.read().decode("utf-8")
    rows = csv.reader(fileContent.splitlines(), delimiter=",")
    next(rows)
    for row in rows:
        pokemon = PokemonTableModel(id=row[0], classification=row[1], name=row[3], percentage_male=float(
            row[4]) if row[4] else None, type1=row[5], type2=row[6], generation=row[7], is_legendary=False if row[8] == '0' else True)
        db.add(pokemon)
    db.commit()


@router.post('/stats/')
def uploadCSVFileToPokemonStatsDatabase(file: UploadFile, db: Session = Depends(get_db)):
    fileContent = file.file.read().decode("utf-8")
    rows = csv.reader(fileContent.splitlines(), delimiter=",")
    next(rows)
    for row in rows:
        pokemonStats = PokemonStatsModel(pokemon_id=row[0], height_m=row[26] if row[26] else None,
                                         weight_kg=row[31] if row[31] else None, attack=row[19], defense=row[24], hp=row[27], speed=row[30])
        db.add(pokemonStats)
    db.commit()
