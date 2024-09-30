import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns
import plotly.express as px
import folium
from streamlit_folium import folium_static
import json
from pathlib import Path
import datetime

# Set page configuration for a better look
st.set_page_config(
    page_title="Brazilian E-Commerce Public Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the data paths using pathlib for the current directory
base_path = Path(__file__).parent  # Get the current script's directory


# Load all_data.csv
@st.cache_data
def load_data():
    file_path = base_path / "all_data.csv"  # Construct the full path to all_data.csv
    return pd.read_csv(file_path)


all_data = load_data()


# Load rfm_data.csv
@st.cache_data
def load_rfm_data():
    file_path = base_path / "rfm_data.csv"  # Construct the full path to rfm_data.csv
    return pd.read_csv(file_path)


rfm_data = load_rfm_data()

# Conclusion and Custom Styling
conclusions = {
    "tab1": """
    **Example Question: What is the average delivery time of products to customers across Brazil?**

    The average delivery time for products across Brazil is primarily between **5 to 15 days**, with the highest concentration in the **5-10 day range**. However, there is a noticeable decline beyond 15 days, indicating longer delays for some orders. This suggests that most deliveries are on time, but there is room for improvement in reducing longer delivery times to ensure consistent service and higher customer satisfaction.
    """,
    "tab2": """
    **Example Question: When was the last time a customer made a purchase at Olist in the past year (2018)?**

    The recency distribution shows that a large number of customers made their last purchase between **100 and 400 days** ago, with the highest peak at about **300 to 400 days**. As time passes beyond 400 days, there is a noticeable decrease in customer activity. This suggests that most customers have been inactive for more than a year, and re-engagement strategies may be essential to bring back customers who have not purchased recently, particularly targeting those in the 400 to 700 day range where the drop-off is significant.
    """,
    "tab3": """
    **Example Question: How Frequently Did Customers Purchase Products in July, August, and September (Q3) 2018?**

    The majority of customers (**12,761**) made only one purchase in July, August, and September 2018, indicating low repeat purchase behavior. A smaller group of **433 customers** made two purchases, while even fewer customers made three or four purchases (**37 and 3** respectively). This highlights potential areas for improvement in customer retention strategies to encourage more repeat purchases, such as loyalty programs or targeted follow-up marketing.
    """,
    "tab4": """
    **Example Question: How much have customers spent on average over the past year (2018)?**
    
    The boxplot shows that the median customer expenditure in 2018 was **89.90 BRL**, indicating that half of the customers spent less than this amount. There is a notable range of expenditures among customers, with some outliers spending significantly more than the typical customer, as indicated by the extended upper whisker. However, most customers tend to spend relatively small amounts, suggesting a concentration of lower-value purchases rather than large, high-value transactions. This data can help guide marketing efforts to encourage higher spending per customer, perhaps through the introduction of incentives or bundled offers.
    """,
    "tab5": """
    **Example Question: In which regions do Olist customers shop the most?**

    Analyzing the number of purchases by region in Brazil, it is clear that **São Paulo (SP)** is the region with the highest number of purchases, with **48,874** orders. This is followed by **Rio de Janeiro (RJ)** with **15,191** purchases and **Minas Gerais (MG)** with **13,495** purchases. The distribution shows a significant concentration of purchases in the southeastern regions of Brazil, indicating that these regions are important markets for Olist. This concentration may be due to factors such as higher population density, better economic conditions, and improved logistics in these areas, which facilitate more frequent online shopping. This finding suggests that marketing and logistics efforts should continue to focus on these high-performing regions, while exploring growth opportunities in other states with lower shopping volumes.
    """,
    "tab6": """
    **Example Question: How can Olist customers be categorized based on the number of purchases in a year?**

    Analysis of customer segmentation based on number of purchases in 2018 shows that the vast majority of customers, **44,889** in total, made only one purchase, indicating that they fall into the **"Low"** category. A much smaller segment of **6,436** customers made 2 to 3 purchases, categorized as **"Medium"**, while only **796** customers were classified as **"High"** with 4 to 10 purchases, and **38** made more than 10 purchases, falling into the **"Very High"** category. This indicates that Olist's customer base consists largely of one-time buyers, suggesting a significant opportunity for Olist to improve customer retention by implementing strategies such as loyalty programs, personalized offers, or targeted campaigns to encourage repeat purchases and increase overall customer lifetime value.
    """
}

# Available years and quarters from the dataset
available_years = sorted(rfm_data['year'].unique())
available_quarters = sorted(rfm_data['quarter'].unique())

# Main Page Title
st.title("Brazilian E-Commerce Public Data Analysis")
st.markdown(
    "This dashboard visualizes insights from Olist Brazilian E-Commerce Public Dataset using various visualizations.")

# Tabs for Visualizations
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📊 Delivery Time Analysis",
     "🕒 Recency Distribution Analysis",
     "📊 Customer Purchase Frequency",
     "💸 Average Expenditure",
     "🌍 Geographic Analysis",
     "🧑 Customer Segmentation"])

