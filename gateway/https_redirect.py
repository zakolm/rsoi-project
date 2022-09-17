import fastapi as _fastapi
import fastapi.security as _security
###########################################################################
import ast
import json
import os
import uuid
from datetime import datetime

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import Response, JSONResponse
import aiohttp

from cb import CircuitBreakerSession
from schema import RentalResponse, DeviceResponse,\
    ReserveSchema, ReturnReserveSchema, \
    ReservationResponse , UserCreate #, NewReservationResponse # RatingSchema
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL',
                                  'http://localhost:8081')

RENTAL_SERVICE_URL = os.environ.get('RENTAL_SERVICE_URL',
                                     'http://127.0.0.1:8082')

RESERVATION_SERVICE_URL = os.environ.get('RESERVATION_SERVICE_URL',
                                         'http://127.0.0.1:8083')

# RATING_SERVICE_URL = os.environ.get('RATING_SERVICE_URL',
#                                     'http://127.0.0.1:8084')


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={
        'message': exc.detail
    })


@app.post("/api/v1/login")
async def auth(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
):
    url = f'{AUTH_SERVICE_URL}/api/token'
    async with CircuitBreakerSession() as session:
        payload = {k: v for k, v in form_data.__dict__.items() if v is not None and len(v) > 0}
        payload_tmp = {k: '' for k, v in form_data.__dict__.items() if not(k in payload.keys())}
        payload = {**payload, **payload_tmp}

        data = ''
        for el in payload.items():
            data += el[0] + '=' + el[1] + '&'
        data = data[:-1]

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            resp = await session.post(url, data=data, headers=headers, raise_exception=True)
            body = await resp.json()
            await resp.release()
        except Exception:
            raise HTTPException(status_code=503,
                                detail='Auth Service unavailable')
        return body


@app.post("/api/v1/registration")
async def auth(
        user: UserCreate
    # form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
):
    url = f'{AUTH_SERVICE_URL}/api/users'
    async with CircuitBreakerSession() as session:
        payload = {k: v for k, v in user.__dict__.items() if v is not None and len(v) > 0}
        payload_tmp = {k: '' for k, v in user.__dict__.items() if not(k in payload.keys())}
        payload = {**payload, **payload_tmp}

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        try:
            resp = await session.post(url, data=json.dumps(payload), headers=headers, raise_exception=True)
            body = await resp.json()
            await resp.release()
        except Exception:
            raise HTTPException(status_code=503,
                                detail='Auth Service unavailable')
        return body


@app.get("/api/v1/me")
async def me():
    url = f'{AUTH_SERVICE_URL}/api/users'
    async with CircuitBreakerSession() as session:
        try:
            resp = await session.post(url, raise_exception=True)
            body = await resp.json()
            await resp.release()
        except Exception:
            raise HTTPException(status_code=503,
                                detail='Auth Service unavailable')
        return body


async def get_rental(session, rentalUid: uuid.UUID) -> RentalResponse:
    url = f'{RENTAL_SERVICE_URL}/api/v1/rentals/{rentalUid}'
    async with session.get(url) as response:
        rental_body = await response.json()
    return RentalResponse(**rental_body)


async def get_device(session, deviceUid: uuid.UUID) -> DeviceResponse:
    url = f'{RENTAL_SERVICE_URL}/api/v1/devices/{deviceUid}'
    async with session.get(url) as response:
        device_body = await response.json()
    return DeviceResponse(**device_body)


@app.get("/api/v1/devices/<deviceUid>")
async def _device(deviceUid):
    async with CircuitBreakerSession() as session:
        # device_uid = reservation_body['deviceUid']
        print(deviceUid)
        body = await get_device(session, deviceUid)
        print(body)

        return body

# @app.get("/api/v1/rating")
# async def rating(username: str = Header('', alias='X-User-Name')):
#     url = f'{RATING_SERVICE_URL}/api/v1/rating'
#     async with CircuitBreakerSession() as session:
#         session.headers.add('X-User-Name', username)
#         try:
#             resp = await session.get(url, raise_exception=True)
#             body = await resp.json()
#             await resp.release()
#         except Exception:
#             raise HTTPException(status_code=503,
#                                 detail='Rating Service unavailable')
#         print(body)
#         body = body[0] if type(body) == list else body
#         rating_schema = RatingSchema(**body)
#         return rating_schema


