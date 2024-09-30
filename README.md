# E-Commerce Public Data Analysis Project 🌟

This project is a **Streamlit** dashboard that provides insights into the Brazilian E-Commerce Public Dataset by Olist using various visualizations. The dashboard is designed to help answer specific business questions related to customer purchase behavior, regional performance, delivery times, and more.

## Dashboard Link
You can access the live version of the dashboard here:
**[E-Commerce Public Data Analysis Dashboard](https://e-commerce-public-data-analysis-project.streamlit.app/)**

---

## 🛠 Setup Environment

This section describes how to set up the Python environment to run the dashboard, either using **Anaconda** or a general **Shell/Terminal** setup.

### Setup Environment - Anaconda
1. **Create a new environment**:
   ```sh
   conda create --name main-BECP python=3.9
   ```
2. **Activate the environment**:
   ```sh
   conda activate main-BECP
   ```
3. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

### Setup Environment - Shell/Terminal
1. **Create a new project directory**:
   ```sh
   mkdir e_commerce_public_data_analysis
   cd e_commerce_public_data_analysis
   ```
2. **Install pipenv and create a shell**:
   ```sh
   pipenv install
   pipenv shell
   ```
3. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

---

## 📊 Running the Dashboard

To run the Streamlit app locally, use the command:

```sh
streamlit run dashboard/dashboard.py
```

---

## 📂 Directory Structure

The main structure of the repository is as follows:

```
E-Commerce_Public_Data_Analysis_Project/
│
├── dashboard/
│   ├── all_data.csv
│   ├── dashboard.py
│   ├── rfm_data.csv
│
├── data/
│   ├── olist_customers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
│   └── product_category_name_translation.csv
│
├── map/
│   ├── brazil-states.geojson
│
├── Data_Analysis_Project.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

---

## 📜 Requirements

The following Python packages are required to run the project:

```plaintext
folium==0.17.0
matplotlib==3.9.2
numpy==2.1.1
pandas==2.2.3
plotly==5.24.1
seaborn==0.13.2
streamlit==1.38.0
streamlit_folium==0.22.1
```

You can install all the required packages by running:

```sh
pip install -r requirements.txt
```

---

## ⚡ Running the Web App

After setting up the environment and installing the required dependencies, simply run:

```sh
streamlit run dashboard/dashboard.py
```

This command will start a local server, and you will be able to access the dashboard via your web browser.

---

## 🔍 Example Usage and Insights

This dashboard provides answers to various business questions, including:

1. **Average Delivery Time Analysis**: Visualizes the distribution of delivery times across different orders in Brazil.
2. **Customer Recency Analysis**: Displays the time since each customer’s last purchase to determine customer engagement levels.
3. **Customer Purchase Frequency**: Provides insights into how often customers made purchases in specific periods.
4. **Average Expenditure Analysis**: Shows the spending patterns of customers.
5. **Geographic Analysis**: Highlights the regions with the highest number of purchases.
6. **Customer Segmentation**: Classifies customers based on their purchase frequency.

These insights can be found in different tabs of the dashboard, with each visualization tailored to address specific business questions.

---