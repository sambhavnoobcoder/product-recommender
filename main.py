import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

# Download necessary resources (run this once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize a dictionary to store tag frequencies
tag_frequencies = Counter()

# List of product descriptions
product_descriptions = [
    "Men Solid Polo Neck Poly Cotton Black T-Shirt",
    "Men Solid Polo Neck Cotton Blend Black T-Shirt",
    "Solid Men Polo Neck Poly Cotton Black T-Shirt",
    "Men Solid Polo Neck Cotton Blend (220 gsm) Green T-Shirt",
    "Men Typography Polo Neck Cotton Blend Black T-Shirt",
    "Solid Men Polo Neck Poly Cotton Black T-Shirt",
    "Men Solid Polo Neck Polyester Black T-Shirt",
]

# Define key feature categories with keywords
key_feature_categories = {
    'color': ['green', 'blue', 'red', 'black', 'white'],
    'cloth_material': ['cotton', 'blend'],
    'gender': ['men', 'women', 'unisex'],
    'type_of_cloth': ['shirt', 'dress', 'shoes', 'backpack']
}

def extract_key_features(description):
    # Tokenize the description
    tokens = word_tokenize(description.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Initialize a dictionary to store keyword frequencies
    keyword_frequencies = Counter()

    # Extract key features based on categories and keywords
    for token in lemmatized_tokens:
        for category, keywords in key_feature_categories.items():
            if token in keywords:
                keyword_frequencies[token] += 1

    return keyword_frequencies

# Initialize a dictionary to store category frequencies
category_frequencies = Counter()

# Process all product descriptions and extract key features
for description in product_descriptions:
    # Extract key features from description
    keyword_frequencies = extract_key_features(description)

    # Update keyword frequencies
    tag_frequencies.update(keyword_frequencies)

    # Update category frequencies
    for category, keywords in key_feature_categories.items():
        category_frequency = sum(keyword_frequencies[keyword] for keyword in keywords)
        category_frequencies[category] += category_frequency

# Sort categories by frequency in descending order
sorted_categories = sorted(category_frequencies, key=category_frequencies.get, reverse=True)

# Calculate the total number of possible keywords
total_possible_keywords = sum(len(keywords) for keywords in key_feature_categories.values())

# Calculate the ratios for each description
x_val = []              # storage for ratio
outer_ratios = []

# Initialize a dictionary to store keyword ratios for each description
keyword_ratio_per_description = {description: {} for description in product_descriptions}

for description in product_descriptions:
    keyword_frequencies = extract_key_features(description)
    total_description_keywords = sum(keyword_frequencies.values())
    ratio = total_description_keywords / total_possible_keywords
    x_val.append(ratio)

    # Calculate the value for this description
    value = ratio ** (category_frequencies[sorted_categories[0]] / total_possible_keywords)
    outer_ratios.append(value)

    # Calculate and store keyword ratios for this description
    inner_ratios = []      # this is the storage for inner ratio
    for category in sorted_categories:
        keywords = key_feature_categories[category]
        total_category_keywords = len(keywords)
        present_keywords = [keyword for keyword in keywords if keyword in keyword_frequencies]
        num_present_keywords = len(present_keywords)
        keyword_ratio = num_present_keywords / total_category_keywords
        inner_ratios.append(keyword_ratio)
        keyword_ratio_per_description[description][category] = keyword_ratio

    inner_ratio_sum = sum([inner_ratios[i] * (ratio ** inner_ratios[i]) for i in range(len(sorted_categories))])

    print("\nDescription: {}".format(description))
    print("Score for product description : {:.4f}".format(ratio * inner_ratio_sum))
    print("-" * 50)

# Ask the user to enter a product description
user_description = input("Enter a product description: ")

# Calculate and display the final score for the user-entered description
user_keyword_frequencies = extract_key_features(user_description)
user_total_description_keywords = sum(user_keyword_frequencies.values())
user_ratio = user_total_description_keywords / total_possible_keywords

user_outer_value = user_ratio ** (category_frequencies[sorted_categories[0]] / total_possible_keywords)
user_inner_ratios = []

for category in sorted_categories:
    keywords = key_feature_categories[category]
    total_category_keywords = len(keywords)
    present_keywords = [keyword for keyword in keywords if keyword in user_keyword_frequencies]
    num_present_keywords = len(present_keywords)
    user_keyword_ratio = num_present_keywords / total_category_keywords
    user_inner_ratios.append(user_keyword_ratio)

user_inner_ratio_sum = sum([user_inner_ratios[i] * (user_ratio ** user_inner_ratios[i]) for i in range(len(sorted_categories))])

print("\nUser-entered Description: {}".format(user_description))
print("Score for user-entered product description : {:.4f}".format(user_ratio * user_inner_ratio_sum))

# Find the closest product description to user's input
closest_description = None
closest_score_difference = float('inf')

for description in product_descriptions:
    keyword_frequencies = extract_key_features(description)
    total_description_keywords = sum(keyword_frequencies.values())
    ratio = total_description_keywords / total_possible_keywords

    outer_value = ratio ** (category_frequencies[sorted_categories[0]] / total_possible_keywords)
    inner_ratios = []

    for category in sorted_categories:
        keywords = key_feature_categories[category]
        total_category_keywords = len(keywords)
        present_keywords = [keyword for keyword in keywords if keyword in keyword_frequencies]
        num_present_keywords = len(present_keywords)
        keyword_ratio = num_present_keywords / total_category_keywords
        inner_ratios.append(keyword_ratio)

    inner_ratio_sum = sum([inner_ratios[i] * (ratio ** inner_ratios[i]) for i in range(len(sorted_categories))])

    # Calculate the absolute score difference
    score_difference = abs(user_ratio * user_inner_ratio_sum - ratio * inner_ratio_sum)

    if score_difference < closest_score_difference:
        closest_score_difference = score_difference
        closest_description = description

print("\nClosest Product Description to User's Input:")
print("Description: {}".format(closest_description))
print("Score Difference: {:.4f}".format(closest_score_difference))
