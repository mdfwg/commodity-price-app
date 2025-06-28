from fastapi import FastAPI, Query, HTTPException
from datetime import date
from typing import List, Optional

from models import PriceData, PriceUpdate
from supabase_client import supabase
from id_mapping import region_map, commodity_map

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Food Price API is running 🚀"}

@app.get("/data")
def get_data(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    regions: Optional[List[str]] = Query(None, description="List of regions to filter by"),
    commodities: Optional[List[str]] = Query(None, description="List of commodities to filter by"),
    limit: int = Query(10000, description="Maximum number of records to return")
):
    query = supabase.table("prices").select("*")

    # Handle multiple regions
    if regions:
        region_ids = []
        for region in regions:
            region_id = region_map.get(region.strip())
            if not region_id:
                raise HTTPException(status_code=404, detail=f"Region '{region}' not found")
            region_ids.append(region_id)
        
        if len(region_ids) == 1:
            query = query.eq("region_id", region_ids[0])
        else:
            query = query.in_("region_id", region_ids)

    # Handle multiple commodities
    if commodities:
        commodity_ids = []
        for commodity in commodities:
            commodity_id = commodity_map.get(commodity.strip())
            if not commodity_id:
                raise HTTPException(status_code=404, detail=f"Commodity '{commodity}' not found")
            commodity_ids.append(commodity_id)
        
        if len(commodity_ids) == 1:
            query = query.eq("commodity_id", commodity_ids[0])
        else:
            query = query.in_("commodity_id", commodity_ids)

    if start_date:
        query = query.gte("date", start_date.isoformat())
    if end_date:
        query = query.lte("date", end_date.isoformat())

    response = query.limit(limit).execute()
    return response.data

@app.get("/data/count")
def get_data_count(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    regions: Optional[List[str]] = Query(None, description="List of regions to filter by"),
    commodities: Optional[List[str]] = Query(None, description="List of commodities to filter by")
):
    """Get the total count of records matching the filters"""
    query = supabase.table("prices").select("id")

    # Handle multiple regions
    if regions:
        region_ids = []
        for region in regions:
            region_id = region_map.get(region.strip())
            if not region_id:
                raise HTTPException(status_code=404, detail=f"Region '{region}' not found")
            region_ids.append(region_id)
        
        if len(region_ids) == 1:
            query = query.eq("region_id", region_ids[0])
        else:
            query = query.in_("region_id", region_ids)

    # Handle multiple commodities
    if commodities:
        commodity_ids = []
        for commodity in commodities:
            commodity_id = commodity_map.get(commodity.strip())
            if not commodity_id:
                raise HTTPException(status_code=404, detail=f"Commodity '{commodity}' not found")
            commodity_ids.append(commodity_id)
        
        if len(commodity_ids) == 1:
            query = query.eq("commodity_id", commodity_ids[0])
        else:
            query = query.in_("commodity_id", commodity_ids)

    if start_date:
        query = query.gte("date", start_date.isoformat())
    if end_date:
        query = query.lte("date", end_date.isoformat())

    response = query.execute()
    return {"total_count": len(response.data)}

@app.post("/data")
def add_data(item: PriceData):
    try:
        region_id = region_map.get(item.region.strip())
        commodity_id = commodity_map.get(item.commodity.strip())

        if not region_id or not commodity_id:
            raise HTTPException(status_code=404, detail="Region or commodity not found")

        data = {
            "region_id": region_id,
            "commodity_id": commodity_id,
            "date": item.date.isoformat(),
            "price": item.price,
            "created_by": item.created_by
        }

        insert = supabase.table("prices").insert(data).execute()
        return {"status": "success", "data": insert.data}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/data/{price_id}")
def update_price(price_id: str, item: PriceUpdate):
    try:
        update_data = {}

        if item.region:
            region_id = region_map.get(item.region.strip())
            if not region_id:
                raise HTTPException(status_code=404, detail="Region not found")
            update_data["region_id"] = region_id

        if item.commodity:
            commodity_id = commodity_map.get(item.commodity.strip())
            if not commodity_id:
                raise HTTPException(status_code=404, detail="Commodity not found")
            update_data["commodity_id"] = commodity_id

        if item.date:
            update_data["date"] = item.date.isoformat()

        if item.price is not None:
            update_data["price"] = item.price

        if item.created_by:
            update_data["created_by"] = item.created_by

        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")

        updated = supabase.table("prices").update(update_data).eq("id", price_id).execute()
        return {"status": "success", "data": updated.data}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/data/{price_id}")
def delete_price(price_id: str):
    try:
        deleted = supabase.table("prices").delete().eq("id", price_id).execute()
        return {"status": "success", "data": deleted.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
