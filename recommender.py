import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from database import load_veg_from_db, load_non_veg_from_db

def get_substitute(meat):
    # Load the dataset of non-vegetarian food ingredients and their nutrient information
    non_veg = load_non_veg_from_db()
    non_veg_df = pd.DataFrame(non_veg)

    # Load the dataset of vegetarian food ingredients and their nutrient information
    veg = load_veg_from_db()
    veg_df = pd.DataFrame(veg)

    # Preprocess the data
    non_veg_df = non_veg_df.drop(columns=['is_Veg',"Description","Nutrient_Data_Bank_Number","id"]) # Remove the "food_type" column
    veg_df = veg_df.drop(columns=['is_Veg',"Description","Nutrient_Data_Bank_Number","id"]) # Remove the "food_type" column
    df = pd.concat([non_veg_df, veg_df]) # Combine the non-veg and veg datasets
    df = df.dropna() # Remove any rows with missing nutrient values

    # Normalize the nutrient values
    nutrient_cols = [col for col in veg_df.columns if col != 'Category']
    veg_df[nutrient_cols] = (veg_df[nutrient_cols] - veg_df[nutrient_cols].min()) / (veg_df[nutrient_cols].max() - veg_df[nutrient_cols].min())

    # Feature selection
    X = veg_df[nutrient_cols] # Select the nutrient features
    y = veg_df['Category'] # Select the food ingredient labels

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train a decision tree classifier model
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    # Given a non-vegetarian food ingredient, predict the top recommended vegetarian substitutes
    non_veg_ingredient = meat
    non_veg_nutrients = non_veg_df[non_veg_df['Category']== non_veg_ingredient][nutrient_cols]
    non_veg_nutrients_norm = (non_veg_nutrients - df[nutrient_cols].min()) / (df[nutrient_cols].max() - df[nutrient_cols].min())
    
    try:
        veg_substitutes = clf.predict(non_veg_nutrients_norm).tolist()
    except:
        veg_substitutes = []
    
    veg_options = veg_df.sample(n=5)['Category'].tolist()

    return veg_substitutes + veg_options
