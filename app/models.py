from datetime import datetime
from enum import Enum, IntEnum
from typing import Optional
from pydantic import BaseModel, EmailStr

class CpfStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=r'\d{11}'
        )

    @classmethod
    def validate(cls, v):

        if not isinstance(v, str):
            raise TypeError("string required")

        numbers = [int(digit) for digit in v if digit.isdigit()]
        if len(numbers) != 11 or len(set(numbers)) == 1:
            raise ValueError("invalid cpf format.")

        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            raise ValueError("cpf doesn't exist")
        
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            raise ValueError("cpf doesn't exist")
        
        return cls(v)

class Sex(str, Enum):
    Male = "M"
    Female = "F"

class BloodGroup(str, Enum):
    APositive = "A+"
    BPositive = "B+"
    ABPositive = "AB+"
    OPositive = "O+"
    ANegative = "A-"
    BNegative = "B-"
    ABNegative = "AB-"
    ONegative = "O-"

class PatientBase(BaseModel):
    weight: Optional[int]
    height: Optional[int]
    blood_group: Optional[BloodGroup]
    email: Optional[EmailStr]

class PatientCreate(PatientBase):
    cpf: CpfStr
    first_name: str
    last_name: str
    birth_date: datetime
    sex: Sex
    tel: str
    emergency_tel: str

class PatientUpdate(PatientBase):
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[datetime]
    sex: Optional[Sex]
    tel: Optional[str]
    emergency_tel: Optional[str]