# Visualization 1: Delivery Time Analysis
with tab1:
    # Add custom filter widgets within Tab 1 for Delivery Time Analysis
    st.header("Distribution of Delivery Time Across Brazil")
    st.subheader("Filter Options")

    order_status = st.multiselect(
        'Select Order Status:',
        options=all_data['order_status'].unique(),
        default=all_data['order_status'].unique()
    )

    # Filter data for Tab 1 based on selected order status
    filtered_data = all_data[all_data['order_status'].isin(order_status)]

    # Check if the filtered data is empty
    if filtered_data.empty:
        st.warning("No data available for the selected order status. Please adjust your selection.")
    else:
        # Creating the matplotlib histogram for delivery time
        fig, ax = plt.subplots(figsize=(12, 6))
        n, bins, patches = ax.hist(filtered_data['delivery_time_days'].dropna(), bins=15, edgecolor='black',
                                   color='#6A5ACD', alpha=0.75)

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

        plt.figtext(0.5, -0.05, f"© {datetime.datetime.now().year} Mohammad Raya Satriatama. All rights reserved.",
                    ha="center",
                    fontsize=9, color='gray')

        st.pyplot(fig)

        st.write(conclusions['tab1'])

# Visualization 2: Recency Distribution Analysis
with tab2:
    st.header("Recency Distribution Analysis")
    fig, ax = plt.subplots(figsize=(12, 6))
    n, bins, patches = ax.hist(rfm_data['recency'], bins=20, edgecolor='black', color='#4682B4', alpha=0.7)

    # Add grid lines for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    # Set the labels and title for the plot
    ax.set_xlabel('Days Since Last Purchase', fontsize=14, labelpad=10)
    ax.set_ylabel('Number of Customers', fontsize=14, labelpad=10)
    ax.set_title('Recency Distribution of Customers', fontsize=16, fontweight='bold', pad=15)

    # Add annotations to each bar to display the count
    for i in range(len(patches)):
        height = n[i]
        if height > 0:
            ax.text(
                patches[i].get_x() + patches[i].get_width() / 2,
                height + 50,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=10,
                color='black'
            )

    plt.figtext(0.5, -0.05, f"© {datetime.datetime.now().year} Mohammad Raya Satriatama. All rights reserved.",
                ha="center",
                fontsize=9, color='gray')

    st.pyplot(fig)

    st.write(conclusions['tab2'])

