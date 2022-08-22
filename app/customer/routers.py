from fastapi import APIRouter, Request, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import (
    CustomerModel,
    CustomerCreateModel,
    CustomerUpdateModel,
    CustomerResponseModel,
    CustomerListResponseModel,
)

router = APIRouter()


@router.get("/{document}", response_model=CustomerResponseModel)
async def read(request: Request, document: str):
    if customer := await request.app.mongodb["customer"].find_one(
        {"document": document}
    ):
        response = CustomerResponseModel.from_dict(customer)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=jsonable_encoder(response)
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )


@router.get("/", response_model=CustomerListResponseModel)
async def read_all(request: Request):
    return CustomerListResponseModel.from_list(
        await request.app.mongodb["customer"].find().to_list(None)
    )


@router.post(
    "/save", status_code=status.HTTP_201_CREATED, response_model=CustomerResponseModel
)
async def create(request: Request, customer: CustomerCreateModel = Body(...)):
    if await request.app.mongodb["customer"].find_one({"document": customer.document}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer document already exists",
        )

    customer_inserted = await request.app.mongodb["customer"].insert_one(
        customer.to_dict()
    )

    response = CustomerResponseModel.from_dict(
        await request.app.mongodb["customer"].find_one(
            {"_id": customer_inserted.inserted_id}
        )
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=jsonable_encoder(response)
    )


@router.put("/{document}", response_model=CustomerModel)
async def update(
    request: Request, document: str, customer: CustomerUpdateModel = Body(...)
):
    if actual_customer := await request.app.mongodb["customer"].find_one(
        {"document": document}
    ):
        actual_customer.update(customer.to_dict())
        await request.app.mongodb["customer"].update_one(
            {"document": document}, {"$set": actual_customer}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    response = CustomerResponseModel.from_dict(actual_customer)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(response)
    )


@router.delete("/{document}")
async def delete(request: Request, document: str):
    if await request.app.mongodb["customer"].find_one({"document": document}):
        await request.app.mongodb["customer"].delete_one({"document": document})
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content={})
