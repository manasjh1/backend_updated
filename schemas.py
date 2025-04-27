# backend/schemas.py

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

# --- Base Schemas ---
class Phone(BaseModel):
    mobile_number: str = Field(..., min_length=10, max_length=10, pattern=r'^\d{10}$')

class SuccessResponse(BaseModel):
    Status: str
    Details: str

class RegisterSuccessResponse(BaseModel):
    success: bool
    farmer_id: str

# --- Token Schemas (used by auth_utils) ---
class TokenData(BaseModel):
    sub: Optional[str] = None  # Subject (mobile for farmer, email for admin)
    type: Optional[str] = None  # 'farmer' or 'admin'
    user_id: Optional[str] = None  # Optional user ID

# --- Farmer Schemas ---
class FarmerCreate(BaseModel):
    # Accept camelCase from frontend using aliases
    mobile: str = Field(..., min_length=10, max_length=10, pattern=r'^\d{10}$')
    otp: str = Field(..., min_length=6, max_length=6, pattern=r'^\d{6}$')
    full_name: str = Field(..., alias='fullName', min_length=2, max_length=100)

    aadhaar_number: Optional[str] = Field(None, alias='aadhaarNumber', max_length=12)
    crop_type: Optional[str] = Field(None, alias='cropType', max_length=50)
    cultivation_area: Optional[str] = Field(None, alias='cultivationArea')
    cultivation_unit: Optional[str] = Field(None, alias='cultivationUnit', max_length=20)
    approximate_produce: Optional[str] = Field(None, alias='approximateProduce', max_length=100)
    pin_code: Optional[str] = Field(None, alias='pinCode', min_length=6, max_length=6, pattern=r'^\d{6}$')
    village: Optional[str] = Field(None, alias='village', max_length=100)
    district: Optional[str] = Field(None, alias='district', max_length=100)
    state: Optional[str] = Field(None, alias='state', max_length=50)
    geo_location: Optional[Dict[str, float]] = Field(None, alias='geoLocation')  # {"lat": float, "lng": float}

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    # --- Validators to handle empty fields ---
    @validator(
        'aadhaar_number', 'crop_type', 'cultivation_area', 'cultivation_unit',
        'approximate_produce', 'pin_code', 'village', 'district', 'state',
        pre=True, always=True
    )
    def empty_string_to_none(cls, v):
        """Convert empty string fields to None."""
        if isinstance(v, str) and v.strip() == "":
            return None
        return v

    @validator('geo_location', pre=True, always=True)
    def empty_geo_to_none(cls, v):
        """Convert empty geoLocation dict to None or validate correct format."""
        if v in ({}, None):
            return None
        if not isinstance(v, dict) or "lat" not in v or "lng" not in v:
            raise ValueError("Invalid geoLocation format. Expecting {'lat': float, 'lng': float}.")
        return v

class FarmerOtpLogin(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=10, pattern=r'^\d{10}$')
    otp: str = Field(..., min_length=6, max_length=6, pattern=r'^\d{6}$')

class FarmerProfile(BaseModel):
    id: str
    full_name: str
    mobile_number: str  # snake_case
    aadhaar_number: Optional[str] = None
    crop_type: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pin_code: Optional[str] = None
    cultivation_area: Optional[float] = None
    cultivation_unit: Optional[str] = None
    approximate_produce: Optional[str] = None
    geo_location: Optional[Dict[str, float]] = None
    registered_at: datetime
    status: Optional[str] = None
    role: Optional[str] = None

    class Config:
        orm_mode = True

# --- Admin Schemas ---
class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminProfile(BaseModel):
    id: str  # Assuming Admin ID is string
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        orm_mode = True