@app.get("/api/v1/rentals/{rentalUid}/devices")
async def rental_devices(rentalUid, page: int, size: int):
    url = f'{RENTAL_SERVICE_URL}/api/v1/rentals/{rentalUid}/devices?' \
          f'&page={page}&size={size}'
    async with CircuitBreakerSession() as session:
        async with session.get(url, raise_exception=True) as response:
            body = await response.json()

            return body


@app.get("/api/v1/rentals")
async def rentals(city: str, page: int, size: int):
    url = f'{RENTAL_SERVICE_URL}/api/v1/rentals?' \
          f'city={city}&page={page}&size={size}'
    async with CircuitBreakerSession() as session:
        async with session.get(url, raise_exception=True) as response:
            body = await response.json()
        print(body)
        return body


@app.get("/api/v1/reservations")
async def list_reservations(username: str = Header('', alias='Authorization')):
    print(username)
    url = f'{RESERVATION_SERVICE_URL}/api/v1/reservations'
    async with CircuitBreakerSession() as session:
        session.headers.add('X-User-Name', username)
        async with session.get(url, raise_exception=True) as response:
            data = await response.read()
            body = json.loads(data) if is_json(data) else []
            reservation_list = []
            for reservation_body in body:
                device_uid = reservation_body['deviceUid']
                print(device_uid)
                rental_uid = reservation_body['rentalUid']
                device = await get_device(session, device_uid)
                print(device)
                rental = await get_rental(session, rental_uid)
                reservation_list.append(ReservationResponse(
                    reservationUid=reservation_body['reservationUid'],
                    status=reservation_body['status'],
                    startDate=datetime.fromisoformat(
                        reservation_body['startDate']).date().isoformat(),
                    tillDate=datetime.fromisoformat(
                        reservation_body['tillDate']).date().isoformat(),
                    device=device,
                    rental=rental
                ))
        return reservation_list


@app.post("/api/v1/reservations")
async def reservations(schema: ReserveSchema,
                       username: str = Header('', alias='X-User-Name')
                       ) -> ReservationResponse:
    async with aiohttp.ClientSession() as session:
        session.headers.add('X-User-Name', username)
        session.headers.add('Content-Type', 'application/json')
        async with session.get(
                f'{RENTAL_SERVICE_URL}/api/v1/devices/{schema.deviceUid}') as device_response:
            device = await device_response.json()
        # device = await get_device(session, schema.deviceUid)
        async with session.get(
                f'{RENTAL_SERVICE_URL}/api/v1/rentals/{schema.rentalUid}') \
                as rental_response:
            rental = await rental_response.json()
        # rental = await get_rental(session, schema.rentalUid)
        rentalId = int(rental.get('id', None))
        print(device)
        deviceId = int(device.get('id', None))
        async with session.get(
                f'{RENTAL_SERVICE_URL}/api/v1/availableCount?'
                f'rentalId={rentalId}&deviceId={deviceId}') \
                as availableCount_response:
            available_count = await availableCount_response.json()
            available_count = available_count.get('avaiblableCount')

        if available_count is not None and available_count != 0:
            # async with session.get(f'{RATING_SERVICE_URL}/api/v1/rating') \
            #         as rating_response:
            #     stars = await rating_response.json()
           # stars = await rating(username=username)
           #  print(stars)
           #  print(type(stars))
           #  stars = stars.stars

            # print(stars)
            # stars = stars[0] if type(stars) == list else stars

            async with session.get(
                    f'{RESERVATION_SERVICE_URL}/api/v1/reservations') \
                    as reservations_response:
                data = await reservations_response.read()
            data = json.loads(data) if is_json(data) else []
            len_resercations = 0
            for i in data:
                if i.get('status'):
                    len_resercations += 1

            # print(type(stars))

            if True:
            # if (stars - len_resercations) > 0:
                reservation_data = {
                    'deviceUid': str(schema.deviceUid),
                    'rentalUid': str(schema.rentalUid),
                    'tillDate': datetime(schema.tillDate.year,
                                         schema.tillDate.month,
                                         schema.tillDate.day).isoformat()
                }
                reservation_data_json = json.dumps(reservation_data)
                async with session.post(
                        f'{RESERVATION_SERVICE_URL}/api/v1/reservations',
                        data=reservation_data_json) as reservation_response:
                    print(await reservation_response.text())
                    reservation = await reservation_response.json()

                available_count -= 1
                async with session.post(
                        f'{RENTAL_SERVICE_URL}/api/v1/availableCount?'
                        f'rentalId={rentalId}&deviceId={deviceId}') \
                        as availableCount_response:
                    print(availableCount_response.text)

                print(reservation)
                print(device)
                print(rental)
                # print(stars)
                return ReservationResponse(
                    reservationUid=reservation['reservationUid'],
                    status=reservation['status'],
                    startDate=datetime.fromisoformat(
                        reservation['startDate']).date().isoformat(),
                    tillDate=datetime.fromisoformat(
                        reservation['tillDate']).date().isoformat(),
                    device=device,
                    rental=rental,
                    # rating={"stars": stars}
                )


