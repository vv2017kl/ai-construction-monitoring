"""
Resource & Procurement Management API Routes
Handles material inventory, resource scheduling, delivery tracking, vendor management, procurement requests, and cost tracking
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db
from models import (
    MaterialInventory, ResourceScheduling, DeliveryTracking, VendorManagement,
    ProcurementRequest, CostTracking, User, Site,
    MaterialCategory, ResourceType, UsageStatus, DeliveryStatus, 
    VendorRating, SeverityLevel
)

router = APIRouter(prefix="/api/resource-procurement", tags=["Resource & Procurement Management"])

# MATERIAL INVENTORY ENDPOINTS

@router.get("/inventory", response_model=List[dict])
def get_all_inventory(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    material_category: Optional[str] = Query(None, description="Filter by material category"),
    low_stock: Optional[bool] = Query(None, description="Filter by low stock items"),
    db: Session = Depends(get_db)
):
    """Get all material inventory with optional filtering"""
    query = db.query(MaterialInventory)
    
    if site_id:
        query = query.filter(MaterialInventory.site_id == site_id)
    
    if material_category:
        try:
            category_enum = MaterialCategory(material_category)
            query = query.filter(MaterialInventory.material_category == category_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid material category: {material_category}")
    
    if low_stock:
        # Filter items where quantity_on_hand is less than reorder_point
        query = query.filter(MaterialInventory.quantity_on_hand < MaterialInventory.reorder_point)
    
    inventory = query.order_by(MaterialInventory.material_name).all()
    return [
        {
            "id": str(i.id),
            "site_id": str(i.site_id),
            "material_name": i.material_name,
            "material_category": i.material_category.value,
            "quantity_on_hand": float(i.quantity_on_hand),
            "quantity_available": float(i.quantity_available),
            "unit_cost": float(i.unit_cost),
            "total_value": float(i.total_value),
            "reorder_point": float(i.reorder_point) if i.reorder_point else None,
            "storage_location": i.storage_location,
            "created_at": i.created_at.isoformat()
        }
        for i in inventory
    ]

@router.post("/inventory", response_model=dict)
def create_inventory_item(
    site_id: str = Query(..., description="Site ID"),
    material_name: str = Query(..., description="Material name"),
    material_category: str = Query(..., description="Material category"),
    unit_of_measure: str = Query(..., description="Unit of measure"),
    unit_cost: float = Query(..., description="Unit cost"),
    storage_condition: str = Query(..., description="Storage condition"),
    db: Session = Depends(get_db)
):
    """Create a new material inventory item"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_item = MaterialInventory(
        site_id=site_id,
        material_name=material_name,
        material_category=MaterialCategory(material_category),
        unit_of_measure=unit_of_measure,
        unit_cost=unit_cost,
        storage_condition=storage_condition
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return {
        "id": str(db_item.id),
        "material_name": db_item.material_name,
        "material_category": db_item.material_category.value,
        "created_at": db_item.created_at.isoformat()
    }

# VENDOR MANAGEMENT ENDPOINTS

