import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data

#enable theme
alt.themes.enable('fivethirtyeight')

###############
###LOAD DATA###
###############

#CHICKEN SOUPS DATA FROM SPOONACULAR
chicken_noodle = pd.read_csv('./data/chicken_noodle_soup_nutrition.csv')
chicken = pd.read_csv('./data/chicken_soup_nutrition.csv')
chicken_soups = pd.concat([chicken_noodle,chicken])
chicken_soups = chicken_soups.set_index('iD')
chicken_soups = chicken_soups.fillna(0)
# st.write(chicken_soups.head())

###Manipulate DF to add nutrition per serving attributes
chicken_soups['fat_per_serving'] = chicken_soups.Fat_g/chicken_soups.servings
chicken_soups['calcium_per_serving'] = chicken_soups.Calcium_mg/chicken_soups.servings
chicken_soups['selenium_per_serving'] = chicken_soups['Selenium_µg']/chicken_soups.servings
chicken_soups['vit_C_per_serving'] = chicken_soups['Vitamin C_mg']/chicken_soups.servings
chicken_soups['zinc_per_serving'] = chicken_soups['Zinc_mg']/chicken_soups.servings
chicken_soups['iron_per_serving'] = chicken_soups['Iron_mg']/chicken_soups.servings
chicken_soups['copper_per_serving'] = chicken_soups['Copper_mg']/chicken_soups.servings
chicken_soups['vit_A_per_serving'] = chicken_soups['Vitamin A_IU']/chicken_soups.servings
chicken_soups['vit_D_per_serving'] = chicken_soups['Vitamin D_µg']/chicken_soups.servings
chicken_soups['calories_per_serving'] = chicken_soups['Calories_kcal']/chicken_soups.servings
# st.write(chicken_soups.head())

#OPEN FOOD DATA
#SOURCE: https://world.openfoodfacts.org/cgi/search.pl?search_terms=chicken+soup&search_simple=1&action=process
open_food_soups = pd.read_csv('./data/open_food_soups.csv')
# open_food_soups

###############
###CHART 1#####
###############

brush = alt.selection(type='interval', encodings=['x'])

# Define the base chart, with the common parts of the
# background and highlights
base = alt.Chart().mark_bar(color='lightgreen').encode(
    x=alt.X(alt.repeat('repeat'), type='quantitative', bin=alt.Bin(maxbins=20)),
    y='count()'
).properties(
    width=190,
    height=160
)

# gray background with selection
background = base.encode(
    color=alt.value('#ddd')
).add_selection(brush)

# blue highlights on the transformed data
highlight = base.transform_filter(brush)

# layer the two charts & repeat
chart1=alt.layer(
    background,
    highlight,
    data=chicken_soups
).repeat(repeat=["Calories_kcal", "Fat_g", 'Carbohydrates_g',
                'Cholesterol_mg','Sodium_mg','Protein_g'],
        columns=3
        )
# chart1

# chart1_5=alt.layer(
#     background,
#     highlight,
#     data=chicken_soups
# ).repeat(column=['Cholesterol_mg','Sodium_mg','Protein_g'])

###############
###CHART 2#####
###############

####Selection Histogram for Count of records in distribution
brush = alt.selection(type='interval')

points = alt.Chart(open_food_soups).mark_point().encode(
    x=alt.X('calcium_value:Q',axis=alt.Axis(title='Calcium (mg)')),
    y=alt.Y('proteins_value:Q',axis=alt.Axis(title='Protein (g)')),
    color=alt.condition(brush, 'hasAllergens:N', alt.value('lightgray')),
    tooltip=['product_name_en','fat_value:N', 'proteins_value:Q']
).add_selection(
    brush
).properties(
    width=400,height=400
)

bars_dairy = alt.Chart(open_food_soups).mark_bar().encode(
    y=alt.Y('hasDairy:N',axis=alt.Axis(title='Dairy')),
    color=alt.Color('hasAllergens:N',scale=alt.Scale(scheme='dark2')),
    x=alt.X('count(hasDairy):Q',axis=alt.Axis(title='Count of Soups'))
).transform_filter(
    brush
)

