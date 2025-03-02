# The libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries to build the webapp
import streamlit as st


# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to load a dataset with information about Netflix Movies and Series, extract some insights usign Pandas and displaying them with Matplotlib.")
    st.write("Data extracted from: https://www.kaggle.com/datasets/shivamb/netflix-shows (with some cleaning and modifications)")


# ----- Title of the page -----
st.title("🎬 Netflix Data Analysis")
st.divider()


# ----- Loading the dataset -----

@st.cache_data
def load_data():
    data_path = "data/netflix_titles.csv"

    movies_df = pd.read_csv(data_path, index_col=0)  # TODO: Ex 2.1: Load the dataset using Pandas, use the data_path variable and set the index column to "show_id"

    return movies_df   # a Pandas DataFrame


movies_df = load_data()

# Displaying the dataset in a expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(movies_df)


# ----- Extracting some basic information from the dataset -----

# TODO: Ex 2.2: What is the min and max release years?
min_year = min(movies_df["release_year"])
max_year = max(movies_df["release_year"])

# TODO: Ex 2.3: How many director names are missing values (NaN)?
num_missing_directors = movies_df["director"].isnull().sum()

# TODO: Ex 2.4: How many different countries are there in the data?
movies_df["country"] = movies_df["country"].fillna("Unknown")

list_countries = movies_df["country"]
delimiter = ', '
str_list_countries = delimiter.join(list_countries)
result_countries = str_list_countries.split(",")
result_countries_df = pd.Series(result_countries).unique()
n_countries = len(result_countries_df)

# TODO: Ex 2.5: How many characters long are on average the title names?
movies_df["Title Length"] = movies_df["title"].apply(lambda x: len(x))

avg_title_length = movies_df["Title Length"].mean() 


# ----- Displaying the extracted information metrics -----

st.write("##")
st.header("Basic Information")

cols1 = st.columns(5)
cols1[0].metric("Min Release Year", min_year)
cols1[1].metric("Max Release Year", max_year)
cols1[2].metric("Missing Dir. Names", num_missing_directors)
cols1[3].metric("Countries", n_countries)
cols1[4].metric("Avg Title Length", str(round(avg_title_length, 2)) if avg_title_length is not None else None)


# ----- Pie Chart: Top year producer countries -----

st.write("##")
st.header("Top Year Producer Countries")

cols2 = st.columns(2)
year = cols2[0].number_input("Select a year:", min_year, max_year, 2005)

# TODO: Ex 2.6: For a given year, get the Pandas Series of how many movies and series 
# combined were made by every country, limit it to the top 10 countries.

year_filter = movies_df.loc[movies_df["release_year"] == year]


list_countries_per_year = year_filter["country"]
delimiter2 = ', '
str_countries = delimiter2.join(list_countries_per_year)
countries_separated = str_countries.split(",")

column_name = ["countries"]
countries_df = pd.DataFrame(countries_separated, columns=column_name)

Count_per_country = countries_df.value_counts()

top_10_countries = Count_per_country.head(10)

# print(top_10_countries)
if top_10_countries is not None:
    fig = plt.figure(figsize=(8, 8))
    plt.pie(top_10_countries, labels=top_10_countries.index, autopct="%.2f%%")
    plt.title(f"Top 10 Countries in {year}")

    st.pyplot(fig)

else:
    st.subheader("⚠️ You still need to develop the Ex 2.6.")


# ----- Line Chart: Avg duration of movies by year -----

st.write("##")
st.header("Avg Duration of Movies by Year")

# TODO: Ex 2.7: Make a line chart of the average duration of movies (not TV shows) in minutes for every year across all the years. 
movies_filter = movies_df.loc[movies_df["type"] == "Movie"]

movies_filter_table = movies_filter["duration"].str.replace(" min", "", regex=False).astype(int).reset_index()
movies_filter.loc[:, "Minutes"] = list(movies_filter_table["duration"])

movies_avg_duration_per_year = movies_filter.groupby("release_year")["Minutes"].mean().reset_index()

if movies_avg_duration_per_year is not None:
    fig = plt.figure(figsize=(9, 6))

    plt.plot(movies_avg_duration_per_year["release_year"], movies_avg_duration_per_year["Minutes"])# TODO: generate the line plot using plt.plot() and the information from movies_avg_duration_per_year (the vertical axes with the minutes value) and its index (the horizontal axes with the years)

    plt.title("Average Duration of Movies Across Years")

    st.pyplot(fig)

else:
    st.subheader("⚠️ You still need to develop the Ex 2.7.")

