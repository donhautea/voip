import streamlit as st
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(layout="wide")  # Set layout to wide

# Automatically load directory.csv without a button click
def load_directory_csv():
    csv_path = "directory.csv"  # Replace with the actual path to directory.csv
    directory_df = pd.read_csv(csv_path)

    # Drop the first column (if it's an unnamed index column) and reset index
    if directory_df.columns[0] == 'Unnamed: 0':
        directory_df = directory_df.drop(directory_df.columns[0], axis=1)
    else:
        directory_df = directory_df.drop(directory_df.columns[0], axis=1)

    directory_df = directory_df.reset_index(drop=True)
    return directory_df

# Function to display directory.csv and provide filter functionality
def display_directory_csv_with_filters(directory_df, show_all_data):
    # Display the loaded directory.csv if the checkbox is checked
    if show_all_data:
        st.write("### VOIP Dataset (All Data)")
        st.dataframe(directory_df)

    # Allow filtering based on the directory.csv content
    column_options = directory_df.columns.tolist()
    
    # Check if "Display Name" exists in the column options and set it as default
    default_column = "Display Name" if "Display Name" in column_options else column_options[0]
    
    filter_column = st.sidebar.selectbox("Select a column to filter in ", column_options, index=column_options.index(default_column), key="directory_column")
    filter_values = st.sidebar.multiselect(f"Select values to filter by in '{filter_column}'", directory_df[filter_column].unique(), key="directory_filter_values")

    # Automatically display filtered results
    if filter_values:
        filtered_directory_df = directory_df[directory_df[filter_column].isin(filter_values)]
        st.write("### VOIP Filtered Results")
        st.dataframe(filtered_directory_df)
    else:
        st.warning("Please select at least one value to filter.")

# Main function to create the Streamlit app
def main():
    # Sidebar with filter options for the directory.csv
    st.sidebar.title("Directory CSV Filter Tool")
    
    # Automatically load directory.csv
    directory_df = load_directory_csv()

    # Checkbox to show or hide all data from directory.csv
    show_all_data = st.sidebar.checkbox("Show All VOIP Data", value=False)

    # Display the directory.csv with filter options, controlled by the checkbox
    st.sidebar.markdown("### Directory Data")
    display_directory_csv_with_filters(directory_df, show_all_data)

if __name__ == "__main__":
    main()
