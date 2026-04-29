import base64
import folium
import sys
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT, "utils"))

import streamlit as st
import pandas as pd
import pickle
from PIL import Image

# ============================================================
# PATH SETUP
# ============================================================
ASSETS = os.path.join(ROOT, "assets")
DATA = os.path.join(ROOT, "data")
MODELS = os.path.join(ROOT, "models")
PROPERTIES_CSV = os.path.join(DATA, "properties.csv")
HOUSE_PRICE_MODEL = os.path.join(MODELS, "house_price_model.pkl")
# -------------------------
# Card CSS for property UI
# -------------------------
CARD_STYLE = """
<style>
.property-card {
    background: #ffffff;
    border-radius: 15px;
    padding: 18px;
    margin: 15px;
    width: 300px;
    display: inline-block;
    vertical-align: top;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    transition: 0.3s;
}
.property-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.prop-title {
    font-size: 18px;
    font-weight: 700;
    color: #5b2cff;
    margin-bottom: 6px;
}
.prop-details {
    color: #444;
    font-size: 14px;
    margin-top: 6px;
}
.badge {
    padding: 4px 10px;
    border-radius: 10px;
    font-size: 12px;
    color: #fff;
    display: inline-block;
    margin-top: 8px;
}
.verified { background: #4CAF50; }
.suspicious { background: #FF9800; }
.fraud { background: #E53935; }
</style>
"""
# Inject it so it's available for the whole app
st.markdown(CARD_STYLE, unsafe_allow_html=True)

# ============================================================
# STREAMLIT CONFIG  (FORCE LIGHT MODE)
# ============================================================
st.set_page_config(
    page_title="PropAI – Smart Real Estate Intelligence",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)
# GLOBAL BACKGROUND
bg_path = os.path.join(ASSETS, "bg.jpg")
bg_bytes = open(bg_path, "rb").read()
bg_base64 = base64.b64encode(bg_bytes).decode()

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;stream
        background-repeat: no-repeat;
    }}

    .main-box {{
        background: rgba(255,255,255,0.8);
        padding: 40px;
        border-radius: 15px;
        backdrop-filter: blur(6px);
        max-width: 800px;
        margin: auto;
        margin-top: 80px;
    }}
    </style>
