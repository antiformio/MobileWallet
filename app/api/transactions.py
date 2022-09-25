from models.models import Wallet, User, Transaction, TransactionConcepts
from schema import Transaction as SchemaTransaction
from fastapi_sqlalchemy import db
from fastapi import Depends, HTTPException
from fastapi import APIRouter
import schema
from aux.oauth2 import get_current_user

router = APIRouter(tags=["Transactions"])


@router.post(
    "/create-transaction/",
    response_model=SchemaTransaction
)
async def create_transaction(
    transaction: SchemaTransaction,
    current_user: schema.User = Depends(get_current_user),
):
    origin_wallet = (
        db.session.query(Wallet).filter_by(id=current_user.wallet.id).first()
    )

    if not origin_wallet:
        raise HTTPException(
            status_code=404,
            detail="You dont have a wallet associated. Please create one first.",
        )

    destin_user = (
        db.session.query(User).filter_by(id=transaction.destination_user).first()
    )

    if not destin_user:
        raise HTTPException(
            status_code=404,
            detail="The user that you are trying to send money to, does not exist.",
        )

    if not destin_user.wallet:
        raise HTTPException(
            status_code=404,
            detail="The user that you are trying to send money to, does not have a wallet.",
        )

    destin_user_wallet = (
        db.session.query(Wallet).filter_by(id=destin_user.wallet.id).first()
    )

    if not destin_user_wallet:
        raise HTTPException(
            status_code=404,
            detail="The user that you are trying to send money to, does not have a wallet.",
        )

    if origin_wallet.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="You are not the owner of this wallet. Please login with the owner credentials.",
        )

    if transaction.amount > current_user.wallet.balance:
        raise HTTPException(
            status_code=404,
            detail="You are not have enough funds.",
        )

    origin_wallet.balance -= transaction.amount
    destin_user_wallet.balance += transaction.amount

    db_transaction_outgoing = Transaction(
        wallet_id=origin_wallet.id,
        to_user=destin_user.id,
        amount=transaction.amount,
        concept=TransactionConcepts.outgoing.value,
        description=transaction.description,
    )

    db_transaction_incoming = Transaction(
        wallet_id=destin_user_wallet.id,
        from_user=origin_wallet.id,
        amount=transaction.amount,
        concept=TransactionConcepts.incoming.value,
        description=transaction.description,
    )
    db.session.add_all(
        [
            origin_wallet,
            db_transaction_outgoing,
            db_transaction_incoming,
            destin_user_wallet,
        ]
    )
    db.session.commit()
    return transaction


@router.get("/transactions/")
async def get_transactions(current_user: schema.User = Depends(get_current_user)):
    return (
        db.session.query(Wallet)
        .filter_by(id=current_user.wallet.id)
        .first()
        .transactions
    )
