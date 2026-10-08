from __future__ import annotations

from typing import Optional
from sqlmodel import Field

from pdf_parsing.core.models import BaseRecord

class GovernmentBudgetHeader(BaseRecord, table=True):
    __tablename__ = "government_budget_header"
    
    fiscal_year: Optional[str] = Field(default=None, description="The fiscal year for the budget (e.g. 2027)")
    total_national_budget: Optional[float] = Field(default=None, description="The total proposed national budget amount")
    document_title: Optional[str] = Field(default=None, description="The official title of the document")
    
class DepartmentBudget(BaseRecord, table=True):
    __tablename__ = "department_budget"
    
    header_id: Optional[int] = Field(default=None, foreign_key="government_budget_header.id")
    department_name: Optional[str] = Field(default=None, description="Name of the government department or agency")
    total_appropriation: Optional[float] = Field(default=None, description="Total budget appropriation for the department")
    personnel_services: Optional[float] = Field(default=None, description="Budget allocated for Personnel Services (PS)")
    capital_outlays: Optional[float] = Field(default=None, description="Budget allocated for Capital Outlays (CO)")
