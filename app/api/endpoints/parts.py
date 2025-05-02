from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.part import Part, PartCreate, PartUpdate, PartList
from app.services.part_service import PartService
from app.services.text_analysis_service import TextAnalysisService

from typing import List
from app.schemas.text_analysis import CommonWord

router = APIRouter()


@router.get("/", response_model=PartList)
def read_parts(
        db: Session = Depends(get_db),
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(10, ge=1, le=100, description="Items per page"),
        name: Optional[str] = None,
        sku: Optional[str] = None,
        is_active: Optional[bool] = None
):
    # Calculate skip for pagination
    skip = (page - 1) * page_size

    filters = {}
    if name:
        filters["name"] = name
    if sku:
        filters["sku"] = sku
    if is_active is not None:
        filters["is_active"] = is_active

    result = PartService.get_parts(
        db=db,
        skip=skip,
        limit=page_size,
        filters=filters
    )

    return result


@router.get("/common-words", response_model=List[CommonWord])
def read_common_words(
        limit: int = Query(5, ge=1, le=50, description="Number of common words to return"),
        db: Session = Depends(get_db)
):
    return TextAnalysisService.get_common_words(db=db, limit=limit)


@router.get("/{part_id}", response_model=Part)
def read_part(part_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific part by ID.
    """
    db_part = PartService.get_part(db=db, part_id=part_id)
    if db_part is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Part with ID {part_id} not found"
        )
    return db_part


@router.post("/", response_model=Part, status_code=status.HTTP_201_CREATED)
def create_part(part: PartCreate, db: Session = Depends(get_db)):
    """
    Create a new part.
    """
    # Check if part with the same SKU already exists
    db_part = PartService.get_part_by_sku(db=db, sku=part.sku)
    if db_part:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Part with SKU {part.sku} already exists"
        )

    return PartService.create_part(db=db, part_data=part)


@router.put("/{part_id}", response_model=Part)
def update_part(
        part_id: int,
        part: PartUpdate,
        db: Session = Depends(get_db)
):
    """
    Update a part.
    """
    # Check if part exists
    db_part = PartService.get_part(db=db, part_id=part_id)
    if db_part is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Part with ID {part_id} not found"
        )

    # If SKU is being updated, check if it's already in use
    if part.sku is not None and part.sku != db_part.sku:
        existing_part = PartService.get_part_by_sku(db=db, sku=part.sku)
        if existing_part:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Part with SKU {part.sku} already exists"
            )

    updated_part = PartService.update_part(
        db=db,
        part_id=part_id,
        part_data=part
    )

    return updated_part


@router.delete("/{part_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_part(part_id: int, db: Session = Depends(get_db)):
    """
    Delete a part.
    """
    # Check if part exists
    db_part = PartService.get_part(db=db, part_id=part_id)
    if db_part is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Part with ID {part_id} not found"
        )

    success = PartService.delete_part(db=db, part_id=part_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the part"
        )