# Visualization 3: Customer Purchase Frequency
with tab3:
    # Default values for Q3 2018
    default_year = 2018
    default_quarters = [3]
    st.header("Frequency of Purchases by Customers")

    # Add custom filter widgets for Year and Quarter
    available_years = sorted(rfm_data['year'].dropna().unique().astype(int))
    available_quarters = [1, 2, 3, 4]

    # Allow multi-select for years and quarters
    selected_years = st.multiselect("Select Year(s)", options=available_years, default=[default_year])
    selected_quarters = st.multiselect("Select Quarter(s)", options=available_quarters, default=default_quarters)

    # Filter the data based on the selected year(s) and quarter(s)
    if selected_years and selected_quarters:
        filtered_data = rfm_data[
            (rfm_data['year'].isin(selected_years)) & (rfm_data['quarter'].isin(selected_quarters))]
    else:
        filtered_data = pd.DataFrame()  # Empty dataframe if no year or quarter is selected

    # Set dynamic header based on user selection
    if selected_years and selected_quarters:
        years_str = ', '.join(map(str, selected_years))
        quarters_str = ', '.join(map(str, selected_quarters))
        dynamic_header = f"Frequency of Purchases by Customers in Year(s): {years_str}, Quarter(s): {quarters_str}"
    else:
        dynamic_header = "Frequency of Purchases by Customers (No Year/Quarter Selected)"

    st.header(dynamic_header)

    # If there are no quarters selected or filtered_data is empty, display a message
    if filtered_data.empty:
        st.warning("No data available for the selected year and quarter(s). Please adjust your selection.")
    else:
        # Set up the figure size and plot histogram for Streamlit
        fig, ax = plt.subplots(figsize=(12, 6))
        n, bins, patches = ax.hist(
            filtered_data['frequency'],
            bins=15,
            edgecolor='black',
            log=True,
            color='lightcoral',
            alpha=0.75
        )

        # Set labels and title with increased font size and bold styling
        ax.set_xlabel('Number of Purchases (Frequency)', fontsize=14)
        ax.set_ylabel('Number of Customers (Log Scale)', fontsize=14)
        ax.set_title(
            f'Frequency of Purchases by Customers in Year(s): {years_str}, Quarter(s): {quarters_str} (Log Scale)',
            fontsize=16, weight='bold')

        # Adding grid lines for better readability
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Adding text annotations for each bar
        for i in range(len(patches)):
            height = n[i]
            if height > 0:
                ax.text(
                    patches[i].get_x() + patches[i].get_width() / 2,
                    height,
                    f'{int(height)}',
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    color='black',  # Use a contrasting color to make text annotations visible
                    fontweight='bold'
                )

        # Set limits and style for the y-axis
        ax.set_ylim(bottom=0.5)
        ax.set_yscale('log')
        ax.set_yticks([1, 10, 100, 1000, 10000])
        ax.set_yticklabels(['1', '10', '100', '1K', '10K'])  # Customize tick labels

        # Add some decorative elements
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Adding a legend to clarify that the bars represent frequency counts
        ax.legend(['Customer Frequency'], loc='upper right', fontsize=12, title='Legend')

        plt.figtext(0.5, -0.05, f"© {datetime.datetime.now().year} Mohammad Raya Satriatama. All rights reserved.",
                    ha="center",
                    fontsize=9, color='gray')

        st.pyplot(fig)

        st.write(conclusions['tab3'])