""", unsafe_allow_html=True)
login_col = st.columns([8,1])[1]

with login_col:
    # If user is logged in
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        username = st.session_state.get("username", "User")

        # Profile Menu Button
        selected = st.selectbox(
            "",
            ["👤 " + username, "My Profile", "My Listings", "Logout"],
            label_visibility="collapsed"
        )

        # Handle menu selection
        if selected == "Logout":
            st.session_state.clear()
            st.experimental_rerun()

        elif selected == "My Profile":
            st.session_state["menu_override"] = "profile_page"

        elif selected == "My Listings":
            st.session_state["menu_override"] = "my_listings_page"

    else:
        # Show Login Button
        st.markdown(
            "<a href='/?Login / Signup' style='padding:8px 16px; background:#8a4fff; color:white; "
            "border-radius:8px; text-decoration:none; font-size:14px;'>Login / Signup</a>",
            unsafe_allow_html=True
        )
    bg_path = os.path.join(ASSETS, "bg.jpg")
    bg_bytes = open(bg_path, "rb").read()
    bg_base64 = base64.b64encode(bg_bytes).decode()
st.markdown("""
    <style>
        body, .stApp {
            background: url("data:image/jpg;base64,{bg_base64}")no-repeat center center fixed !important;
            background-size: cover 1important;
        }
        .stSidebar {
            background-color: #f3e9ff !important;
            border-right: 1px solid #d9c9ff !important;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# GLOBAL CSS (HOME PAGE + SEARCH BAR + SIDEBAR STYLE)
# ============================================================
def inject_css():
    st.markdown("""
        <style>

        /* Background image */
        .stApp {
            background: url('/assests/bg.jpg') no-repeat center center fixed !important;
            background-size: cover !important;
            opacity: 0.97;
        }

        /* White blur overlay for readability */
        .main-content {
            backdrop-filter: blur(5px);
            background: rgba(255,255,255,0.75);
            padding: 20px;
            border-radius: 15px;
            margin-top: -40px;
        }

        </style>
    """, unsafe_allow_html=True)
    # ========= GLOBAL CARD CSS ===========
    CARD_CSS = """
    <style>
    .card {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        transition: 0.2s ease;
        border: 1px solid #eee;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
    }

    .prop-title {
        font-size: 18px;
        font-weight: 700;
        color: #333;
    }

    .prop-details {
        font-size: 14px;
        color: #555;
        margin-top: 6px;
    }

    .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 12px;
        margin-top: 10px;
        font-weight: 600;
    }

    .badge.trustworthy {
        background: #d4f8d4;
        color: #0b7a0b;
    }

    .badge.suspicious {
        background: #ffd6d6;
        color: #cc0000;
    }

    </style>
    """
    st.markdown(CARD_CSS, unsafe_allow_html=True)
inject_css()
st.markdown(CARD_STYLE,unsafe_allow_html=True)

# ============================================================
# SIMPLE HELPERS (NO MAP YET)
# ============================================================
def load_price_model():
    try:
        with open(HOUSE_PRICE_MODEL, "rb") as f:
            return pickle.load(f)
    except:
        return None

price_model = load_price_model()

# ============================================================
# PAGE FUNCTIONS
# ============================================================

# ---------- HOME ----------

def home_page():
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>🏡 PropAI – Smart Real Estate Intelligence</h1>", unsafe_allow_html=True)

    # SEARCH BAR (WORKING)
    search = st.text_input("", placeholder="Search properties, location, BHK…")

    if st.button("Search"):
        st.session_state["search_query"] = search
        st.session_state["go_to_search"] = True
        st.success("Searching... Go to Search Properties page!")

    # Move tagline BELOW search bar:
    st.markdown("<p style='text-align:center; font-size:18px;'>Find your dream home with AI-powered fraud detection & insights.</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
def render_property_card(row):
    fraud = row["fraud_status"]

    # Choose badge color
    if fraud == "VERIFIED":
        badge_color = "#1B5E20"  # dark green
        badge_text = "Verified ✔️"
    elif fraud == "SUSPICIOUS":
        badge_color = "#F57F17"  # amber
        badge_text = "Suspicious ⚠️"
    else:
        badge_color = "#B71C1C"  # red
        badge_text = "Fraud 🚨"

    html = f"""
    <div class="card">
        <div class="prop-title">{row['location']} — {row['size']}</div>

        <div class="prop-details">
            <b>{row['total_sqft']} sqft</b><br>
            <b>{row['bath']} Bathrooms</b><br>
            <b>₹{row['price']} Lakhs</b>
        </div>

        <div class="badge" style="background:{badge_color}">
            {badge_text}
        </div>
    </div>
    """

    return html


# ---------- FIND PROPERTY ----------
def find_property():
    st.title("Search Properties 🔍")
    st.write("Browse properties from your dataset.")

    df = pd.read_csv(PROPERTIES_CSV)
    # APPLY SEARCH
    if "search_query" in st.session_state and st.session_state["search_query"]:
        query = st.session_state["search_query"].lower()
        df = df[df["location"].str.lower().str.contains(query)]

    # Add fraud status
    from utils.fraud_detector import fraud_score
    df["fraud_status"] = df.apply(lambda r: fraud_score(r), axis=1)

    # --------------------------
    # 🔽 DROPDOWN FILTER
    # --------------------------

    # Extract unique locations
    area_list = sorted(df["location"].dropna().unique().tolist())

    # Add "All Locations" option on top
    area_list = ["All Locations"] + area_list

    selected_area = st.selectbox(
        "Select Area / Location",
        area_list
    )

    # Filter dataset
    if selected_area != "All Locations":
        df = df[df["location"] == selected_area]

    # If nothing found
    if df.empty:
        st.warning("No properties found in this area.")
        return

    # --------------------------
    # EXISTING CARD GRID (UNCHANGED)
    # --------------------------
    cols = st.columns(3)
    index = 0

    for _, row in df.iterrows():
        with cols[index]:
            st.markdown(render_property_card(row), unsafe_allow_html=True)

        index += 1
        if index == 3:
            index = 0
            cols = st.columns(3)
# ---------- PRICE PREDICTION ----------
def price_prediction():
    st.title("Price Prediction 💰")
    if price_model is None:
        st.error("Model not loaded.")
        return

    sqft = st.number_input("Total Sqft", min_value=500, max_value=10000, value=1200)
    bath = st.number_input("Bathrooms", 1, 5, 2)
    bhk = st.number_input("BHK", 1, 6, 2)
    location = st.text_input("Location")

    if st.button("Predict Price"):
        input_df = pd.DataFrame([{
            "total_sqft": sqft,
            "bath": bath,
            "bhk": bhk,
            "location": location
        }])
        price = price_model.predict(input_df)[0]
        st.success(f"Predicted Price: ₹ {round(price, 2)} Lakhs")

# ---------- PHOTO VERIFICATION ----------

from utils.photo_verification import analyze_image

def photo_verification():
    st.title("Photo Verification 📷")
    st.write("Upload property image to analyze authenticity.")

    uploaded = st.file_uploader("Upload property image", type=["jpg", "jpeg", "png"])

    if uploaded:
        img = Image.open(uploaded)
        st.image(img, caption="Uploaded Image", use_container_width=True)

        result, issues, exif, ela = analyze_image(img)

        st.subheader("🔍 Verification Result")

        if result == "VERIFIED":
            st.success("Image looks authentic ✔️")
        elif result == "SUSPICIOUS":
            st.warning("Image appears suspicious ⚠️")
        else:
            st.error("Image may be AI-generated or edited 🚨")

        st.subheader("📌 Issues Found")
        if issues:
            for i in issues:
                st.write(f"- {i}")
        else:
            st.write("No inconsistencies found.")

        st.subheader("📷 ELA Preview (Error Level Analysis)")
        st.image(ela, caption="ELA Result", use_container_width=True)

        st.subheader("📝 EXIF Metadata")
        if exif:
            st.json(exif)
        else:
            st.write("No metadata found (common for AI-generated images).")
def classify_image_page():
    st.title("🖼️ Image Classifier")

    uploaded = st.file_uploader("Upload a property image", type=["jpg", "jpeg", "png"])

    if uploaded:
        # preview image
        img = Image.open(uploaded)
        st.image(img, caption="Uploaded Image", use_container_width=True)

        # save temporarily
        temp_path = "temp_property_image.jpg"
        with open(temp_path, "wb") as f:
            f.write(uploaded.getbuffer())

        # import classifier
        from image_classifier import classify_property

        # run model
        result = classify_property(temp_path)

        st.subheader("🔍 Classification Result")
        st.success(f"🏠 This image looks like a **{result}** property.")
# ---------- LIST YOUR PROPERTY ----------
def list_property():
    st.title("List Your Property 🏠")

    st.write("Add your property details and save it to the database.")

    # --- FORM ---
    area_type = st.selectbox("Area Type", ["Super built-up Area", "Built-up Area", "Plot", "Villa"])
    availability = st.selectbox("Availability", ["Ready To Move", "Immediate", "18-Dec", "20-Jan"])
    location = st.text_input("Location")
    size = st.text_input("Size (ex: 2 BHK)")
    society = st.text_input("Society Name")
    total_sqft = st.number_input("Total Sqft", min_value=100, max_value=10000, value=1200)
    bath = st.number_input("Bathrooms", min_value=1, max_value=5, value=2)
    balcony = st.number_input("Balcony", min_value=0, max_value=3, value=1)
    price = st.number_input("Price (Lakhs)", min_value=1, max_value=999, value=50)
    bhk = st.number_input("BHK", min_value=1, max_value=6, value=2)
    locality = st.text_input("Locality")
    area = st.text_input("Area")
    price_unit = st.selectbox("Price Unit", ["Lakhs", "Cr"])
    region = st.text_input("Region")
    status = st.text_input("Status")
    age = st.text_input("Property Age")
    owner = st.text_input("Owner Name")
    posted_date = str(pd.Timestamp.today().date())

    if st.button("Submit Property"):
        df = pd.read_csv(PROPERTIES_CSV)

        new_row = {
            "area_type": area_type,
            "availability": availability,
            "location": location,
            "size": size,
            "society": society,
            "total_sqft": total_sqft,
            "bath": bath,
            "balcony": balcony,
            "price": price,
            "bhk": bhk,
            "type": "Not Available",
            "locality": locality,
            "area": area,
            "price_unit": price_unit,
            "region": region,
            "status": status,
            "age": age,
            "owner": owner,
            "posted_date": posted_date
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(PROPERTIES_CSV, index=False)

        st.success("Property successfully added!")
        st.info("Go to 'Search Properties' to see your new listing.")
# ---------- CHATBOT ----------
def chatbot():
    st.header("🤖 AI-Chatbot")
    st.markdown("Type anything about properties, pricing or AI verification!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user = st.text_input("Ask something...", key="chat_msg")

    if st.button("Send"):
        from utils.chatbot_rules import chatbot_reply
        reply = chatbot_reply(user)

        st.session_state.chat_history.append(("You", user))
        st.session_state.chat_history.append(("PropAI Bot", reply))

    # display
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**🧠 PropAI Bot:** {message}")
# -----------------------------
#   MAP VIEW PAGE (with Auto Geocoding)
# -----------------------------
def mapview():
    st.title("🗺️ Property Map View")

    st.write("Showing default map (no coordinates available in dataset).")

    try:
        # Show Bengaluru default map
        lat, lon = 12.9716, 77.5946  # Bengaluru center
        m = folium.Map(location=[lat, lon], zoom_start=12)

        # Render map
        st.components.v1.html(m._repr_html_(), height=600)
    except Exception as e:
        st.error(f"Map loading failed: {e}")
# ---------- ABOUT ----------
def about():
    st.title("About 📄")
    st.write("PropAI helps verify homes, check fraud, predict prices and more.")
def login_page():
    import streamlit as st
    from utils.auth import login_user, signup_user

    st.title("🔐 Login / Signup")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    # ---------------- LOGIN ----------------
    with tab1:
        st.subheader("Login to your account")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            ok, username = login_user(email, password)

            if ok:
                st.success(f"Welcome back, {username}! 💜")

                # 🔥 SAVE SESSION HERE (THIS WAS MISSING)
                st.session_state["logged_in"] = True
                st.session_state["username"] = username

            else:
                st.error(username)

    # ---------------- SIGNUP ----------------
    with tab2:
        st.subheader("Create a new account")
        name = st.text_input("Name", key="su_name")
        email = st.text_input("Email", key="su_email")
        password = st.text_input("Password", key="su_password", type="password")

        if st.button("Create Account"):
            ok, msg = signup_user(name, email, password)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
def profile_page():
    st.title("👤 My Profile")

    if "logged_in" not in st.session_state:
        st.warning("Please login first.")
        return

    st.success(f"Logged in as: {st.session_state['username']}")
    st.write("Email: (stored internally)")
    st.write("Profile features coming soon…")
def my_listings_page():
    st.title("📦 My Listings")

    if "logged_in" not in st.session_state:
        st.warning("Please login first.")
        return

    st.info("In the future, this page will show all properties uploaded by this user.")

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
menu = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🔍 Search Properties",
        "💰 Price Prediction",
        "📷 Photo Verification",
        "🖼️ Image Classifier",
        "🏡 List Your Property",
        "🤖 AI-Chatbot",
        "🗺️ Map View",
        "ℹ️ About",
        "Login/Signup"
    ]
)
# Handle profile or listings override
if "menu_override" in st.session_state:
    menu = st.session_state["menu_override"]
if menu == "🏠 Home":
    home_page()
elif menu == "🔍 Search Properties":
    find_property()
elif menu == "💰 Price Prediction":
    price_prediction()
elif menu == "📷 Photo Verification":
    photo_verification()
elif menu == "🖼️ Image Classifier":
    classify_image_page()
elif menu == "🏡 List Your Property":
    list_property()
elif menu == "🤖 AI-Chatbot":
    chatbot()
elif menu == "🗺️ Map View":
    mapview()
elif menu == "ℹ️ About":
    about()
elif menu=="Login/Signup":
    login_page()
elif menu == "profile_page":
    profile_page()
elif menu == "my_listings_page":
    my_listings_page()