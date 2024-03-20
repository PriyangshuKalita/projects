import pandas as pd
import streamlit as st
import io
import contextlib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mini project G-06",page_icon=":bar_chart", layout='wide')

st.title("MHA Population Report(Gp-06)")
data = pd.read_csv('MHA_Population_Report.csv')
st.write(data)

# Create a buffer to capture the output
buffer = io.StringIO()

# Redirect the standard output to the buffer
with contextlib.redirect_stdout(buffer):
    data.info(verbose=True, show_counts=True)

# Get the captured output from the buffer
info_output = buffer.getvalue()

# Display the info() output on Streamlit
st.write("DataFrame Information:")
st.code(info_output)

# Get the slice of the DataFrame
data_slice = data.loc[:10:2]

# Display the slice on Streamlit
st.write("DataFrame Slice:")
st.dataframe(data_slice)

# Get the length of the DataFrame
data_length = len(data)

# Display the length on Streamlit
st.write("The length of the data is :")
st.write(data_length)

# Get the descriptive statistics of the DataFrame
data_desc = data.describe()

# Display the descriptive statistics on Streamlit
st.write("DataFrame Descriptive Statistics:")
st.write(data_desc)

# Get the count of missing values for each column
missing_values = data.isnull().sum()

# Display the missing value counts on Streamlit
st.write("Missing Value Counts:")
st.write(missing_values)

# Get the count of duplicated rows
duplicated_rows = data.duplicated().sum()

# Display the count of duplicated rows on Streamlit
st.write("Duplicated Rows Count:")
st.write(duplicated_rows)


st.title("Sorting")

# Sorting the DataFrame by 'Total_population' column in ascending order
data = data.sort_values(['Total_population'], ascending=True)
# Display the first 5 rows of the sorted DataFrame
st.write("Sorted DataFrame - First 5 Rows : ")
st.write(data.head(5))

# Sorting the households column in descending order
st.write('''Sorting the DataFrame by 'No. of households' column in descending order : ''')
sorted_data = data.sort_values(by='No_Of_households', ascending=False)
# Display the top rows of the sorted DataFrame
st.dataframe(sorted_data.head())

# Sorting the Number of areas where Total Population > 5000000 in ascending order
st.write('''Areas where Total Population > 5000000 : ''')
filtered_data = data[data['Total_population'] > 5000000]
st.write(filtered_data)
pop = len(filtered_data)
st.write("Number of areas where Total Population > 5000000 : ", pop)

# sidebar
st.title("Filtered Data : ")
st.sidebar.header("Please filter here :")
Year_list = st.sidebar.multiselect("Choose Year : ", options=data['Census_Year'].unique())
Place = st.sidebar.multiselect("Select Place : ", options=data['Town_or_Village'].unique())
if Year_list and Place:
    data_selection = data.query(("Census_Year == @Year_list & Town_or_Village==@Place"))
elif Year_list:
    data_selection = data.query("Census_Year == @Year_list")
elif Place:
    data_selection = data.query("Town_or_Village==@Place")
else:
    data_selection = data
st.dataframe(data_selection)


# Queries
st.title("Queries : ")

# What is the Total population by district in Maharashtra?
total_population_by_district = data.groupby("District")["Total_population"].sum()
st.write("Total population by district in Maharashtra : ")
st.write(total_population_by_district)

# What is the Total population in Maharashtra?
total_population = data['Total_population'].sum()
st.write(total_population, "is the total population in Maharashtra.")

# What is the total number of households?
avg_male_population = data['No_Of_households'].sum()
st.write(avg_male_population, "is the total number of households.")

# What is the Total number of households with children under 6 years old?
households_with_children = data[data["Total 0 to 6 year children"] > 0]
households_with_children_by_district = households_with_children.groupby("District")["No_Of_households"].sum()
st.write("Total number of households with children under 6 years old : ")
st.write(households_with_children_by_district)

# What is the Percentage of households with literate members by district?
literate_households = data[data["Total_literates"] > 0]
households_by_district = data.groupby("District")["No_Of_households"].sum()
literate_households_by_district = literate_households.groupby("District")["No_Of_households"].sum()
literate_households_percentage_by_district = literate_households_by_district / households_by_district * 100
st.write("Percentage of households with literate members by district : ")
st.write(literate_households_percentage_by_district)


# Graphs
st.title("Graphs : ")

# Bar graph
st.title("Bar Graph")
total_population_by_district = data.groupby("District")["Total_population"].sum()
st.bar_chart(total_population_by_district)

district = st.selectbox("Select a district", data["District"].unique())
total_population_by_district = data[data["District"] == district]["Total_population"].sum()
st.bar_chart(pd.Series(total_population_by_district))

# Histogram
st.title( "Histogram" )
literacy_rates = data["Total_literates"] / data["Total_population"] * 100
fig, ax = plt.subplots()
ax.hist(literacy_rates , color='orange', edgecolor='black', rwidth=1)
ax.set_xlabel('Literacy Rate (%)')
ax.set_ylabel('Number of People')
ax.set_title('Distribution of Literacy Rates')
st.pyplot(fig)

# Plot Graph
st.title("Plot Graph Example")
sc_st_population = data["Total_SC_population"] + data["Total_ST_population"]
fig, ax = plt.subplots()
ax.plot(sc_st_population.index, sc_st_population.values, marker='o')
ax.set_xlabel('SC/ST Population')
ax.set_ylabel('Number of People')
ax.set_title('Distribution of SC/ST Population')
ax.set_xticks(range(1, 100))
st.pyplot(fig)

# Scatter plot
st.title("Scatter Plot")
fig, ax = plt.subplots()
ax.scatter(data['Total_population'],data['Total_iliterates'], alpha=0.5)
ax.set_xlabel('Total population')
ax.set_ylabel('Total Iliterates')
st.pyplot(fig)
st.write('''This scatter plot shows the relationship between the total population and the total number of literates in the dataset.''')

# Line Chart
st.title("Line Chart")
def line_chart(df, district=None, taluka=None):
    filtered_data = df.copy()
    if district:
        filtered_data = filtered_data[filtered_data['District'] == district]    
    if taluka:
        filtered_data = filtered_data[filtered_data['Taluka'] == taluka] 
    population_by_year = filtered_data.groupby("Census_Year")["Total_population"].sum()
    fig, ax = plt.subplots()
    ax.plot(population_by_year.index, population_by_year.values)
    ax.set_title("Population Trends by Census Year")
    ax.set_xlabel("Census Year")
    ax.set_ylabel("Total Population")
    st.pyplot(fig)
    
# Creating filters for District and Taluka
selected_district = st.selectbox("Select a district", data['District'].unique(), key="district_select")
selected_taluka = st.selectbox("Select a taluka", data['Taluka'].unique(), key="taluka_select")

# Applying the filters and display the line chart
line_chart(data, district=selected_district, taluka=selected_taluka)

# Pie Chart
st.title("Pie Chart")
total_population = data.groupby("Census_Year")["Total_population"].sum()
fig, ax = plt.subplots()
ax.pie(total_population, labels=total_population.index, autopct='%1.1f%%')
ax.set_title("Total Population by Census Year in Maharashtra")
st.pyplot(fig)