# Visualization 4: Average Expenditure Per Customer with Year Filter
with tab4:
    # Add custom filter widgets for Year within Tab 4
    st.header("Customer Expenditure Analysis")
    st.subheader("Filter Options")

    # Multiselect widget for selecting the year, default set to 2018
    available_years = sorted(rfm_data['year'].dropna().unique().astype(int))
    selected_years = st.multiselect(
        "Select Year(s) for Analysis:",
        options=available_years,
        default=[2018]
    )

    # Filter the data based on selected years from rfm_data
    filtered_data = rfm_data[rfm_data['year'].isin(selected_years)]

    # If no years are selected or filtered_data is empty, display a warning
    if filtered_data.empty:
        st.warning("No data available for the selected year(s). Please adjust your selection.")
    else:
        # Set the title based on selected years
        selected_years_str = ', '.join(map(str, selected_years))
        plot_title = f"Boxplot of Customer Expenditure in {selected_years_str}"

        # Create the boxplot for the filtered data
        fig, ax = plt.subplots(figsize=(12, 6))

        # Draw the boxplot with enhancements
        box = ax.boxplot(
            filtered_data['monetary'],
            vert=False,
            patch_artist=True,
            boxprops=dict(facecolor='lightblue', color='navy', linewidth=1.5),
            medianprops=dict(color='red', linewidth=2),
            whiskerprops=dict(color='navy', linestyle='--', linewidth=1.5),
            capprops=dict(color='navy', linewidth=1.5),
            flierprops=dict(marker='o', color='orange', alpha=0.5, markersize=6)
        )

        # Set the labels and title
        ax.set_xlabel('Total Expenditure (BRL)', fontsize=14)
        ax.set_title(plot_title, fontsize=16, weight='bold')
        ax.set_yticks([])  # Remove y-axis ticks since we have a single boxplot

        # Adding grid for better readability
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        # Highlight the median value with annotation
        median = filtered_data['monetary'].median()
        ax.annotate(
            f'Median: {median:.2f}',
            xy=(median, 1),
            xytext=(median + 200, 1.1),
            arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5),
            fontsize=12, color='darkred'
        )

        # Add some decorations to make it more polished
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.figtext(0.5, -0.05, f"© {datetime.datetime.now().year} Mohammad Raya Satriatama. All rights reserved.",
                    ha="center",
                    fontsize=9, color='gray')

        st.pyplot(fig)

        st.write(conclusions['tab4'])

# Visualization 5: Regions with the Highest Number of Purchases
with tab5:
    st.header("Regions with the Highest Number of Purchases")

    # Aggregate number of purchases by state using all_data
    state_purchases = all_data.groupby('customer_state')['order_id'].count().reset_index()
    state_purchases.columns = ['state', 'total_purchases']
    state_purchases = state_purchases.sort_values(by='total_purchases', ascending=False)

    # Load GeoJSON file for Brazil states boundaries
    geojson_file_path = Path(__file__).parent.parent / 'map' / 'brazil-states.geojson'
    try:
        with open(geojson_file_path, 'r') as f:
            brazil_geo = json.load(f)
    except FileNotFoundError:
        st.error(f"GeoJSON file not found at {geojson_file_path}. Please check the path.")
        st.stop()

    # Merge GeoJSON data with state purchase data to include the total_purchases field
    for feature in brazil_geo['features']:
        state_code = feature['properties']['sigla']
        purchase_info = state_purchases[state_purchases['state'] == state_code]
        if not purchase_info.empty:
            feature['properties']['total_purchases'] = int(purchase_info['total_purchases'].values[0])
        else:
            feature['properties']['total_purchases'] = 0

    # Create a base map centered around Brazil
    brazil_map = folium.Map(location=[-14.2350, -51.9253], zoom_start=4, tiles='cartodbpositron')

    # Add the Choropleth layer for visualizing the number of purchases by state
    folium.Choropleth(
        geo_data=brazil_geo,
        name='choropleth',
        data=state_purchases,
        columns=['state', 'total_purchases'],
        key_on='feature.properties.sigla',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.5,
        line_color='black',
        legend_name='Number of Purchases by State',
        highlight=True
    ).add_to(brazil_map)

    # Add custom tooltips for additional information about each state
    style_function = lambda x: {
        'fillColor': '#ffffff',
        'color': '#000000',
        'fillOpacity': 0.1,
        'weight': 0.1
    }
    highlight_function = lambda x: {
        'fillColor': '#0000ff',
        'color': '#000000',
        'fillOpacity': 0.5,
        'weight': 0.4
    }

    # Add GeoJson layer with tooltips showing state name, state code, and total purchases
    folium.GeoJson(
        brazil_geo,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['sigla', 'name', 'total_purchases'],  # Use fields from the GeoJSON properties
            aliases=['State Code:', 'State Name:', 'Total Purchases:'],
            localize=True
        )
    ).add_to(brazil_map)

    # Add a layer control panel to the map
    folium.LayerControl(collapsed=False).add_to(brazil_map)

    # Display the map in Streamlit
    folium_static(brazil_map)

    st.write(conclusions['tab5'])

