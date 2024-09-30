import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns
import plotly.express as px
import folium
from streamlit_folium import folium_static
import json

# Set page configuration for a better look
st.set_page_config(
    page_title="Olist Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Load the data from CSV
@st.cache_data
def load_data():
    return pd.read_csv('all_data.csv')


all_data = load_data()

# Sidebar for filtering
st.sidebar.header('Filter Options')
order_status = st.sidebar.multiselect(
    'Select Order Status:',
    options=all_data['order_status'].unique(),
    default=all_data['order_status'].unique()
)

# Filter data
filtered_data = all_data[all_data['order_status'].isin(order_status)]

# Main Page Title
st.title("Olist Data Analysis")
st.markdown("This dashboard visualizes insights from Olist dataset using various visualizations.")

# Tabs for Visualizations
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Delivery Time Analysis", "📈 Purchase Frequency", "🛒 Customer Segmentation", "🌍 Geographic Analysis"])

# Visualization 1: Delivery Time Analysis
with tab1:
    # Creating the matplotlib histogram for delivery time
    st.header("Distribution of Delivery Time Across Brazil")
    fig, ax = plt.subplots(figsize=(12, 6))
    n, bins, patches = ax.hist(filtered_data['delivery_time_days'].dropna(), bins=15, edgecolor='black', color='#6A5ACD', alpha=0.75)

    # Add grid lines along the y-axis for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    # Add labels for axes
    ax.set_xlabel('Delivery Time (Days)', fontsize=14, labelpad=10)
    ax.set_ylabel('Number of Orders', fontsize=14, labelpad=10)

    # Add a title to the plot
    ax.set_title('Distribution of Delivery Time Across Brazil', fontsize=16, fontweight='bold', pad=15)

    # Adding annotations for each bar to display the count
    for i in range(len(patches)):
        height = n[i]
        if height > 0:
            ax.text(
                patches[i].get_x() + patches[i].get_width() / 2,
                height + max(n) * 0.02,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=10,
                color='black'
            )

    # Highlighting specific bins
    for patch in patches:
        if patch.get_height() > 5000:
            patch.set_facecolor('#FFA07A')
        else:
            patch.set_facecolor('#87CEFA')

    # Adding a legend to explain the bar colors
    legend_elements = [
        Patch(facecolor='#FFA07A', edgecolor='black', label='High Count (> 5000 Orders)'),
        Patch(facecolor='#87CEFA', edgecolor='black', label='Moderate Count')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12, title="Order Count Categories")

    # Adding some visual separation at the borders of the bars
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)

# Visualization 2: Purchase Frequency
with tab2:
    st.header("Frequency of Purchases by Customers in July, August, and September 2018")
    purchase_frequency = \
    filtered_data[filtered_data['order_purchase_timestamp'].str.contains('2018')].groupby('customer_id')[
        'order_id'].count()

    fig, ax = plt.subplots(figsize=(10, 6))
    n, bins, patches = plt.hist(purchase_frequency, bins=15, edgecolor='black', color='salmon', log=True)
    ax.set_xlabel("Number of Purchases (Frequency)")
    ax.set_ylabel("Number of Customers (Log Scale)")
    ax.set_title("Frequency of Purchases by Customers in Q3 2018 (Log Scale)")
    # Adding text annotations for each bar
    for i in range(len(patches)):
        height = n[i]
        if height > 0:
            ax.text(patches[i].get_x() + patches[i].get_width() / 2, height, f'{int(height)}', ha='center', va='bottom',
                    fontsize=10)
    st.pyplot(fig)

# Visualization 3: Customer Segmentation Based on Purchases
with tab3:
    st.header("Customer Segmentation Based on Purchase Frequency in 2018")
    recency = filtered_data.groupby('customer_id').agg({'order_purchase_timestamp': 'max'})
    recency['order_purchase_timestamp'] = pd.to_datetime(recency['order_purchase_timestamp'])
    recency['recency_days'] = (pd.Timestamp.now() - recency['order_purchase_timestamp']).dt.days

    # Segment data
    customer_segment = pd.cut(recency['recency_days'], bins=[0, 30, 60, 90, float('inf')],
                              labels=['New', 'Active', 'Idle', 'Lapsed'])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x=customer_segment, palette='viridis', ax=ax)
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Number of Customers")
    ax.set_title("Customer Segmentation Based on Recency Days")
    st.pyplot(fig)

# Visualization 4: Geographic Analysis with Folium
with tab4:
    st.header("Geographic Distribution of Purchases Across Brazil")

    # Load GeoJSON data
    with open('../map/brazil-states.geojson', 'r') as file:
        brazil_geo = json.load(file)

    state_purchases = filtered_data.groupby('customer_state')['order_id'].count().reset_index()
    state_purchases.columns = ['state', 'total_purchases']

    # Plotting Folium map
    m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
    folium.Choropleth(
        geo_data=brazil_geo,
        name="choropleth",
        data=state_purchases,
        columns=['state', 'total_purchases'],
        key_on="feature.properties.sigla",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Number of Purchases by State",
    ).add_to(m)

    folium_static(m)

# Conclusion and Custom Styling
st.markdown("### Conclusion")
st.write(
    "Through these visualizations, we were able to understand customer purchase behavior, delivery times, and geographic purchase patterns across Brazil.")
