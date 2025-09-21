import streamlit as st
import pandas as pd
import plotly.express as px
import json, os

st.set_page_config(page_title="Simple Finance App", page_icon="💰", layout="wide")

category_file = "categories.json"
if "categories" not in st.session_state:
    st.session_state.categories = { "Uncategorized": [] }

if os.path.exists(category_file):
    with open(category_file, "r") as f:
        st.session_state.categories = json.load(f)

def save_categories():
    with open(category_file, "w") as f:
        json.dump(st.session_state.categories, f)

def load_transactions(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"].astype(str).str.replace(",", ""), errors="coerce")
    return df

def categorize(df):
    df["Category"] = "Uncategorized"
    for cat, keys in st.session_state.categories.items():
        if keys:
            pattern = "|".join([k.lower() for k in keys])
            mask = df["Details"].str.lower().str.contains(pattern, na=False)
            df.loc[mask, "Category"] = cat
    return df

def main():
    st.title("Simple Finance Dashboard")
    uploaded = st.file_uploader("Upload your transactions CSV", type="csv")

    if uploaded:
        df = load_transactions(uploaded)
        if df is None:
            return
        df = categorize(df)

        debits = df[df["Debit/Credit"] == "Debit"].copy()
        credits = df[df["Debit/Credit"] == "Credit"].copy()
        st.session_state.debits_df = debits

        tab1, tab2 = st.tabs(["Expenses", "Payments"])
        with tab1:
            new_cat = st.text_input("Add New Category")
            if st.button("Add"):
                if new_cat and new_cat not in st.session_state.categories:
                    st.session_state.categories[new_cat] = []
                    save_categories()
                    st.experimental_rerun()

            edited = st.data_editor(
                debits[["Date","Details","Amount","Category"]],
                column_config={
                    "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                    "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
                    "Category": st.column_config.SelectboxColumn("Category", options=list(st.session_state.categories))
                },
                hide_index=True,
                use_container_width=True,
                key="editor"
            )
            if st.button("Apply Changes"):
                for idx, row in edited.iterrows():
                    old = st.session_state.debits_df.at[idx, "Category"]
                    new = row["Category"]
                    if new != old:
                        st.session_state.debits_df.at[idx, "Category"] = new
                        st.session_state.categories.setdefault(new, []).append(row["Details"])
                save_categories()

            summary = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
            st.dataframe(summary)
            fig = px.pie(summary, names="Category", values="Amount", title="Expenses by Category")
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Payments")
            total = credits["Amount"].sum()
            st.metric("Total Payments", f"{total:,.2f} AED")
            st.write(credits)

if __name__ == "__main__":
    main()
