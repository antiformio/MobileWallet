from pydantic import BaseModel


class User(BaseModel):
    name: str
    db_username: str
    db_password: str

    class Config:
        orm_mode = True


class Wallet(BaseModel):
    balance: int
    user_id: int

    class Config:
        orm_mode = True


class Balance(BaseModel):
    balance: int


class Transaction(BaseModel):
    destination_user: int
    amount: int
    description: str


class TransactionResponse(BaseModel):
    from_user: int
    to_user: int
    amount: int
    description: str
    time_created: str
