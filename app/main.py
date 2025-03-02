from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://luis:123@db:5432/penjat")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    total_games = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    max_score = Column(Integer, default=0)

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)
    theme = Column(String)

class GameLog(Base):
    __tablename__ = "game_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word_id = Column(Integer, ForeignKey("words.id"))
    attempts = Column(Integer)
    errors = Column(Integer)
    score = Column(Integer)
    finished = Column(Boolean)

class UIText(Base):
    __tablename__ = "ui_texts"
    id = Column(Integer, primary_key=True, index=True)
    screen = Column(String)
    text = Column(String)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Esquemas Pydantic
class UserCreate(BaseModel):
    username: str
    password_hash: str

class WordCreate(BaseModel):
    word: str
    theme: str

class GameLogCreate(BaseModel):
    user_id: int
    word_id: int
    attempts: int
    errors: int
    score: int
    finished: bool

class UITextCreate(BaseModel):
    screen: str
    text: str

# FastAPI App
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- CRUD USERS ----------------
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, password_hash=user.password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_user.username = user.username
    db_user.password_hash = user.password_hash
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_user)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}

# ---------------- CRUD WORDS ----------------
@app.post("/words/")
def create_word(word: WordCreate, db: Session = Depends(get_db)):
    db_word = Word(word=word.word, theme=word.theme)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word

@app.get("/words/")
def get_words(db: Session = Depends(get_db)):
    return db.query(Word).all()

@app.get("/words/{word_id}")
def get_word(word_id: int, db: Session = Depends(get_db)):
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Palabra no encontrada")
    return word

@app.put("/words/{word_id}")
def update_word(word_id: int, word: WordCreate, db: Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.id == word_id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Palabra no encontrada")
    db_word.word = word.word
    db_word.theme = word.theme
    db.commit()
    db.refresh(db_word)
    return db_word

@app.delete("/words/{word_id}")
def delete_word(word_id: int, db: Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.id == word_id).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Palabra no encontrada")
    db.delete(db_word)
    db.commit()
    return {"message": "Palabra eliminada correctamente"}

# ---------------- CRUD GAME LOGS ----------------
@app.post("/game_logs/")
def create_game_log(game_log: GameLogCreate, db: Session = Depends(get_db)):
    db_log = GameLog(**game_log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@app.get("/game_logs/")
def get_game_logs(db: Session = Depends(get_db)):
    return db.query(GameLog).all()

@app.get("/game_logs/{log_id}")
def get_game_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(GameLog).filter(GameLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    return log

@app.delete("/game_logs/{log_id}")
def delete_game_log(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(GameLog).filter(GameLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    db.delete(db_log)
    db.commit()
    return {"message": "Partida eliminada correctamente"}

# ---------------- CRUD UI TEXTS ----------------
@app.post("/ui_texts/")
def create_ui_text(ui_text: UITextCreate, db: Session = Depends(get_db)):
    db_text = UIText(screen=ui_text.screen, text=ui_text.text)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text

@app.get("/ui_texts/")
def get_ui_texts(db: Session = Depends(get_db)):
    return db.query(UIText).all()

@app.get("/ui_texts/{text_id}")
def get_ui_text(text_id: int, db: Session = Depends(get_db)):
    text = db.query(UIText).filter(UIText.id == text_id).first()
    if not text:
        raise HTTPException(status_code=404, detail="Texto no encontrado")
    return text

@app.delete("/ui_texts/{text_id}")
def delete_ui_text(text_id: int, db: Session = Depends(get_db)):
    db_text = db.query(UIText).filter(UIText.id == text_id).first()
    if not db_text:
        raise HTTPException(status_code=404, detail="Texto no encontrado")
    db.delete(db_text)
    db.commit()
    return {"message": "Texto eliminado correctamente"}