# bars_allergens = alt.Chart(open_food_soups).mark_bar().encode(
#     y='hasAllergens:N',
#     color=alt.Color('hasAllergens:N', legend=None),
#     x='count(hasAllergens):Q'
# ).transform_filter(
#     brush
# )


chart2=points & bars_dairy
# chart2

###############
###CHART 3#####
###############

selection=alt.selection_single(empty="none",on='mouseover', nearest=True)
colorCondition=alt.condition(selection,alt.Color('healthScore:Q',scale=alt.Scale(scheme='reds')),alt.value("lightgrey"))
sizeCondition=alt.condition(selection,alt.value(200),alt.value(50))

#Calcium Per Serving vs. VItamin D Per Serving; color by healthScore
base1=alt.Chart(chicken_soups).mark_circle().encode(
    alt.X('calcium_per_serving',axis=alt.Axis(title='Calcium (mg)')),
    alt.Y('vit_D_per_serving',axis=alt.Axis(title='Vitamin D (µg)')),
    color=colorCondition,
    size=sizeCondition,
    tooltip=['Title', 'calcium_per_serving', 'vit_D_per_serving']
).add_selection(
    selection
).properties(
    width=300,height=300
)
calc_D=base1
# calc_D

#Zinc Per Serving vs. Vit C Per Serving; color by healthScore
base=alt.Chart(chicken_soups).mark_circle().encode(
    alt.X('zinc_per_serving',axis=alt.Axis(title='Zinc (mg)')),
    alt.Y('vit_C_per_serving',axis=alt.Axis(title='Vitamin C (mg)')),
    color=colorCondition,
    size=sizeCondition,
    tooltip=['Title','zinc_per_serving','vit_C_per_serving']
).add_selection(
    selection
).properties(
    width=300,height=300
)
zinc_c=base
# zinc_c

#Iron Per Serving vs. Copper Per Serving; color by healthScore
base=alt.Chart(chicken_soups).mark_circle().encode(
    alt.X('iron_per_serving',axis=alt.Axis(title='Iron (mg)')),
    alt.Y('copper_per_serving',axis=alt.Axis(title='Copper (mg)')),
    color=colorCondition,
    size=sizeCondition,
    tooltip=['Title','iron_per_serving','copper_per_serving'],
).add_selection(
    selection
).properties(
    width=300,height=300
)
copp_iron=base
# copp_iron

#Vitamin A Per Serving vs. Selenium Per Serving; color by healthScore
base=alt.Chart(chicken_soups).mark_circle().encode(
    alt.X('vit_A_per_serving',axis=alt.Axis(title='Vitamin A (IU)')),
    alt.Y('selenium_per_serving',axis=alt.Axis(title='Selenium (µg)')),
    color=colorCondition,
    size=sizeCondition,
    tooltip=['Title','vit_A_per_serving','selenium_per_serving']
).add_selection(
    selection
).properties(
    width=300,height=300
)
A_selen=base
# A_selen

#Join the charts
chart3=((calc_D | zinc_c) & (copp_iron | A_selen))#.properties(title={
    #   "text": ["Flu-Fighting Nutrients Per Serving of Chicken Soups"], 
    #   "subtitle": ["The Nutritional Value of Various Chicken Soups sourced from 300+ Spoonacular recipes"]
    # })
# chart3

###############
###CHART 4#####
###############

cy_options=list(chicken_soups["servings"].unique())
cy_options=list(map(lambda x:int(x),cy_options))
cy_options.sort()

widget=alt.binding_select(options=cy_options,name='Select Serving Size: ')
selectServing=alt.selection_single(fields=['servings'],init={'servings':cy_options[1]},bind=widget)
# colorCondition = alt.condition(selectServing,alt.Color('servings:N'),alt.value('orange'))


chart4=alt.Chart(chicken_soups).mark_circle(size=80,opacity=0.5).encode(
    x=alt.X('Fat_g:Q',axis=alt.Axis(title='Fat (g)')),
    y=alt.Y('Calories_kcal:Q',axis=alt.Axis(title='Calories (kcal)')),
    color=alt.Color('veryPopular:N', scale=alt.Scale(scheme='dark2')),
    tooltip = ['Title', 'Fat_g:Q','Calories_kcal:Q']
).add_selection(
        selectServing,
).transform_filter(selectServing).properties(
    width=600,height=500
)
# chart4

