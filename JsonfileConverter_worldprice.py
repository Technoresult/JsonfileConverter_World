import streamlit as st
import json

def parse_input(data):
    lines = data.strip().split('\n')
    gold_prices = []
    
    country_prices = {}

    for i in range(0, len(lines), 3):
        parts = lines[i].split()
        country = " ".join(parts[:-1])
        currency = parts[-1][:3]
        price = int(parts[-1][3:])
        if country not in country_prices:
            country_prices[country] = {"currency": currency, "18K": None, "22K": None, "24K": None}
        carat_value = i // len(lines) * 3 + 18
        country_prices[country][f"{carat_value}K"] = price

    for country, prices in country_prices.items():
        gold_prices.append({
            "country": country,
            "currency": prices["currency"],
            "18K": prices["18K"],
            "22K": prices["22K"],
            "24K": prices["24K"]
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
