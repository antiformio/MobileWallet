from models.models import User, Wallet
from schema import Wallet as SchemaWallet
from schema import Balance as SchemaBalance
from fastapi_sqlalchemy import db
from fastapi import Depends, HTTPException
from fastapi import APIRouter
from app.api.auth import auth_required

router = APIRouter()


@router.post(
    "/create-wallet/",
    response_model=SchemaWallet,
    dependencies=[Depends(auth_required)],
    tags=["Wallets"],
)
async def create_wallet(wallet: SchemaWallet):
    user = db.session.query(User).filter_by(id=wallet.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    db_wallet = Wallet(balance=wallet.balance, user_id=wallet.user_id)
    db.session.add(db_wallet)
    db.session.commit()
    return wallet


# This endpoint is just for administrative purposes. It shouldnt be used by any user.
@router.get("/wallets/", dependencies=[Depends(auth_required)], tags=["Wallets"])
async def get_users():
    return db.session.query(Wallet).all()


@router.get("/balance/", dependencies=[Depends(auth_required)], tags=["Wallets"])
async def get_balance(user_logged_in: User = Depends(auth_required)):
    return {
        "balance": db.session.query(Wallet)
        .filter_by(id=user_logged_in.wallet.id)
        .first()
        .balance
    }


@router.delete(
    "/wallet/{wallet_id}", dependencies=[Depends(auth_required)], tags=["Wallets"]
)
async def delete_wallet(wallet_id: int, user_logged_in: User = Depends(auth_required)):
    wallet = db.session.query(Wallet).filter_by(id=wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="No wallet found")

    if wallet.user_id != user_logged_in.id:
        raise HTTPException(
            status_code=404,
            detail="You are not the owner of this wallet. Please login with the owner credentials.",
        )

    db.session.delete(wallet)
    db.session.commit()
    return HTTPException(status_code=200, detail="Wallet deleted")


@router.get(
    "/wallet/{wallet_id}", dependencies=[Depends(auth_required)], tags=["Wallets"]
)
async def get_wallet(wallet_id: int, user_logged_in: User = Depends(auth_required)):
    wallet = db.session.query(Wallet).filter_by(id=wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="No wallet found")

    if wallet.user_id != user_logged_in.id:
        raise HTTPException(
            status_code=404,
            detail="You are not the owner of this wallet. Please login with the owner credentials.",
        )
    return wallet
