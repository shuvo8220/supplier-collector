"""
MongoDB Database Configuration and Schema
"""
from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB Connection
# For local development, use local MongoDB
# For production, use MongoDB Atlas connection string
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://suvo_admin:pqAGAboOYjug7shZ@cluster0.7r3fteh.mongodb.net/supplier_collector?retryWrites=true&w=majority&appName=Cluster0')
DB_NAME = 'supplier_collector'

def get_db():
    """Get database connection"""
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def init_db():
    """Initialize database with indexes"""
    db = get_db()
    
    # Create indexes for better query performance
    db.suppliers.create_index([("company", 1)], unique=True)
    db.suppliers.create_index([("created_at", -1)])
    db.products.create_index([("supplier_id", 1)])
    db.samples.create_index([("supplier_id", 1)])
    db.documents.create_index([("supplier_id", 1)])
    db.commercial.create_index([("supplier_id", 1)])
    db.contacts.create_index([("supplier_id", 1)])
    db.interviews.create_index([("supplier_id", 1)])
    
    print("✓ Database initialized with indexes")

# Collection Schemas (for reference)

SUPPLIER_SCHEMA = {
    "_id": "ObjectId",
    "company": "string",  # Unique company name
    "date": "date",
    "collected_by": "string",
    "est_year": "number",
    "employees": "number",
    "business_type": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}

PRODUCT_SCHEMA = {
    "_id": "ObjectId",
    "supplier_id": "ObjectId",  # Reference to supplier
    "product_type": "string",
    "product_type_custom": "string",
    "main_products": ["array of strings"],
    "main_products_other": "string",
    "material": "string",
    "material_source": "string",  # NEW: Where material comes from
    "material_quality": "string",  # NEW: Material quality details
    "material_supplier_company": "string",  # NEW: Material supplier name
    "product_working_status": "string",  # NEW: Working or not
    "product_origin": "string",  # NEW: Where product comes from
    "custom": "string",
    "custom_details": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}

SAMPLE_SCHEMA = {
    "_id": "ObjectId",
    "supplier_id": "ObjectId",
    "sample_available": "string",
    "sample_details": "string",
    "sample_type": "string",  # NEW: Type of sample
    "sample_quality": "string",  # NEW: Quality rating
    "manufacture_date": "date",  # NEW: When sample was made
    "photo_date": "date",  # NEW: When photo was taken
    "sample_images": ["array of image paths"],  # NEW: Sample pictures
    "created_at": "datetime",
    "updated_at": "datetime"
}

DOCUMENT_SCHEMA = {
    "_id": "ObjectId",
    "supplier_id": "ObjectId",
    "tin_bin": "string",
    "tin_provided": "boolean",  # NEW: True if provided, False if opted out
    "trade_license": "string",
    "trade_license_no": "string",
    "trade_license_image": "string",  # NEW: Scan/photo of license
    "bsti": "string",
    "bsti_image": "string",  # NEW: BSTI certificate image
    "export_exp": "string",
    "company_authenticity_verified": "boolean",  # NEW
    "verification_notes": "string",  # NEW
    "created_at": "datetime",
    "updated_at": "datetime"
}

COMMERCIAL_SCHEMA = {
    "_id": "ObjectId",
    "supplier_id": "ObjectId",
    "moq": "string",
    "capacity_monthly": "string",
    "capacity_per_order_max": "string",  # NEW: Highest quantity in one order
    "lead_time": "number",
    "price_list_available": "string",
    "price_list_details": "string",
    "price_list_images": ["array of image paths"],  # NEW: Price list pics
    "price_range": "string",  # NEW: Approximate range if no list
    "opening_time": "string",  # NEW: Business opening time
    "closing_time": "string",  # NEW: Business closing time
    "delivery_cost": "string",  # NEW: Delivery cost details
    "vehicle_available": "string",  # NEW: Yes/No/Type
    "capacity_per_load": "string",  # NEW: How many in one load (loot)
    "created_at": "datetime",
    "updated_at": "datetime"
}

CONTACT_SCHEMA = {
    "_id": "ObjectId",
    "supplier_id": "ObjectId",
    "contacts": [
        {
            "name": "string",
            "designation": "string",
            "phone": "string",
            "whatsapp": "string"
        }
    ],
    "email": "string",
    "facebook": "string",
    "website": "string",
    "factory_addr": "string",
    "factory_map_link": "string",
    "office_addr": "string",
    "office_map_link": "string",
    "factory_own": "string",
    "delivery": ["array of strings"],
    "created_at": "datetime",
    "updated_at": "datetime"
}

INTERVIEW_SCHEMA = {
    "_id": "ObjectId",
    "supplier_id": "ObjectId",
    "questions": {
        "q1": "string",
        "q2": "string",
        # ... up to q27
    },
    "interest": "string",
    "next_action": "string",
    "notes": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}

MEDIA_SCHEMA = {
    "_id": "ObjectId",
    "supplier_id": "ObjectId",
    "photo_product": "string",
    "product_images": ["array of image paths"],  # NEW: Product photos
    "photo_factory": "string",
    "factory_images": ["array of image paths"],  # NEW: Factory photos
    "catalog": "string",
    "catalog_images": ["array of image paths"],  # NEW: Catalog images
    "consent": ["array of strings"],
    "signature": "string",
    "sign_date": "date",
    "created_at": "datetime",
    "updated_at": "datetime"
}

if __name__ == "__main__":
    # Test connection
    try:
        db = get_db()
        print(f"✓ Connected to MongoDB: {DB_NAME}")
        print(f"✓ Collections: {db.list_collection_names()}")
        init_db()
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        print("\n💡 Make sure MongoDB is running locally:")
        print("   Download: https://www.mongodb.com/try/download/community")
        print("   Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas")
