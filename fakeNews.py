import requests
import tkinter as tk
from tkinter import ttk
import textract


# News API endpoint and API key
news_api_url = "https://newsapi.org/v2/top-headlines"
api_key = "457b204d23224f93ba3079ef7c890de8"

# Country code for India
country = "in"

# News categories
categories = [
    "general",
    "entertainment",
    "health",
    "science",
    "sports",
    "technology",
    "User Input",  # Special option for user input
]


# Function to fetch news data from the API
def get_news(category):
    if category == "User Input":
        return []
    else:
        params = {
            "country": country,
            "category": category,
            "apiKey": api_key,
        }

        try:
            response = requests.get(news_api_url, params=params)
            response_data = response.json()
            articles = response_data["articles"]
            return articles
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news data: {e}")
            return None


# Function to perform simple fake news detection based on keywords
def detect_fake_news(text):
    keywords = list(set([
        "Hoax", "Fake", "Unreliable", "Unconfirmed", "Satire", "Misleading", "Sensational", "Clickbait", "Manipulated",
        "Propaganda", "Fabricated", "Conspiracy", "Rumor", "Exaggerated", "Deceptive", "Biased", "Scam", "Distorted",
        "Dubious", "Unsubstantiated", "Fraudulent", "Speculative", "Questionable", "Falsehood", "Disinformation",
        "Inaccurate", "Fictitious", "Phony", "Bogus", "Fabrication", "Fallacious", "Illusory", "Inauthentic",
        "Untrustworthy", "Pseudo", "Unverified", "Unreal", "Counterfeit", "Delusive", "Deceitful", "Preposterous",
        "Ambiguous", "Devious", "Fallacy", "Illusive", "Insidious", "Perjury", "Sham", "Slander", "Subterfuge",
        "Opinion Disguised as Fact", "unverified", "dubious", "speculative", "sensational", "misleading", "biased",
        "rumour", "conspiracy", "propaganda", "manipulation", "fabricated", "exaggerated", "unsubstantiated",
        "baseless","falsehood", "unreliable", "prejudiced", "hyperbolic", "opinion disguised as fact", "controversial",
        "selective reporting", "divisive", "nationalistic bias", "ethnic tensions", "communal disharmony",
        "misinformation","fabricated quotes", "polarizing", "concocted stories", "yellow journalism", "fake claims", "censorship claims",
        "satirical content", "urban legends", "ethnic stereotyping", "hoax", "fabricated", "misleading", "unverified",
        "debunked", "fictitious", "sensational", "conspiracy", "misinformation", "discredited", "propaganda",
        "deceitful","biased", "manipulation", "false", "unfounded", "distorted", "sensationalism", "unreliable", "clickbait",
        "pseudoscience", "unsubstantiated", "rumor", "partisan", "conspiracy theory", "manipulated", "counterfeit",
        "fraudulent", "distorted", "baseless", "exaggerated", "insidious", "uncorroborated", "sensationalized",
        "speculative", "dubious", "fallacious", "unauthenticated", "counterfeit", "specious", "hyperbolic", "concocted", "prejudiced",
        "deceptive", "spurious", "fallacy", "misinformation", "misleading", "false premise", "disinformation",
        "rumor mill", "deceit", "unreliable source", "misleading headline", "fraudulent claim", "unscrupulous", "erroneous",
        "unconfirmed","distorted facts", "truth distortion", "innuendo", "clickbait headline", "rumor mongering",
        "manipulated content", "contrived", "deceitful narrative", "sensationalist reporting", "contrived story", "deceptive tactics", "spin",
        "false narrative", "fiction", "unreliable information", "sensational reporting", "falsified evidence",
        "partial truth","partisan agenda", "rumor spreading", "deceptive framing", "biased reporting", "false attribution",
        "cherry-picked data","staged event", "misleading visuals", "hyper-partisan", "agenda-driven", "deceptive statistics",
        "false context","unverified source", "manipulated data", "selective quoting", "data distortion", "context manipulation",
        "opinion disguised as fact", "agenda-driven reporting", "cherry-picked quotes", "selective reporting",
        "manufactured controversy" ]))
    for keyword in keywords:
        if keyword.lower() in text.lower():
            return True
    return False


# Function to generate news cards with fake news detection
def generate_ui(articles):
    # Remove existing news cards
    for widget in container.winfo_children():
        widget.destroy()

    for item in articles:
        card_frame = ttk.Frame(container)
        card_frame.grid(row=len(container.winfo_children()) + 1, column=0)

        news_title_label = ttk.Label(card_frame, text=item["title"])
        news_title_label.grid(row=0, column=0)

        news_description_label = ttk.Label(card_frame, text=item["description"] or item["content"] or "")
        news_description_label.grid(row=1, column=0, columnspan=2)

        # Perform fake news detection
        news_text = f"{item['title']} {item['description']} {item['content']}"
        is_fake = detect_fake_news(news_text)
        fake_status_label = ttk.Label(card_frame, text="Fake" if is_fake else "Real")
        fake_status_label.grid(row=2, column=0, columnspan=2)

        read_more_button = ttk.Button(
            card_frame,
            text="Read More",
            command=lambda url=item["url"]: open_url(url),
        )
        read_more_button.grid(row=3, column=0, columnspan=2)


# Function to open news article URL in a browser
def open_url(url):
    import webbrowser

    webbrowser.open(url)


# Function to handle category selection from dropdown menu
def select_category(event):
    category = category_var.get()
    if category == "User Input":
        container.grid_remove()  # Hide the container for API-based news
        show_user_input()
    else:
        articles = get_news(category)
        if articles:
            generate_ui(articles)
            container.grid()  # Show the container for API-based news
        else:
            # In case of error or no articles for the selected category, display a message
            container.grid_remove()
            no_data_label = ttk.Label(root, text="No data available for this category.")
            no_data_label.grid(row=2, column=0)


# Function to show user input widgets
def show_user_input():
    user_input_label.grid(row=10, column=0, pady=5)
    user_input.grid(row=12, column=0, pady=5)
    fetch_button.grid(row=20, column=0, pady=5)
    result_label.grid(row=25, column=0)


# Function to hide user input widgets
def hide_user_input():
    user_input_label.grid_remove()
    user_input.grid_remove()
    fetch_button.grid_remove()
    result_label.grid_remove()


# Function to handle fake news detection for user-input article
def check_user_input():
    user_article = user_input.get("1.0", tk.END)
    is_fake = detect_fake_news(user_article)
    result_label.config(text="Fake" if is_fake else "Real")


# Create the main application window
root = tk.Tk()
root.title("News App")

# Dropdown menu for category selection
category_var = tk.StringVar(root)
category_var.set(categories[0])  # Set the default category to "general"
category_menu = ttk.OptionMenu(root, category_var, *categories, command=select_category)
category_menu.grid(row=1, column=0)

# Create a container frame to hold the news cards
container = ttk.Frame(root)
container.grid(row=2, column=0)

# Entry widget for user to input a news article
user_input_label = ttk.Label(root, text="Enter News Article:")
user_input = tk.Text(root, height=4, width=50)

# Button to trigger fake news detection for user-input article
fetch_button = ttk.Button(root, text="Check", command=check_user_input)

# Label to display the result of fake news detection for user-input article
result_label = ttk.Label(root, text="")

# Initial fetch and display news for the "general" category
initial_articles = get_news("general")
generate_ui(initial_articles)

# Start the main event loop
root.mainloop()
