import streamlit as st
import json

def parse_input(data):
    lines = data.strip().split('\n')
    gold_prices = []

    for i in range(1, len(lines), 3):  # Process in chunks of 3 lines (Country Price, Price (INR), empty line)
        country_line = lines[i].strip().split()
        country = " ".join(country_line[:-1])
        currency_price = country_line[-1].split()[-1]
        price_18k = int(lines[i+1].split()[1])
        price_22k = int(lines[i+2].split()[1])
        price_24k = int(lines[i+3].split()[1])
        
        gold_prices.append({
            "country": country,
            "currency": currency_price[:3],
            "18K": price_18k,
            "22K": price_22k,
            "24K": price_24k
        })

    return {"gold_prices": gold_prices}

def main():
    st.title("Gold Prices to JSON Converter")
    
    input_data = st.text_area("Input Data", height=300)
    
    if st.button("Convert to JSON"):
        if input_data:
            parsed_data = parse_input(input_data)
            json_data = json.dumps(parsed_data, indent=2)
            st.json(json_data)
            
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="gold_prices.json",
                mime="application/json"
            )
        else:
            st.error("Please provide input data")

if __name__ == "__main__":
    main()
