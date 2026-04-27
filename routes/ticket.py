from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.ticket import Ticket
from models.user import User
from services.ai_service import generate_answer

# 🔥 BURASI ÖNEMLİ
from routes.auth import get_current_user

router = APIRouter(prefix="/tickets")


# 🔥 DB BAĞLANTISI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 TICKET OLUŞTURMA
@router.post("/")
def create_ticket(
    question: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    answer = generate_answer(question)

    new_ticket = Ticket(
        question=question,
        answer=answer,
        user_id=current_user.id,
        status="open"
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "id": new_ticket.id,
        "question": new_ticket.question,
        "answer": new_ticket.answer,
        "status": new_ticket.status
    }


# 🔥 KULLANICI KENDİ TICKETLARI
@router.get("/")
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tickets = db.query(Ticket).filter(Ticket.user_id == current_user.id).all()

    return tickets


# 🔥 ADMIN TÜM TICKETLAR
@router.get("/all")
def get_all_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    tickets = db.query(Ticket).all()

    return tickets


# 🔥 STATUS UPDATE (ADMIN)
@router.patch("/{ticket_id}")
def update_ticket_status(
    ticket_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = status

    db.commit()
    db.refresh(ticket)

    return ticket