# @app.post("/api/v1/reservations/{reservationUid}/return")
# async def library_books(reservationUid, schema: ReturnReserveSchema,
#                         username: str = Header('', alias='X-User-Name')):
#     async with aiohttp.ClientSession() as session:
#         session.headers.add('X-User-Name', username)
#         session.headers.add('Content-Type', 'application/json')
#
#         reservation_data = {
#             'date': datetime.fromisoformat(schema.date).date().isoformat()
#         }
#         reservation_data_json = json.dumps(reservation_data)
#         async with session.post(f'{RESERVATION_SERVICE_URL}/api/v1/'
#                                 f'reservations/{reservationUid}/return',
#                                 data=reservation_data_json) \
#                 as reservation_response:
#             print(await reservation_response.text())
#             reservation = await reservation_response.json()
#
#         print(reservation.get('bookUid'))
#
#         book_data = {
#             'condition': schema.condition
#         }
#         bookUid = reservation.get('bookUid')
#         book_data_json = json.dumps(book_data)
#
#         async with session.get(
#                 f'{LIBRARY_SERVICE_URL}/api/v1/books/{bookUid}') \
#                 as book_response:
#             book_tmp = await book_response.json()
#         book_condition = book_tmp.get('condition')
#         async with session.post(
#                 f'{LIBRARY_SERVICE_URL}/api/v1/books/{bookUid}',
#                 data=book_data_json) as book_response:
#             print(await book_response.text())
#             book = await book_response.json()
#
#         print(reservation)
#
#         libraryUid = reservation.get('libraryUid')
#         url = f'{LIBRARY_SERVICE_URL}/api/v1/libraries/{libraryUid}'
#         async with session.get(url) as response:
#             library_body = await response.json()
#         url = f'{LIBRARY_SERVICE_URL}/api/v1/books/{bookUid}'
#         async with session.get(url) as response:
#             book_body = await response.json()
#         libraryId = library_body.get('id')
#         bookId = book_body.get('id')
#         print(libraryId, bookId)
#
#         async with session.post(
#                 f'{LIBRARY_SERVICE_URL}/api/v1/availableCount/return?'
#                 f'libraryId={libraryId}&bookId={bookId}') \
#                 as availableCount_response:
#             print(availableCount_response.text)
#
#         if reservation.get('status') is not None and \
#                 book.get('condition') is not None:
#             rating = 0
#             if reservation.get('status') == 'EXPIRED':
#                 rating -= 10
#
#             print(book_condition, schema.condition)
#             if book_condition != schema.condition:
#                 if book_condition == 'EXCELLENT':
#                     rating -= 10
#                 elif book_condition == 'GOOD':
#                     if schema.condition == 'BAD':
#                         rating -= 10
#
#             print(rating)
#             if rating == 0:
#                 rating += 1
#
#             rating_data = {
#                 'stars': rating
#             }
#             rating_data_json = json.dumps(rating_data)
#
#             try:
#                 async with session.post(f'{RATING_SERVICE_URL}/api/v1/rating',
#                                      data=rating_data_json) as rating_response:
#                     stars = await rating_response.json()
#             except:
#                 return Response(status_code=204)
#             return Response(status_code=204)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port='8080')
