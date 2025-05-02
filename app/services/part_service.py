from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.models.part import Part
from app.schemas.part import PartCreate, PartUpdate
from app.core.exceptions import DatabaseError


class PartService:
    @staticmethod
    def get_parts(
            db: Session,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        query = db.query(Part)

        if filters:
            if filters.get("name"):
                query = query.filter(Part.name.ilike(f"%{filters['name']}%"))
            if filters.get("sku"):
                query = query.filter(Part.sku.ilike(f"%{filters['sku']}%"))
            if filters.get("is_active") is not None:
                query = query.filter(Part.is_active == filters["is_active"])

        total = query.count()

        parts = query.offset(skip).limit(limit).all()

        pages = (total + limit - 1) // limit if limit else 1

        return {
            "items": parts,
            "total": total,
            "page": (skip // limit) + 1 if limit else 1,
            "page_size": limit,
            "pages": pages
        }

    @staticmethod
    def get_part(db: Session, part_id: int) -> Optional[Part]:
        return db.query(Part).filter(Part.id == part_id).first()

    @staticmethod
    def get_part_by_sku(db: Session, sku: str) -> Optional[Part]:
        return db.query(Part).filter(Part.sku == sku).first()

    @staticmethod
    def create_part(db: Session, part_data: PartCreate) -> Part:
        try:
            db_part = Part(**part_data.model_dump())
            db.add(db_part)
            db.commit()
            db.refresh(db_part)
            return db_part
        except Exception as e:
            db.rollback()
            raise DatabaseError(f"Error creating part: {str(e)}")

    @staticmethod
    def update_part(
            db: Session,
            part_id: int,
            part_data: PartUpdate
    ) -> Optional[Part]:
        db_part = PartService.get_part(db, part_id)
        if db_part:
            # Filter out None values to avoid overriding with None
            update_data = {
                k: v for k, v in part_data.model_dump().items()
                if v is not None
            }

            for key, value in update_data.items():
                setattr(db_part, key, value)

            db.commit()
            db.refresh(db_part)
        return db_part

    @staticmethod
    def delete_part(db: Session, part_id: int) -> bool:
        db_part = PartService.get_part(db, part_id)
        if db_part:
            db.delete(db_part)
            db.commit()
            return True
        return False
