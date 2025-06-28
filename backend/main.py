from fastapi import FastAPI, Query, HTTPException
from datetime import date

from models import PriceData, PriceUpdate
from supabase_client import supabase
from id_mapping import region_map, commodity_map

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Food Price API is running 🚀"}

@app.get("/data")
def get_data(
    start_date: date = Query(None),
    end_date: date = Query(None),
    region: str = Query(None),
    commodity: str = Query(None)
):
    query = supabase.table("prices").select("*")

    if region:
        region_id = region_map.get(region.strip())
        if not region_id:
            raise HTTPException(status_code=404, detail=f"Region '{region}' not found")
        query = query.eq("region_id", region_id)

    if commodity:
        commodity_id = commodity_map.get(commodity.strip())
        if not commodity_id:
            raise HTTPException(status_code=404, detail=f"Commodity '{commodity}' not found")
        query = query.eq("commodity_id", commodity_id)

    if start_date:
        query = query.gte("date", start_date.isoformat())
    if end_date:
        query = query.lte("date", end_date.isoformat())

    response = query.limit(1000).execute()
    return response.data

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
