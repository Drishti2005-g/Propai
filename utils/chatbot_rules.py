import re

def clean(text):
    return text.lower().strip()

def match(patterns, text):
    text = clean(text)
    return any(re.search(p, text) for p in patterns)

def chatbot_reply(user_msg):

    msg = clean(user_msg)

    # 1 — Greetings
    if match([r"\bhello\b", r"\bhi\b", r"hey"], msg):
        return "Hey! 👋 How can I help you today with property info?"

    # 2 — Price related
    if match([r"price", r"cost", r"how much", r"rate"], msg):
        # detect location names
        location = None
        for area in ["whitefield", "koramangala", "indiranagar", "yelahnaka", "hebbal", "marathahalli"]:
            if area in msg:
                location = area
                break
        if location:
            return f"Prices in **{location.title()}** vary based on size. Use the *Smart Price Prediction* page for an accurate ML estimate! 🏡📊"
        return "For price estimation, use the *Smart Price Prediction* feature. It gives ML-powered predictions! 💸📈"

    # 3 — Location comparison
    if " vs " in msg or "better" in msg:
        return "Both areas have pros and cons! You can check current listings using *Search Properties* to compare. 😊"

    # 4 — Map view
    if match([r"map", r"location view"], msg):
        return "You can check the property map using the *Map View* section! 🗺️"

    # 5 — Fraud check related
    if match([r"fake", r"fraud", r"verify", r"real"], msg):
        return "Upload the property image in *Photo Verification* to check for tampering, AI-generated images, or inconsistencies! 🔍🤖"

    # 6 — Image type classification
    if match([r"what type", r"classify", r"is this property"], msg):
        return "Upload your photo in the *Image Classifier* section to detect whether it is an apartment, villa, plot, or office! 🏢🏠"

    # 7 — Listing property
    if match([r"list", r"sell", r"post"], msg):
        return "You can list your property on the *List Your Property* page! 📝"

    # 8 — About project
    if match([r"who are you", r"what are you", r"about"], msg):
        return "I'm *PropAI Assistant*, here to help you with property verification, pricing, and information! 🤖💙"

    # 9 — Thanks response
    if match([r"thank"], msg):
        return "Happy to help! 😊"

    # 10 — Default fallback
    return "I'm not fully sure about that 🤔. Try asking about pricing, locations, features, fraud check, or maps!"