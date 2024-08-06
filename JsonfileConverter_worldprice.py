import os
import streamlit as st
import json
import re
from datetime import datetime
from pymongo import MongoClient
from bson.json_util import dumps
from urllib.parse import quote_plus

def generate_filename(metal_type):
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{metal_type[0].upper()}_{today}.json"

def table_to_json(table_data):
    lines = table_data.strip().split('\n')
    gold_prices = []
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 5:  # Ensure we have enough parts
            country = ' '.join(parts[:-4])  # Join all parts except the last 4
            currency = parts[-4]
            price_18k = parts[-3]
            price_22k = parts[-2]
            price_24k = parts[-1]
            
            gold_price = {
                "country": country,
                "currency": currency,
                "18K": float(price_18k),
                "22K": float(price_22k),
                "24K": float(price_24k)
            }
            gold_prices.append(gold_price)
    
    return {"gold_prices": gold_prices}

def upload_to_mongodb(json_data):
    username = "technoresult"
    password = "Domain@202!"
    cluster = "goldcalculator-01.lfvxjyn.mongodb.net"
    
    escaped_username = quote_plus(username)
    escaped_password = quote_plus(password)
    
    mongo_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster}/?retryWrites=true&w=majority&appName=GoldCalculator-01"
    
    client = MongoClient(mongo_uri)
    db = client["your_database_name"]
    collection = db["international_gold_prices"]

    filename = generate_filename("Gold")

    document = {
        "filename": filename,
        "data": json_data,
        "timestamp": datetime.utcnow()
    }

    result = collection.insert_one(document)
    return result.inserted_id

st.title("International Gold Price Data Converter")

if 'json_string' not in st.session_state:
    st.session_state.json_string = ""

st.write("Paste your international gold price data below. The format should be:")
st.code("Country Currency 18K_price 22K_price 24K_price")

table_data = st.text_area("Paste your data here:", height=200)

if st.button("Convert to JSON"):
    if table_data:
        json_data = table_to_json(table_data)
        
        st.write("Converted JSON data:")
        st.json(json_data, expanded=True)
        
        st.session_state.json_string = json.dumps(json_data, indent=2, ensure_ascii=False).encode('utf-8').decode('utf-8')
        filename = generate_filename("Gold")
        st.download_button(
            label="Download JSON",
            file_name=filename,
            mime="application/json",
            data=st.session_state.json_string,
        )
    else:
        st.warning("Please paste some data before converting.")

st.write("Upload to MongoDB Atlas")

with st.form(key='mongodb_upload_form'):
    submit_button = st.form_submit_button(label="Upload to MongoDB Atlas")

if submit_button:
    if st.session_state.json_string:
        json_data = json.loads(st.session_state.json_string)
        try:
            inserted_id = upload_to_mongodb(json_data)
            st.success(f"Data uploaded successfully to MongoDB Atlas! Document ID: {inserted_id}")
        except Exception as e:
            st.error(f"Failed to upload data to MongoDB Atlas. Error: {str(e)}")
    else:
        st.warning("Please convert data to JSON before uploading.")

st.write("Note: Make sure your data is in the correct format. Each country should be on a new line.")
