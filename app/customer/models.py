from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, validator
from datetime import datetime


class CustomerEnum(Enum):
    NATURAL = "natural"
    JURIDICAL = "juridical"


class CustomerModel(BaseModel):
    customer_type: CustomerEnum = Field(
        ..., description="Customer type", example="natural"
    )
    document: str = Field(
        ...,
        description="Document number",
        example="01234567890",
        min_length=11,
        max_length=14,
    )
    name: str = Field(..., description="Name")

    @classmethod
    @validator("customer_type", pre=True)
    def validate_customer_type(cls, v):
        if v not in ["natural", "juridical"]:
            raise ValueError("Customer type must be natural or juridical")
        return v

    @classmethod
    @validator("document", pre=True)
    def validate_document(cls, v, values):
        if not v.isdigit():
            raise ValueError("Document must be a number")

        match values.get("customer_type"):
            case CustomerEnum.NATURAL:
                if len(v) != 11:
                    raise ValueError("Document must be 11 digits")
            case CustomerEnum.JURIDICAL:
                if len(v) != 14:
                    raise ValueError("Document must be 14 digits")
        return v

    @classmethod
    @validator("name", pre=True)
    def validate_name(cls, v):
        if not v.isalpha():
            raise ValueError("Name must be alphabetic")
        return v

    @classmethod
    @validator("username", pre=True)
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v


class CustomerCreateModel(CustomerModel):

    def to_dict(self):
        return {
            "document": self.document,
            "name": self.name,
            "customer_type": self.customer_type.value,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }


class CustomerUpdateModel(BaseModel):
    name: str = Field(..., description="Name")

    def to_dict(self):
        return {
            "name": self.name,
            "updated_at": datetime.now(),
        }


class CustomerResponseModel(CustomerModel):
    id: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, customer: dict):
        return CustomerResponseModel(
            id=str(customer.get("_id")),
            customer_type=customer.get("customer_type"),
            document=customer.get("document"),
            name=customer.get("name"),
            created_at=customer.get("created_at"),
            updated_at=customer.get("updated_at"),
        )


class CustomerListResponseModel(BaseModel):
    customers: Optional[List[CustomerResponseModel]] = None

    @classmethod
    def from_list(cls, customers):
        return cls(customers=[CustomerResponseModel.from_dict(c) for c in customers])
