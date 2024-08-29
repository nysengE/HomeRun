# services/rental_service.py
from sqlalchemy.orm import Session
from datetime import datetime

from app.schema.rental import RentalCreate, Rental

class RentalServices:
    def create_rental(db: Session, rental: RentalCreate):
        db_rental = Rental(
            title=rental.title,
            contents=rental.contents,
            people=rental.people,
            price=rental.price,
            zipcode=rental.zipcode,
            businessno=rental.businessno,
            sportsno=rental.sportsno,
            sigunguno=rental.sigunguno,
            regisdate=datetime.now()
        )
        db.add(db_rental)
        db.commit()
        db.refresh(db_rental)
        return db_rental
