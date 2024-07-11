import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

#set page configuration
st.set_page_config(page_title="Agribusiness Dashboard",page_icon=":globe_with_meridians:")

st.title("Global Agribusiness Expansion Analytics")

#load data function
@st.cache_data
def load_data():
    file_path='FAOSTAT_data_en_2-20-2024.csv'
    data=pd.read_csv(file_path)
    data=data[(data!=0).all(axis=1)] #remove zero values
    data=data.drop(columns=['Domain Code','Domain','Area Code (M49)','Element Code','Item Code (CPC)','Flag','Flag Description','Year Code','Unit'])
    data=data.pivot_table(index=['Area','Year'],columns='Element',values='Value',aggfunc='sum').reset_index()    
    return data

@st.cache_data
def load_data2():
    file_path='FAOSTAT_data_en_2-20-2024.csv'
    data=pd.read_csv(file_path)
    data=data[(data!=0).all(axis=1)] #remove zero values
    data=data.drop(columns=['Domain Code','Domain','Area Code (M49)','Element Code','Item Code (CPC)','Flag','Flag Description','Year Code','Unit'])
    data=data.pivot_table(index=['Area','Item','Year'],columns='Element',values='Value',aggfunc='sum').reset_index()
    return data

def update_layout(fig,width,height):
    fig.update_layout( autosize=False, width=width, height=height)
    return fig


    