@router.get("/vendors", response_model=List[dict])
def get_all_vendors(
    vendor_category: Optional[str] = Query(None, description="Filter by vendor category"),
    overall_rating: Optional[str] = Query(None, description="Filter by overall rating"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """Get all vendors with optional filtering"""
    query = db.query(VendorManagement)
    
    if vendor_category:
        query = query.filter(VendorManagement.vendor_category.ilike(f"%{vendor_category}%"))
    
    if overall_rating:
        try:
            rating_enum = VendorRating(overall_rating)
            query = query.filter(VendorManagement.overall_rating == rating_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid rating: {overall_rating}")
    
    if is_active is not None:
        query = query.filter(VendorManagement.is_active == is_active)
    
    vendors = query.order_by(VendorManagement.vendor_name).all()
    return [
        {
            "id": str(v.id),
            "vendor_name": v.vendor_name,
            "vendor_category": v.vendor_category,
            "overall_rating": v.overall_rating.value,
            "quality_score": float(v.quality_score) if v.quality_score else None,
            "delivery_performance_score": float(v.delivery_performance_score) if v.delivery_performance_score else None,
            "is_active": v.is_active,
            "is_preferred": v.is_preferred,
            "primary_contact_name": v.primary_contact_name,
            "primary_contact_email": v.primary_contact_email,
            "created_at": v.created_at.isoformat()
        }
        for v in vendors
    ]

@router.post("/vendors", response_model=dict)
def create_vendor(
    vendor_name: str = Query(..., description="Vendor name"),
    vendor_category: str = Query(..., description="Vendor category"),
    primary_contact_email: str = Query(..., description="Primary contact email"),
    db: Session = Depends(get_db)
):
    """Create a new vendor"""
    db_vendor = VendorManagement(
        vendor_name=vendor_name,
        vendor_category=vendor_category,
        primary_contact_email=primary_contact_email
    )
    
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    
    return {
        "id": str(db_vendor.id),
        "vendor_name": db_vendor.vendor_name,
        "vendor_category": db_vendor.vendor_category,
        "created_at": db_vendor.created_at.isoformat()
    }

# PROCUREMENT REQUESTS ENDPOINTS

@router.get("/procurement-requests", response_model=List[dict])
def get_all_procurement_requests(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority_level: Optional[str] = Query(None, description="Filter by priority level"),
    db: Session = Depends(get_db)
):
    """Get all procurement requests with optional filtering"""
    query = db.query(ProcurementRequest)
    
    if site_id:
        query = query.filter(ProcurementRequest.site_id == site_id)
    
    if status:
        query = query.filter(ProcurementRequest.status == status)
    
    if priority_level:
        try:
            priority_enum = SeverityLevel(priority_level)
            query = query.filter(ProcurementRequest.priority_level == priority_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid priority level: {priority_level}")
    
    requests = query.order_by(ProcurementRequest.created_at.desc()).all()
    return [
        {
            "id": str(r.id),
            "site_id": str(r.site_id),
            "request_number": r.request_number,
            "request_type": r.request_type,
            "priority_level": r.priority_level.value,
            "requested_by": str(r.requested_by),
            "status": r.status,
            "approval_status": r.approval_status,
            "required_delivery_date": r.required_delivery_date.isoformat(),
            "total_estimated_cost": float(r.total_estimated_cost) if r.total_estimated_cost else None,
            "created_at": r.created_at.isoformat()
        }
        for r in requests
    ]

@router.post("/procurement-requests", response_model=dict)
def create_procurement_request(
    site_id: str = Query(..., description="Site ID"),
    request_number: str = Query(..., description="Request number"),
    request_type: str = Query(..., description="Request type"),
    requested_by: str = Query(..., description="Requester user ID"),
    justification: str = Query(..., description="Justification"),
    required_delivery_date: str = Query(..., description="Required delivery date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Create a new procurement request"""
    # Verify site and requester exist
    site = db.query(Site).filter(Site.id == site_id).first()
    requester = db.query(User).filter(User.id == requested_by).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not requester:
        raise HTTPException(status_code=404, detail="Requester not found")
    
    # Parse delivery date
    try:
        delivery_date = datetime.strptime(required_delivery_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    db_request = ProcurementRequest(
        site_id=site_id,
        request_number=request_number,
        request_type=request_type,
        requested_by=requested_by,
        justification=justification,
        required_delivery_date=delivery_date,
        items_requested=[]  # Empty items initially
    )
    
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    return {
        "id": str(db_request.id),
        "request_number": db_request.request_number,
        "status": db_request.status,
        "created_at": db_request.created_at.isoformat()
    }

# DELIVERY TRACKING ENDPOINTS

@router.get("/deliveries", response_model=List[dict])
def get_all_deliveries(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    status: Optional[str] = Query(None, description="Filter by delivery status"),
    db: Session = Depends(get_db)
):
    """Get all deliveries with optional filtering"""
    query = db.query(DeliveryTracking)
    
    if site_id:
        query = query.filter(DeliveryTracking.site_id == site_id)
    
    if status:
        try:
            status_enum = DeliveryStatus(status)
            query = query.filter(DeliveryTracking.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    deliveries = query.order_by(DeliveryTracking.scheduled_delivery_date.desc()).all()
    return [
        {
            "id": str(d.id),
            "site_id": str(d.site_id),
            "delivery_number": d.delivery_number,
            "status": d.status.value,
            "scheduled_delivery_date": d.scheduled_delivery_date.isoformat(),
            "actual_delivery_date": d.actual_delivery_date.isoformat() if d.actual_delivery_date else None,
            "carrier_name": d.carrier_name,
            "tracking_number": d.tracking_number,
            "total_items_count": d.total_items_count,
            "on_time_delivery": d.on_time_delivery,
            "created_at": d.created_at.isoformat()
        }
        for d in deliveries
    ]

@router.post("/deliveries", response_model=dict)
def create_delivery(
    site_id: str = Query(..., description="Site ID"),
    delivery_number: str = Query(..., description="Delivery number"),
    scheduled_delivery_date: str = Query(..., description="Scheduled delivery date (YYYY-MM-DD)"),
    carrier_name: Optional[str] = Query(None, description="Carrier name"),
    db: Session = Depends(get_db)
):
    """Create a new delivery tracking record"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Parse delivery date
    try:
        delivery_date = datetime.strptime(scheduled_delivery_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    db_delivery = DeliveryTracking(
        site_id=site_id,
        delivery_number=delivery_number,
        scheduled_delivery_date=delivery_date,
        carrier_name=carrier_name,
        items_manifest=[]  # Empty manifest initially
    )
    
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    
    return {
        "id": str(db_delivery.id),
        "delivery_number": db_delivery.delivery_number,
        "scheduled_delivery_date": db_delivery.scheduled_delivery_date.isoformat(),
        "created_at": db_delivery.created_at.isoformat()
    }

# COST TRACKING ENDPOINTS

@router.get("/costs", response_model=List[dict])
def get_all_costs(
    site_id: Optional[str] = Query(None, description="Filter by site ID"),
    cost_category: Optional[str] = Query(None, description="Filter by cost category"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get all cost tracking records with optional filtering"""
    query = db.query(CostTracking)
    
    if site_id:
        query = query.filter(CostTracking.site_id == site_id)
    
    if cost_category:
        query = query.filter(CostTracking.cost_category.ilike(f"%{cost_category}%"))
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d").date()
            query = query.filter(CostTracking.transaction_date >= from_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_from format. Use YYYY-MM-DD")
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, "%Y-%m-%d").date()
            query = query.filter(CostTracking.transaction_date <= to_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_to format. Use YYYY-MM-DD")
    
    costs = query.order_by(CostTracking.transaction_date.desc()).all()
    return [
        {
            "id": str(c.id),
            "site_id": str(c.site_id),
            "cost_category": c.cost_category,
            "transaction_date": c.transaction_date.isoformat(),
            "transaction_type": c.transaction_type,
            "amount": float(c.amount),
            "description": c.description,
            "authorized_by": str(c.authorized_by),
            "approval_status": c.approval_status,
            "created_at": c.created_at.isoformat()
        }
        for c in costs
    ]

@router.post("/costs", response_model=dict)
def create_cost_entry(
    site_id: str = Query(..., description="Site ID"),
    cost_category: str = Query(..., description="Cost category"),
    transaction_date: str = Query(..., description="Transaction date (YYYY-MM-DD)"),
    transaction_type: str = Query(..., description="Transaction type"),
    amount: float = Query(..., description="Amount"),
    description: str = Query(..., description="Description"),
    authorized_by: str = Query(..., description="Authorizer user ID"),
    entered_by: str = Query(..., description="Entry user ID"),
    db: Session = Depends(get_db)
):
    """Create a new cost tracking entry"""
    # Verify site, authorizer, and entry user exist
    site = db.query(Site).filter(Site.id == site_id).first()
    authorizer = db.query(User).filter(User.id == authorized_by).first()
    entry_user = db.query(User).filter(User.id == entered_by).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    if not authorizer:
        raise HTTPException(status_code=404, detail="Authorizer not found")
    if not entry_user:
        raise HTTPException(status_code=404, detail="Entry user not found")
    
    # Parse transaction date
    try:
        trans_date = datetime.strptime(transaction_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    db_cost = CostTracking(
        site_id=site_id,
        cost_category=cost_category,
        transaction_date=trans_date,
        transaction_type=transaction_type,
        amount=amount,
        description=description,
        authorized_by=authorized_by,
        entered_by=entered_by
    )
    
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    
    return {
        "id": str(db_cost.id),
        "cost_category": db_cost.cost_category,
        "amount": float(db_cost.amount),
        "transaction_date": db_cost.transaction_date.isoformat(),
        "created_at": db_cost.created_at.isoformat()
    }