from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db, SessionLocal

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Items API",
    description="API sederhana untuk manajemen Item menggunakan FastAPI, SQLAlchemy, dan SQLite",
    version="1.0.0",
)


# ─── Seed Data ───────────────────────────────────────────────────────────────

def seed_data(db: Session):
    """Masukkan data awal jika tabel masih kosong."""
    if db.query(models.Item).count() == 0:
        initial_items = [
            models.Item(name="Laptop Asus VivoBook", description="Laptop ringan 14 inci untuk produktivitas sehari-hari", price=7500000.0, stock=15),
            models.Item(name="Mouse Wireless Logitech", description="Mouse nirkabel ergonomis dengan baterai tahan lama", price=250000.0, stock=50),
            models.Item(name="Keyboard Mechanical", description="Keyboard mekanik dengan switch Blue dan backlight RGB", price=450000.0, stock=30),
            models.Item(name="Monitor LG 24 inci", description="Monitor Full HD IPS 75Hz cocok untuk kerja dan gaming ringan", price=2100000.0, stock=10),
            models.Item(name="SSD Samsung 512GB", description="SSD SATA internal berkecepatan tinggi untuk upgrade laptop/PC", price=800000.0, stock=25),
        ]
        db.add_all(initial_items)
        db.commit()


# Seed saat aplikasi pertama kali dijalankan
with SessionLocal() as db_session:
    seed_data(db_session)


# ─── Endpoints ───────────────────────────────────────────────────────────────

@app.get(
    "/",
    summary="Root",
    description="Halaman utama API",
)
def root():
    return {"message": "Selamat datang di Items API! Kunjungi /docs untuk Swagger UI."}


@app.get(
    "/items/",
    response_model=List[schemas.ItemResponse],
    status_code=status.HTTP_200_OK,
    summary="Ambil Semua Item",
    description="Mengembalikan daftar semua item yang tersedia di database.",
    tags=["Items"],
)
def get_all_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Endpoint **GET /items/**

    Mengembalikan semua item dengan opsional pagination menggunakan `skip` dan `limit`.
    """
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items


@app.get(
    "/items/{id}",
    response_model=schemas.ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Ambil Item Berdasarkan ID",
    description="Mengembalikan satu item berdasarkan ID yang diberikan. Jika tidak ditemukan, mengembalikan 404.",
    tags=["Items"],
)
def get_item_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    """
    Endpoint **GET /items/{id}**

    Mengembalikan detail item berdasarkan `id`. Jika item tidak ditemukan, akan mengembalikan HTTP 404.
    """
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item dengan ID {id} tidak ditemukan.",
        )
    return item