# Visualization 6: Customer Segmentation Based on Purchase Frequency
with tab6:

    # Add header and filter for the year (from 2016 to 2018) with default set to 2018
    st.header("Customer Segmentation Based on Purchase Frequency in Selected Year(s)")
    st.subheader("Filter Options")

    # Convert 'order_purchase_timestamp' to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(all_data['order_purchase_timestamp']):
        all_data['order_purchase_timestamp'] = pd.to_datetime(all_data['order_purchase_timestamp'])

    # Add a multiselect widget for selecting the year(s), default set to 2018
    available_years = sorted(all_data['order_purchase_timestamp'].dt.year.unique())
    selected_years = st.multiselect(
        "Select Year(s) for Analysis:",
        options=available_years,
        default=[2018],
        key="year_selection_tab6"
    )

    # Filter the data based on selected years
    filtered_data = all_data[all_data['order_purchase_timestamp'].dt.year.isin(selected_years)]

    # If no years are selected, display a warning
    if filtered_data.empty:
        st.warning("No data available for the selected year(s). Please adjust your selection.")
    else:
        frequency_data = filtered_data.groupby('customer_unique_id').size().reset_index(name='frequency')
        low_segment = frequency_data[frequency_data['frequency'] == 1]
        medium_segment = frequency_data[(frequency_data['frequency'] >= 2) & (frequency_data['frequency'] <= 3)]
        high_segment = frequency_data[(frequency_data['frequency'] >= 4) & (frequency_data['frequency'] <= 10)]
        very_high_segment = frequency_data[frequency_data['frequency'] > 10]

        # Count the number of customers in each segment
        segment_counts = [
            len(low_segment),
            len(medium_segment),
            len(high_segment),
            len(very_high_segment)
        ]

        # Define labels and colors for the segments
        segment_conditions = ['Low: 1 Purchase',
                              'Medium: 2-3 Purchases',
                              'High: 4-10 Purchases',
                              'Very High: > 10 Purchases']
        segment_colors = ['skyblue', 'orange', 'green', 'red']

        # Create the bar chart
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(segment_counts)), segment_counts, color=segment_colors, edgecolor='black')

        # Adding text annotations for each bar, positioned more precisely
        for i, bar in enumerate(bars):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + (bar.get_height() * 0.02),
                f'{int(bar.get_height())}',
                ha='center',
                va='bottom',
                fontsize=10,
                fontweight='bold',
                color='black'
            )

        # Set the title based on selected years
        selected_years_str = ', '.join(map(str, selected_years))
        plot_title = f"Customer Segmentation Based on Purchase Frequency in Year(s): {selected_years_str}"

        # Adding labels and title
        ax.set_xlabel('Customer Segment', fontsize=14)
        ax.set_ylabel('Number of Customers', fontsize=14)
        ax.set_title(plot_title, fontsize=16, weight='bold')

        # Adding the legend
        legend = ax.legend(
            handles=bars,
            labels=segment_conditions,
            loc='upper right',
            shadow=True,
            fontsize='medium',
            title="Segment Conditions"
        )

        # Remove top and right spines for better aesthetics
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Adding gridlines for better readability
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        plt.figtext(0.5, -0.05, f"© {datetime.datetime.now().year} Mohammad Raya Satriatama. All rights reserved.",
                    ha="center",
                    fontsize=9, color='gray')

        st.pyplot(fig)

        # Display the conclusion text (make sure to define 'conclusions' dict beforehand)
        st.write(conclusions['tab6'])

current_year = datetime.datetime.now().year
footer = f"""
    <style>
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: #333;
            text-align: center;
            padding: 10px;
            font-size: 12px;
        }}
    </style>
    <div class="footer">
        &copy; {current_year} Mohammad Raya Satriatama. All Rights Reserved.
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
