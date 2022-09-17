import uuid
from datetime import date
from typing import Optional

import pydantic


class _UserBase(pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int

    class Config:
        orm_mode = True


class OmitNullModel(pydantic.BaseModel):
    def dict(self, *args, **kwargs) -> dict:
        kwargs['exclude_none'] = True
        return super().dict(*args, **kwargs)


# class RatingSchema(OmitNullModel):
#     stars: Optional[int]


# class RatingResponse(OmitNullModel):
#     stars: Optional[int]


class DeviceResponse(OmitNullModel):
    deviceUid: Optional[str]
    name: Optional[str]
    brand: Optional[str]


class RentalResponse(OmitNullModel):
    rentalUid: Optional[uuid.UUID]
    name: Optional[str]
    address: Optional[str]
    city: Optional[str]


class ReserveSchema(OmitNullModel):
    deviceUid: Optional[uuid.UUID]
    rentalUid: Optional[uuid.UUID]
    tillDate: Optional[date]


class ReturnReserveSchema(OmitNullModel):
    condition: Optional[str]
    date: Optional[str]


class ReservationResponse(OmitNullModel):
    reservationUid: Optional[uuid.UUID]
    status: Optional[str]
    startDate: Optional[str]
    tillDate: Optional[str]
    device: Optional[DeviceResponse]
    rental: Optional[RentalResponse]


# class NewReservationResponse(ReservationResponse):
#     rating: Optional[RatingResponse]
