import streamlit as st
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(layout="wide")  # Set layout to wide

# Load the CSV file with caching
@st.cache_data
def load_data(file_path):
    # Load data and drop the first column (index 0)
    df = pd.read_csv(file_path)
    if df.columns[0] == 'Unnamed: 0':  # Sometimes index columns are named 'Unnamed: 0'
        df = df.drop(df.columns[0], axis=1)
    else:
        df = df.drop(df.columns[0], axis=1)
    return df

# Main function to create the Streamlit app
def main():
    # Sidebar with upload and filter options
    st.sidebar.title("CSV Filter Tool")
    
    # Upload CSV file
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Load data from CSV and drop the first column
        df = load_data(uploaded_file)

        # Display the entire dataframe by default in the main window
        st.write("### All Data")
        st.write(df)

        # Default column to filter set to 'Display Name'
        column_options = df.columns.tolist()
        default_column = "Display Name" if "Display Name" in column_options else column_options[0]
        column_to_filter = st.sidebar.selectbox("Select a column to filter", column_options, index=column_options.index(default_column))

        # Allow multiple search values
        search_values = st.sidebar.multiselect(f"Search value(s) in '{column_to_filter}'", df[column_to_filter].unique())

        # If search values are selected, filter the dataframe
        if search_values:
            filtered_df = df[df[column_to_filter].isin(search_values)]
            st.write("### Filtered Results")
            st.write(filtered_df)

            # Display message about the number of matching rows
            if not filtered_df.empty:
                st.success(f"Found {len(filtered_df)} matching rows.")
            else:
                st.warning("No matching rows found.")

if __name__ == "__main__":
    main()