def plot_area_chart(area,n=10):
    area_explanations = {
    'Bahrain': """Bahrain demonstrates promising potential in crop production and yield, with both metrics steadily increasing over the analyzed period, culminating in record highs of 44.33 thousand tonnes and 7.71 million grams per hectare respectively in 2022. This growth can be attributed to several factors, including the expansion of greenhouse cultivation, a growing workforce, and improved agricultural techniques.

A key contributor to Bahrain's agricultural success is the significant adoption of greenhouse farming. By providing a controlled environment, greenhouses ensure consistent production and protect crops from adverse weather conditions. Crops such as cucumbers, gherkins, and tomatoes exhibit substantial opportunities, boasting high yields and production rates. Notably, Bahrain's data points cluster towards the highest and rightmost end of the spectrum.

However, despite these positive developments, agriculture in Bahrain faces challenges such as land tenure issues, small-scale farm operations, labor shortages, and a lack of financial incentives, which limit investment in the sector. Additionally, the arid climate and limited water resources pose significant risks to agribusiness expansion in the country.Source: Mordor Intelligence - Agriculture in Bahrain Industry Report"""
,
    'Bangladesh': """In Bangladesh, both crop production and yield show a steady increase over the analyzed period, culminating in record highs of 94.5 million tonnes and 4.80 million grams per hectare respectively in 2022. Promising crops for further growth in Bangladesh include sugar cane, mangoes, guavas, mangosteens, potatoes, and rice. These crops demonstrate a high growth trajectory, indicating potential opportunities for expansion. However, agriculture in Bangladesh faces challenges such as arable land loss due to population growth, as well as susceptibility to natural disasters like floods, droughts, and salinity.""",
    'China, mainland': """China, mainland exhibits a rapid increase in crop yield from 14.76 million grams per hectare in 2016 to 15.53 million grams per hectare in 2022. However, in terms of crop production, there is a sharp decline from its peak of 1.95 billion tonnes in 2021 to 1.88 billion tonnes in the following year. Despite being the world's largest agricultural producer, with the largest area harvested at 44.18 million hectares, only 10% of China's total land is cultivable. Source: https://en.wikipedia.org/wiki/Agriculture_in_China. Potential crops for growth in China include sugar cane, tomatoes, cucumbers, gherkins, and watermelons. China is also the second-largest sugar cane producer globally, reaching an all-time high production of 109.388 million tonnes in 2019, although it decreased to 103.38 million tonnes in 2022. However, China faces significant constraints, particularly related to climate change. Shifting climate patterns and ozone pollution have collectively reduced China's crop yields by 10% between 1981 and 2010, resulting in an annual loss of 55 million tons of crops. Source: https://www.csis.org/.""",
    'Cambodia': """Crop production and yield in Cambodia gradually increases over the period, reaching its highest peak of 35.4M tons and 2M g/ha respectively in year 2021 and 2022. This was driven using new technologies and quality fertilizers, expanded irrigation and better access to mechanized services and markets. Cambodia’s agricultural exports increases as prices remained competitive compared to rice producers in neighbouring Thailand, Vietnam and Myanmar. Crops that were most likely to be profitable in production are fresh cassava leaves, followed by sugar cane and rice. Point clusters in a high growth trajectory, running from bottom left to top right. Cambodia faces deceleration in land expansion, bad weather, falling global rice prices, and the tightening of competition among rice producers. Source: https://www.worldbank.org/en/country/cambodia/publication/cambodian-agriculture-in-transition-opportunities-and-risks . Immediate investments and policy improvements are necessary to address these challenges and support agriculture growth in Cambodia. Short to medium-term recommendations include strengthening the environmental sustainability of agricultural production, enhancing the quality of agricultural public programs, and increasing allocations to more effective programs. These measures can contribute to sustaining and further boosting Cambodia's agricultural sector.""",
    'India': """The average crop production and yield in India exhibit an upward trend with slight fluctuations over the analyzed period. The total production volume reached its peak at 1.25 billion tons in 2021. In terms of crop yield, India recorded its highest value in 2016, with 6.789 million grams per hectare (g/ha), followed by a drastic decline to 6.455 million g/ha the following year. However, it gradually climbed back up to reach 6.697 million g/ha in 2022.

India holds the title of being the world's largest sugar cane producer, with its highest production recorded at 439.42 million tons and 849.0 million g/ha. Promising crops for consideration in India include potatoes, rice, and wheat, as their data points cluster in a positive trajectory, moving from left to right on the chart.""",
    'Nepal':"""Nepal demonstrates a high growth trajectory throughout the analysis period, with crop production increasing from 22.9 million tons in 2017 to 25.12 million tons in 2022. Similarly, the average crop yield shows a positive trend, rising from 3.52 million grams per hectare (g/ha) in 2017 to 3.99 million g/ha in 2022. Agriculture remains a crucial pillar of Nepal’s economy, contributing one-third of the nation's GDP.

Nepal boasts rich agro-biodiversity, enabling farmers to cultivate diversified crops as a strategy to mitigate the impact of erratic weather patterns and other unfavorable conditions. While certain crops, such as raw ginger, exhibit significant production potential, their data points appear disorganized and scattered. Conversely, crops like maize, mangoes, guavas, mangosteens, millet, potatoes, and wheat demonstrate promising growth trajectories, with their data points clustering in a positive direction from left to right on the chart.

However, there are risks to consider, including a shrinking workforce due to changing landscapes and climate variations, which can adversely affect productivity and income generation. Additionally, the insufficient adoption of modern technology and mechanization poses challenges to further enhancing agricultural productivity in Nepal.""",
    'Oman':"""Oman exhibits a notable growth trajectory in crop production, with output increasing from 905.45 thousand tons in 2016 to 1.57 million tons in 2022, reflecting a significant upward trend. Similarly, the average crop yield also demonstrates substantial growth, rising from 6.67 million grams per hectare (g/ha) in 2016 to 12.08 million g/ha in 2022.

The diverse climate of Oman, encompassing arid deserts and subtropical regions, presents opportunities for cultivating a wide variety of crops suited to different environmental conditions. Despite being a water-scarce country, Oman has made investments in irrigation infrastructure, including dams and reservoirs, to optimize water utilization for agriculture.

However, these advancements also pose risks, particularly regarding water scarcity, as Oman grapples with limited freshwater resources and a reliance on groundwater extraction for irrigation purposes. Moreover, the country's diverse climate increases susceptibility to extreme weather events, which can disrupt crop production and pose challenges to agricultural sustainability.

Notably, crops such as cauliflowers, broccoli, chillies, peppers, green capsicum, cucumbers, gherkins, and eggplants exhibit a positive growth trajectory, with data points clustering from the lower left to the upper right on the chart, indicating promising trends in their production and yield over time.
""",
    'Qatar':"""The chart illustrates a sharp increase in crop production, rising from 76.89 thousand tons to 132.61 thousand tons, alongside an increase in crop yield from 4.19 million grams per hectare (g/ha) to 5.13 million g/ha. One of Qatar's major strengths lies in its high per capita income, which provides significant purchasing power and investment potential for agricultural development. Crops such as tomatoes, chillies, peppers, green capsicum, and other vegetables demonstrate promising opportunities, as evidenced by the clustering of data points from the lower left to the upper right, indicating a growth trajectory. However, risks to consider include limited arable land availability, which poses constraints on large-scale agricultural expansion, necessitating efficient land use and management strategies.""",
    'Saudi Arabia':"""In Saudi Arabia, the trend in agricultural production and yield depicts an upward trajectory, with production increasing from 5.04 million tons in 2016 to 7.080 million tons in 2020, and yield rising from 3.19 g/ha in 2016 to 7.26 million g/ha in 2022. One of Saudi Arabia's major strengths is its vast expanses of land suitable for agricultural production, particularly in the southwestern regions where underground water resources are available, despite the arid climate. However, overuse of water resources for agriculture poses a risk to long-term sustainability. Potential crops for consideration, such as potatoes and tomatoes, exhibit an upward trend in their point clustering, indicating promising opportunities for cultivation."""
}
    area_data = df2.query(f"Area == '{area}'")
    top_items=area_data.groupby('Item')['Production'].sum().sort_values(ascending=False).head(n).index.tolist() #find top items
    top_items_data=area_data[area_data['Item'].isin(top_items)] #filter data for top items
    fig=px.scatter(top_items_data,x='Production',y='Yield',color='Item',
               title=f'Yield vs Production of Top {n} Agricultural items in {area_data["Area"].iloc[0]}',
               labels={'Yield':'Yield (100g/ha)','Production':'Production (Tonne)'})
    fig=update_layout(fig,width=1000,height=800)
    st.plotly_chart(fig)
    
     # display explanations for area
    st.write(f"{area_explanations.get(area)}")
   

