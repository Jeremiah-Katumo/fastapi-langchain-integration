from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    
class UserCreate(UserBase):
    created_at: Optional[datetime] = None
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    updated_at: Optional[datetime] = None
    
class UserRead(UserBase):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
        
class PostBase(BaseModel):
    title: str
    content: str
    
class PostCreate(PostBase):
    created_at: Optional[datetime] = None
    
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    updated_at: Optional[datetime] = None
    
class PostRead(PostBase):
    id: Optional[str] = None
    author_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
        
class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    sku: Optional[str] = None
    
class ProductCreate(ProductBase):
    created_at: Optional[datetime] = None
    
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    sku: Optional[str] = None
    updated_at: Optional[datetime] = None
    
class ProductRead(ProductBase):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
        
class OrderBase(BaseModel):
    user_id: Optional[str] = None
    product_id: Optional[str] = None
    quantity: int
    total_price: float
    
class OrderCreate(OrderBase):
    created_at: Optional[datetime] = None
    
class OrderUpdate(BaseModel):
    user_id: Optional[str] = None
    product_id: Optional[str] = None
    quantity: Optional[int] = None
    total_price: Optional[float] = None
    updated_at: Optional[datetime] = None
    
class OrderRead(OrderBase):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
        
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    
class CategoryCreate(CategoryBase):
    created_at: Optional[datetime] = None
    
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    updated_at: Optional[datetime] = None
    
class CategoryRead(CategoryBase):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
        
class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None
    
class ReviewCreate(ReviewBase):
    created_at: Optional[datetime] = None
    
class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None
    updated_at: Optional[datetime] = None
    
class ReviewRead(ReviewBase):
    id: Optional[str] = None
    user_id: Optional[str] = None
    product_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True