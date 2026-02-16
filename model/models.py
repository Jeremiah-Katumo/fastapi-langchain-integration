from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from uuid import uuid4


class User(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    posts: List["Post"] = Relationship(back_populates="author")
    reviews: List["Review"] = Relationship(back_populates="user")
    
class Post(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    title: str
    content: str
    author_id: Optional[str] = Field(foreign_key="user.id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
class Product(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(index=True)
    price: float
    description: Optional[str] = None
    sku: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    category: "Category" = Relationship(back_populates="product")
    reviews: List["Review"] = Relationship(back_populates="product")
    
class Order(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: Optional[str] = Field(foreign_key="user.id")
    product_id: Optional[str] = Field(foreign_key="product.id")
    quantity: int
    total_price: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    user: "User" = Relationship(back_populates="orders")
    product: "Product" = Relationship(back_populates="orders")
    
class Category(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    products: List["Product"] = Relationship(back_populates="category")
    
class ProductCategoryLink(SQLModel, table=True):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    category_id: Optional[str] = Field(foreign_key="category.id", primary_key=True)
    category: "Category" = Relationship(back_populates="products")
    
    product_id: Optional[str] = Field(foreign_key="product.id", primary_key=True)
    product: "Product" = Relationship(back_populates="category")
    
class Review(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    rating: int
    comment: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    user_id: Optional[str] = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="reviews")
    
    product_id: Optional[str] = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="reviews")
    