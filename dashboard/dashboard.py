
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt
from babel.numbers import format_currency

def create_byproduct_df(df):
    sum_orders_df = df.groupby("product_category_name_english").product_id.count().sort_values(ascending=False).reset_index()
    return sum_orders_df

def create_bypayment_df(df):
    payment_df = df.groupby(by="payment_type").payment_value.mean().sort_values(ascending=False).reset_index()
    return payment_df

def customers_rating_df(df):
    customers_rating = df['review_score'].value_counts().sort_values(ascending=False)
    max_score = customers_rating.idxmax()
    #customers_df = df['review_score']
    return (customers_rating, max_score)

def create_rfm_df(df):
    current_time =dt.datetime(2018,12,10)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    recency = (current_time - df.groupby('customer_id')['order_purchase_timestamp'].max()).dt.days
    frequency = df.groupby('customer_id')['order_id'].count()
    monetary = df.groupby('customer_id')['price'].sum()

    # Create a new DataFrame with the calculated metrics
    rfm = pd.DataFrame({
        'customer_id': recency.index,
        'Recency': recency.values,
        'Frequency': frequency.values,
        'Monetary': monetary.values
    })

    col_list = ['customer_id','Recency','Frequency','Monetary']
    rfm.columns = col_list
    return rfm

all_df = pd.read_csv("proyek_analisis_data/submission/dashboard/main_data.csv")

datetime_columns=["order_approved_at",]
for column in datetime_columns:
    all_df[column]=pd.to_datetime(all_df[column])

#sidebar
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://dicoding-web-img.sgp1.cdn.digitaloceanspaces.com/original/commons/new-ui-logo.png")
    st.write('Brazilian E-Commerce Public Dataset')
    
orders_product_df = create_byproduct_df(all_df)
customers_rating, max_score = customers_rating_df(all_df)
payment_df = create_bypayment_df(all_df)
rfm=create_rfm_df(all_df)

st.header('Brazilian E-Commerce Public Dataset by Olist :sparkles:')

# Produk apa dengan jumlah pembelian terbesar dan terkecil?
st.subheader("penjualan produk tinggi dan terendah")
col1, col2 = st.columns(2)

with col1:
    highest_product_sold=orders_product_df['product_id'].max()
    st.markdown(f"Penjualan Tertinggi : **{highest_product_sold}**")

with col2:
    lowest_product_sold=orders_product_df['product_id'].min()
    st.markdown(f"Penjualan Terendah : **{lowest_product_sold}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))

colors = ["#102cd4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="product_id", 
    y="product_category_name_english", 
    data=orders_product_df.head(5), 
    palette=colors, 
    ax=ax[0],
    )
ax[0].set_ylabel('')
ax[0].set_xlabel('')
ax[0].set_title("produk dengan penjualan tertinggi", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(
    x="product_id", 
    y="product_category_name_english", 
    data=orders_product_df.sort_values(by="product_id", ascending=True).head(5), 
    palette=colors, 
    ax=ax[1],)
ax[1].set_ylabel('')
ax[1].set_xlabel('')
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("produk dengan penjualan terendah", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

plt.suptitle("penjualan produk tinggi dan terendah", fontsize=20)
st.pyplot(fig)


#  bagaimana tingkat kepuasan customers setelah melakukan pembelian terhadap suatu barang?
st.subheader("Tipe pembayaran yang paling sering digunakan")

plt.figure(figsize=(10, 5))

colors = ["#102cd4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot( 
    x="payment_type",
    y="payment_value",
    data=payment_df.sort_values(by="payment_value", ascending = False),
    palette=colors
)
plt.title("tipe pembayaran yang paling sering digunakan", loc="center", fontsize=15)
plt.ylabel("nilai transaksi")
plt.xlabel(None)
plt.xticks(fontsize=12)
st.pyplot(plt)

#tipe pembayaran apa yang paling sering digunakan dan berapa jumlah rata_rata nilai pembayarannya?
st.subheader("tingkat kepuasan customers")

plt.figure(figsize=(16, 8))
sns.barplot(
            x=customers_rating.index, 
            y=customers_rating.values, 
            order=customers_rating.index,
            palette=["#102cd4" if score == max_score else "#D3D3D3" for score in customers_rating.index],
            #palette=["#90CAF9"]
            
            )

plt.title("tingkat kepuasan customers", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Customer")
plt.xticks(fontsize=12)
st.pyplot(plt)


#RFM Analysis
st.subheader("Best Customer Based on RFM Parameters")

colors = ["#102cd4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

tab1, tab2, tab3 = st.tabs(["Recency", "Frequency", "Monetary"])

with tab1:
    plt.figure(figsize=(16, 8))
    sns.barplot(
        y="Recency", 
        x="customer_id", 
        data=rfm.sort_values(by="Recency", ascending=True).head(5), 
        palette=colors,
        
        )
    plt.title("By Recency (Day)", loc="center", fontsize=18)
    plt.ylabel('')
    plt.xlabel("customer")
    plt.tick_params(axis ='x', labelsize=15)
    plt.xticks([])
    st.pyplot(plt)

with tab2:
    plt.figure(figsize=(16, 8))
    sns.barplot(
        y="Frequency", 
        x="customer_id", 
        data=rfm.sort_values(by="Frequency", ascending=False).head(5), 
        palette=colors,
        
        )
    plt.ylabel('')
    plt.xlabel("customer")
    plt.title("By Frequency", loc="center", fontsize=18)
    plt.tick_params(axis ='x', labelsize=15)
    plt.xticks([])
    st.pyplot(plt)

with tab3:
    plt.figure(figsize=(16, 8))
    sns.barplot(
        y="Monetary", 
        x="customer_id", 
        data=rfm.sort_values(by="Monetary", ascending=False).head(5), 
        palette=colors,
        )
    plt.ylabel('')
    plt.xlabel("customer")
    plt.title("By Monetary", loc="center", fontsize=18)
    plt.tick_params(axis ='x', labelsize=15)
    plt.xticks([])
    st.pyplot(plt)

st.caption('Copyright (c) M Rama 2023')