#load data
df=load_data()
df2=load_data2()

#sidebar navigation
page=st.sidebar.selectbox("Choose a page",["Homepage",'Data View','Data Analysis'])

if page == "Homepage":
    st.header("Executive Summary")
    st.write("""The analysis of agricultural data across 51 countries in Asia reveals promising opportunities and challenges for agribusiness expansion. Countries like Bahrain, Cambodia, and Qatar exhibit high growth trajectories in crop production and yield, driven by factors such as technological advancements and market competitiveness. Saudi Arabia and Qatar boast favorable conditions for agricultural development, including ample land availability and high purchasing power. Challenges such as water scarcity, climate variability, and limited arable land availability pose risks to long-term sustainability. Efficient resource management and adaptation strategies will be crucial for mitigating these risks. Adoption of modern technologies and improved agricultural practices, as seen in Oman and Cambodia, can drive growth and enhance productivity in agriculture. Investments in infrastructure, research, and development, coupled with supportive policies, are essential for fostering a conducive environment for agribusiness expansion. Countries like Nepal and Bangladesh highlight the importance of policy improvements and investment in sustainable agricultural practices.""")
    st.header("Introduction")
    st.write("""The objective of analyzing FAOSTAT agricultural data is to identify potential countries with growth opportunities for agribusiness expansion. 51 countries in Asia are analyzed using datasets spanning from 2016 to 2022. Quantitative metrics used to gain insights into trends include production volume, crop yield, and area harvested.""")
    st.header("Methodology")
    st.write("""The dataset is sourced from the Food and Agriculture Organization of the United Nations. Tools explored in this project include Python libraries such as Plotly, Pandas, and Streamlit for building an interactive dashboard. Exploratory data analysis is conducted using Jupyter Notebook.""")
    st.header("Data Overview")
    st.write("""The analysis covers 51 countries in Asia, encompassing a total of 174 agricultural products. These products include a variety of crops such as rice, sugar cane, raw ginger, and natural rubber, among others. It's important to note that the product list includes both manufactured items like cotton lint and molasses, as well as raw crop yields. The main key metrics utilized in the analysis are yield, measured in 100 grams per hectare harvested, and production volume, measured in tonnes.""")
    
    
             
