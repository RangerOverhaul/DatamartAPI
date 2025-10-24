from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix = "/sales", tags = ["sales"])

@router.get("/by-employee")
async def get_sales_by_employee(key_employee: str, date_start: str, date_end: str):
    # TODO: Implement the logic to get sales by employee
    pass

@router.get("/by-product")
async def get_sales_by_product(key_product: str, date_start: str, date_end: str):
    # TODO: Implement the logic to get sales by product
    pass

@router.get("/by-store")
async def get_sales_by_store(key_store: str, date_start: str, date_end: str):
    # TODO: Implement the logic to get sales by store
    pass

@router.get("/store-summary")
async def get_sales_store_summary(key_store: str = None):
    # TODO: Implement the logic to get sales store summary
    pass

@router.get("/product-summary")
async def get_sales_product_summary(key_product: str = None):
    # TODO: Implement the logic to get sales product summary
    pass

@router.get("/employee-summary")
async def get_sales_employee_summary(key_employee: str = None):
    # TODO: Implement the logic to get sales employee summary
    pass