#######################################
####Design Process Chart Examples######
#######################################
###Create vis with selection options for X and Y
# y_axis_options = ['calcium_per_serving', 'copper_per_serving', 'iron_per_serving', 'selenium_per_serving', 'vit_A_per_serving',
#                 'vit_C_per_serving', 'vit_D_per_serving', 'zinc_per_serving']
# y_axis_select = st.selectbox(label='Select what you want the Y axis to be: ',
#                     options=y_axis_options)

# x_axis_options = ['copper_per_serving', 'iron_per_serving', 'selenium_per_serving', 'vit_A_per_serving',
#                 'vit_C_per_serving', 'vit_D_per_serving', 'zinc_per_serving','calcium_per_serving']
# x_axis_select = st.selectbox(label='Select what you want the X axis to be: ',
#                     options=x_axis_options)

# soup_nutrients = alt.Chart(chicken_soups).mark_circle(size=80,opacity=0.5).encode(
#     x=x_axis_select,
#     y=y_axis_select
# )

#dairy drop-down example
cy_options=list(open_food_soups["hasDairy"].unique())

widget=alt.binding_select(options=cy_options,name='Items with Dairy?: ')
selectServing=alt.selection_single(fields=['hasDairy'],init={'hasDairy':cy_options[0]},bind=widget)
# colorCondition = alt.condition(selectServing,alt.Color('hasDairy:N'),alt.value('orange'))

c4=alt.Chart(open_food_soups).mark_point().encode(
    y=alt.Y("calcium_value:Q", axis=alt.Axis(title='Calcium (mg)')),
    x=alt.X("hasBone:N", axis=alt.Axis(title='Contains Bone-in Chicken or Broth')),
    tooltip=['product_name_en:N', 'calcium_value:Q']
).add_selection(
        selectServing,
    ).transform_filter(selectServing)

c5=alt.Chart(open_food_soups).mark_point().encode(
    y=alt.Y("calcium_value:Q", axis=alt.Axis(title='Calcium (mg)')),
    x=alt.X("hasAllergens:N", axis=alt.Axis(title='Has Allergens')),
    tooltip=['product_name_en:N', 'calcium_value:Q']
).add_selection(
        selectServing,
    ).transform_filter(selectServing)

source = data.cars()

##brush example!
brush = alt.selection(type='interval')

points = alt.Chart(source).mark_point().encode(
    x='Horsepower:Q',
    y='Miles_per_Gallon:Q',
    color=alt.condition(brush, 'Origin:N', alt.value('lightgray'))
).add_selection(
    brush
)

bars = alt.Chart(source).mark_bar().encode(
    y='Origin:N',
    color='Origin:N',
    x='count(Origin):Q'
).transform_filter(
    brush
)

############################
### Display blog sections###
############################

section_options = ['Learning Objectives','The Data','The Design Process', 'Inspiration', 'Evaluation',
                    'Nutrient Facts Distributions', 'Dairy Content and Nutrition', 'Flu-Fighting Nutrients',
                    'Recipes By Serving Size']

with st.sidebar:
    chart_options_select = st.selectbox(label='Select a section to view: ',
                    options=section_options)

if chart_options_select == 'Learning Objectives':
    st.title('Learning Objectives')
    st.write('The viewer will be able to:')
    '''
    - Identify the most prevalent root vegetable(s) used in chicken soup recipes. (static only)
    - Compare the nutrition value (fat/calories/etc) of various chicken soup recipes. (interactive & static)
    - Summarize the variety of flu-fighting nutrients in various chicken soup recipes. (interactive & static)
    - Evaluate various soup recipes based on their popularity, presence of dairy and allergens, and nutrition (interactive)
    '''