if page == "Data View":
    st.header("Data View")
    row_num=st.slider("Number of Rows to View",10,len(df2)) #slider for dataframe length
    st.dataframe(df2.head(row_num), #display dataframe
                 width=1000,
                 column_config={
                     "Area harvested":"Area harvested (ha)",
                     "Production":"Production (t)",
                     "Yield":"Yield (100g/ha)",
                     "Year":st.column_config.NumberColumn(format="%d ")
                 }
                )
             
if page == "Data Analysis":
    st.header("Analysis Findings")
    fig=px.line(df,
            x='Year',
            y='Production',
            color='Area',
            markers=True,
            title='Average Agricultural Production Trend (2016-2022) by area ',
            labels={'Production':'Production, in tonnes'}
           )
    fig=update_layout(fig,width=1000,height=800)
    st.plotly_chart(fig)
    st.write("""Based on the average agricultural production line chart, China (mainland) is the world’s no.1 top agricultural producer, starting at 1.84 billion tonnes in 2016 and increasing to 1.95 billion tonnes in 2021. However, it experiences a drastic dip to 1.88 billion tonnes in the following year. India comes second, with a steady increase from 1.07 billion tonnes in 2016 to 1.26 billion tonnes in 2021, followed by a slight dip to 1.23 billion tonnes the next year. Indonesia takes third place, starting at 426.824 million tonnes in 2016, making a steep climb to 507.31 million tonnes before experiencing slight fluctuations.
    In sequence, Thailand and Pakistan, both demonstrating significant fluctuations. Thailand's agricultural production starts at 213.48 million tonnes in 2016, experiences a sudden increase in 2017-2018 to 265.6 million tonnes, then decreases before a sharp fall in 2019-2020 to 195.44 million tonnes, and gradually climbs again. Pakistan shows a drastic steep increase in 2019-2020 from 151.90 million tonnes to 184.3 million tonnes before experiencing a significant fall to 164.08 million tonnes the following year.""")
    
     
    fig=px.line(df,
            x='Year',
            y='Yield',
            color='Area',
            markers=True,
            labels={'Yield':'Yield(100g/ha)'},
            title='Average Agricultural Yield Trend (2016-2022) by area'
           )
    fig=update_layout(fig,width=1000,height=800)
    st.plotly_chart(fig)
    st.write("""Based on the average agricultural yield trend, China (mainland) scores the highest crop yield in Asia, demonstrating a gradual increase over the analysis period, starting at 14.76 million grams per hectare (g/ha) in 2016 and reaching 15.53 g/ha. Turkey comes second, showing a gradual increase with its highest peak at 14.65 million g/ha. Israel ranks third highest, with the highest point reaching 13.25 million g/ha in 2022, although its yield shows many fluctuations. Jordan holds the fourth highest position, reaching 13.89 million g/ha in its peak in 2021, but also shows fluctuation. Kuwait reaches its highest peak at 13.40 million g/ha in 2019 but experiences a drastic fall to its lowest peak (9.55 million g/ha) in the following year.""")
    
    fig=px.scatter(df2,
          x='Production',
          y='Area harvested',
          color='Area',
          title='Relationship between Production and Area harvested')
    fig=update_layout(fig,width=1000,height=800)
    st.plotly_chart(fig)
    st.write("""As depicted in the scatter chart comparing area harvested to production, there exists a relationship between these two metrics: a larger area harvested (ha) tends to result in higher crop production (t). Most data points cluster densely near the origin, indicating smaller areas harvested and lower production volumes. However, certain outliers are notable, particularly India and China, mainland, where both large areas are harvested and high production volumes are observed. Additionally, Indonesia demonstrates high production volumes despite having an area harvested within the average range. Typically, individual area profiles illustrate dense clusters of data points near the origin, with a spread towards higher production volumes. However, some exceptions exist, such as China, Hong Kong SAR, China, Macao SAR, and Singapore, where data points are more sparse.""")
    
    fig=px.scatter(df2,
              x='Production',
              y='Yield',
              color='Area',
              title='Relationship between Production and Yield')
    fig=update_layout(fig,width=1000,height=800)
    st.plotly_chart(fig)
    st.write("""In the yield vs production scatter chart, data points cluster from the lower left to the upper right, indicating a positive correlation between the two metrics. It can be observed that most data points appear to be denser near the origin. However, a couple of outliers can be seen on the far left and right of the plot. For example, Oman has the highest crop yield (5.39M g/ha) but a very low production volume of 73.3k T. In other cases exhibiting unique patterns, areas like Bangladesh, Bahrain, or China, Hong Kong SAR represent points clustered in a vertical pattern. Conversely, in areas like Brunei Darussalam, point clusters are disorganized and display an unordered pattern.""")
    
    
    #identify demand trends
    top_items=df2.groupby(['Item','Year'])['Production'].sum().sort_values(ascending=False).reset_index()
    print(top_items.head(10))
    fig=px.scatter(top_items,
                x='Year',
                y='Production',
                color='Item',
                title='Demand Trends of Top Agricultural Items (2016-2022)',
                labels={'Production':'Production,in tonnes'}
               )
    fig=update_layout(fig,width=1500,height=800)
    st.plotly_chart(fig)
    st.write("""The sequence of highly demanded agricultural products begins with sugar cane, which experiences significant fluctuations in demand. Following sugar cane, rice demonstrates a gradual increase in demand, reaching its peak production volume of 708.7 million tonnes in 2021. Maize (corn) initially experiences higher demand than oil palm fruit, but over the analysis period, oil gradually surpasses maize in demand. Maize maintains a demand value ranging from 355 million to 363 million tonnes in the first four years, but it rapidly increases to 389.9 million tonnes, its highest value, in 2022. Meanwhile, oil maintains a demand value ranging from 360 million to 370 million tonnes.""")
    

    st.header('Areas with potential growth opportunities:')
    # Example usage in Streamlit
    specific_area=['Bahrain', 'Bangladesh', 'China, mainland','India','Nepal','Oman','Qatar','Saudi Arabia','Tajikistan','Turkiye','Uzbekistan','Yemen']
    selected_area = st.selectbox("Select an area",specific_area)
    if st.button("Plot"):
        plot_area_chart(selected_area)
        
    st.header('Conclusion')
    st.write("The analysis of agricultural data across various countries in Asia reveals a diverse landscape of opportunities and challenges for agribusiness expansion. Many countries, including Bahrain, Cambodia, and Qatar, exhibit high growth trajectories in both crop production and yield. This suggests significant potential for expansion and investment in these regions. Countries like Saudi Arabia and Qatar boast favorable conditions such as ample land availability and high per capita income, offering promising opportunities for agricultural development. Crops like tomatoes, chillies, and peppers show potential for growth. Despite opportunities, challenges such as water scarcity, climate variability, and limited arable land availability pose risks to long-term sustainability. Efficient resource management and adaptation strategies will be crucial for mitigating these risks. By aligning its expansion strategy with these insights and considerations, the agribusiness company can capitalize on emerging opportunities, mitigate risks, and achieve sustainable growth in the dynamic Asian agricultural market.")
   
    
    
