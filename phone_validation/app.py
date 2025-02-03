import streamlit as st
import requests
import pandas as pd
import json
import io

# Replace with your Neutrino API credentials
USER_ID = "Tohka"
API_KEY = "On2I9wPkS2aJYflMX99umTM0XfbTFL4LH3JoHpZVc0gxuV7n"

# API endpoint
url = "https://neutrinoapi.net/phone-validate"

def phone_validation_app():
    st.title("📱 Phone Number Validator")

    # User input fields
    number = st.text_input("Enter the phone number (e.g., +6495552000):")

    # Button to trigger validation
    if st.button("✅ Validate Phone Number"):
        if number:
            params = {
                "number": number,
            }

            headers = {
                "User-ID": USER_ID,
                "API-Key": API_KEY
            }

            # Make the POST request
            response = requests.post(url, headers=headers, data=params)

            if response.status_code == 200:
                data = response.json()

                # Rearrange the results
                rearranged_data = {
                    "✔️ Valid": data.get("valid"),
                    "📞 Type": data.get("type"),
                    "🌍 Country": data.get("country"),
                    "📍 Location": data.get("location"),
                    "🔢 International Number": data.get("international-number"),
                    "🔢 Local Number": data.get("local-number"),
                    "🇨🇺 Country Code": data.get("country-code"),
                    "💱 Currency Code": data.get("currency-code"),
                    "📡 International Calling Code": data.get("international-calling-code"),
                    "📱 Is Mobile": data.get("is-mobile"),
                    "📶 Carrier Service Provider": data.get("prefix-network")
                }

                # Display rearranged data in a box without background color
                st.subheader("Phone Validation Results:")
                st.markdown(
                    """<div style="border: 2px solid #ddd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    """ + "<br>".join([f"<b>{key}:</b> {value}" for key, value in rearranged_data.items()]) + "</div>",
                    unsafe_allow_html=True
                )

                # Check additional country details from CSV
                csv_file = "countries/countries.csv"  # Replace with your actual CSV file path
                try:
                    country_data = pd.read_csv(csv_file, delimiter=";")
                    country_info = country_data[country_data['Country Name'] == data.get("country")]

                    if not country_info.empty:
                        st.subheader("Additional Country Details (CSV):")
                        st.markdown(
                            """<div style="border: 2px solid #ddd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                            """ + "<br>".join([f"<b>{col}:</b> {country_info.iloc[0][col]}" for col in country_info.columns]) + "</div>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.info("No additional details found for this country in the CSV file.")

                except FileNotFoundError:
                    st.error("Country details CSV file not found.")

                # Convert results to CSV format
                df = pd.DataFrame([rearranged_data])
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, sep=';')
                csv_data = csv_buffer.getvalue()

                # Add some space before the download button
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv_data,
                    file_name="phone_validation_results.csv",
                    mime="text/csv"
                )
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        else:
            st.warning("Please enter a valid phone number.")

# Define the main function for integration
def main():
    phone_validation_app()

if __name__ == "__main__":
    main()
