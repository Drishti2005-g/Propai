# utils/ui_style.py
def load_css():
    return """
    <style>
    .stApp {
        background: none !important;
    }
    body {
        background-color: transparent !important;
    }

    .main-title {
        font-size: 40px;
        font-weight: 900;
        color: #8a4fff;
        text-align: center;
    }

    .tagline {
        font-size: 18px;
        text-align: center;
        color: white;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    .search-box input {
        border: 2px solid #8a4fff !important;
        background: rgba(255,255,255,0.9);
        padding: 14px;
        border-radius: 14px;
        font-size: 17px;
    }

    .card {
        background: rgba(255,255,255,0.12);
        backdrop-filter: blur(8px);
        padding: 15px;
        border-radius: 14px;
        color: white;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }

    .feature-card {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(6px);
        padding: 20px;
        color: white;
        border-radius: 14px;
        text-align: center;
    }
    </style>
    """