elif chart_options_select == 'The Design Process':
    '''
    In early stages of the design process, I started out with some basic interactions on a few of the recipe attributes (as shown in
    the example above) in order to explore what might be possible with the data. The first visualization I attempted allowed the user to select both the x and y
    axes from various nutritional value options. In attempt to provide an example of this visualization, I unfortunately found that the code
    utilizing streamlit drop-down seemed to be pervasive throughout the document and display the drop-down along with every visualization despite
    attempts to remove it. This proved a challenge for moving forward with this type of interaction and so I decided to remove that from my final selection.
    '''
    st.write((c4|c5))
    '''
    I also had a few examples like the one above where I was simply playing with what variables could be included in different selectors
    or encoded with color. I felt, though, that my early interactions were quite limited since the interaction was not providing much 
    to the viewer in terms of added expressiveness.
    '''
    '''
    In some stages of the design process, 
    '''


elif chart_options_select == 'The Data':
    '''The 300+ recipes and their respective nutrition and ingredient details have been accessed from [Spoonacular's API](https://spoonacular.com/food-api).
    I began by leveraging a recipe parsing document and customizing it, in order to explore the elements of the data.
    I wanted to get a sense of all of the data that was available within the set of JSON documents and spent a good amount
    of time in the early stages of the project simply trying to understand what attributes could be utilized or manipulated
    to include in visualizations. I found that the most accessible and applicable data was the nutrition and ingredient information, 
    so I began by parsing the JSON objects to access various key nutrient data points and then converting it to a pandas dataframe 
    and ultimately writing to a new CSV file.  '''
    '''
    I felt that there were some limitations for interactivity in my original data. In particular, the original ingredient data
    that I had parsed and saved to a csv file did not have enough attributes to create any interactive visualizations of interest.
    This led me to scour the internet for more information and additional data was also sourced from the [Open Food Facts](https://world.openfoodfacts.org/)
    website, which "is a food products database made by everyone, for everyone." This data had a lot of great attributes about manufactured chicken
    soups as opposed to my original data set of homemeade recipes, along with their countries of origin, packaging, nutritional facts, ingredients, and more.
    Howeever, the data required a lot more clean up and so ultimately only made it into one of the final visualizations I selected.'''

elif chart_options_select == 'Inspiration':
    ''''Much of my inspiration for the interactive stage of the project came from reading through the documentation for altair. Since I am still quite
    new to Altair, I felt limited in terms of creating in altair whatever visualizations I might have imagined in my mind. For this reason, I started reading
    through the documentation and example code for various types of interactions in the Altair documentation. I began by recreating them for myself in
    order to understand how the code worked. For example, one of my visualizations is very much inspired by the example below because I felt it translated well
    into giving the viewer some insight into the distribution of recipes both with/without dairy and with/without allergens.'''
    points & bars

elif chart_options_select == 'Nutrient Facts Distributions':
    st.title('What is the nutritional distribution of various chicken soup recipes?')
    chart1
    '#### Interaction Notes: '
    '''
    * Select an interval in any one of the bar charts to highlight the adjusted distribution for that particular interval in all of the charts.
    '''

elif chart_options_select == 'Dairy Content and Nutrition':
    st.title('How does dairy content impact the amount of Protein and Calcium in a chicken soup recipe?')
    chart2
    '#### Interaction Notes: '
    '''
    * Hovering over each recipe (data point) will change the color and size of that particular recipe in the target chart, as well as, align this same interaction in the 3 other charts.
    * The tooltip provides additional details for each recipe: Title and Amount of each plotted nutritional element.
    * Each point's color is encoded to indicate that recipe's Health Score as defined by Spoonacular. Health Score is on a 0 to 100 point scale.
    '''

elif chart_options_select == 'Flu-Fighting Nutrients':
    st.title("Does the presence of flu-fighting nutrients impact a chicken soup recipe's health score?")
    chart3
    '#### Interaction Notes: '
    '''
    * Brush over the data points to select an interval of data and the target data points will remain in color, while the rest will fade to grey.
    * As the interval is selected in the scatterplot, the bar chart will filter to only those data points
    * The color of the bar plot is double encoded to show the count of recipes that also contain allergies.
    '''

elif chart_options_select == 'Recipes By Serving Size':
    st.title("Does a recipe's fat content, calorie content, or serving size impact its popularity?")
    chart4
    '#### Interaction Notes: '
    '''
    * Hover over each data point to view a tooltip with additional recipe details: Title, Amount of Fat, and Amount of Calories.
    * Utilize the drop-down to select only the recipes with a specific serving size.
    '''