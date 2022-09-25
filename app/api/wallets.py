from models.models import User, Wallet
from schema import Wallet as SchemaWallet
from fastapi_sqlalchemy import db
from fastapi import Depends, HTTPException
from fastapi import APIRouter
import schema
from aux.oauth2 import get_current_user

router = APIRouter(tags=["Wallets"])


@router.post(
    "/create-wallet/",
    response_model=SchemaWallet
)
async def create_wallet(
    wallet: SchemaWallet, current_user: schema.User = Depends(get_current_user)
):
    # TODO create new schema and only receive balance, the user of the wallet we can get from 
    #   current_user (user logged in)
    #   - Maybe we can even initialize the wallet with 0 balance. do not allow user to choose it

    user = db.session.query(User).filter_by(id=wallet.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    db_wallet = Wallet(balance=wallet.balance, user_id=wallet.user_id)
    db.session.add(db_wallet)
    db.session.commit()
    return wallet


@router.get("/wallets/")
async def get_users(current_user: schema.User = Depends(get_current_user)):
    return db.session.query(Wallet).all()


@router.get("/balance/")
async def get_balance(current_user: schema.User = Depends(get_current_user)):
    return {
        "balance": db.session.query(Wallet)
        .filter_by(id=current_user.wallet.id)
        .first()
        .balance
    }


@router.delete("/wallet/{wallet_id}")
async def delete_wallet(
    wallet_id: int, current_user: schema.User = Depends(get_current_user)
):
    wallet = db.session.query(Wallet).filter_by(id=wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="No wallet found")

    if wallet.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="You are not the owner of this wallet. Please login with the owner credentials.",
        )

    db.session.delete(wallet)
    db.session.commit()
    return HTTPException(status_code=200, detail="Wallet deleted")


@router.get("/wallet/{wallet_id}")
async def get_wallet(
    wallet_id: int, current_user: schema.User = Depends(get_current_user)
):
    wallet = db.session.query(Wallet).filter_by(id=wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="No wallet found")

    if wallet.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="You are not the owner of this wallet. Please login with the owner credentials.",
        )
    return wallet
