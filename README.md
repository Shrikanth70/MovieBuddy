# MovieBuddy
**MovieBuddy** is a dynamic movie discovery web app built with Streamlit and powered by the TMDB API, delivering real-time trending films and personalized recommendations. Explore detailed movie insights, ratings, and related titles through a sleek, cinematic interface designed for effortless browsing. 🎬✨

https://moviebuddy-12.streamlit.app/

**MovieBuddy** is a dynamic movie discovery web application built using **Streamlit** and powered by the **TMDB (The Movie Database) API**.
It allows users to explore trending movies, view detailed information, and receive intelligent movie recommendations — all in a sleek, cinematic dark-themed interface.

---

## 🚀 Live Features

* 🔥 Daily Featured Movie Rotation
* 🎥 Detailed Movie Information Page
* ⭐ Ratings & Overview Display
* 📺 OTT Streaming Availability (Watch Providers)
* 🎯 Dynamic Movie Recommendations
* 🔄 Real-Time Data via TMDB API
* 🖤 Modern Cinematic UI (Dark + Gold Theme)
* ⚡ Fast Performance with Caching
* 🏠 Clickable Logo Navigation to Home
* 📱 Premium Mobile Responsive Layout

---

## 🛠 Tech Stack

* **Frontend & App Framework:** Streamlit
* **Backend API:** TMDB REST API
* **Language:** Python
* **Styling:** Custom CSS (Injected into Streamlit)
* **State Management:** Streamlit Session State
* **Deployment Ready:** Streamlit Cloud / Render

---

## 📂 Project Structure

```
MovieBuddy/
│
├── app.py                # Main Streamlit application
├── tmdb_service.py       # TMDB API calls & data handling
├── components.py         # UI components (cards, layouts)
├── requirements.txt      # Python dependencies
├── .gitignore            # Ignored files (API keys, cache, etc.)
└── README.md             # Project documentation
```

---

## 🔑 API Integration

MovieBuddy uses the official TMDB API endpoints:

* `/trending/movie/week`
* `/movie/{movie_id}`
* `/movie/{movie_id}/recommendations`

Data is fetched dynamically using your API key, meaning:

✔ Movie lists update automatically
✔ Ratings update live
✔ Recommendations change dynamically
✔ No static or hardcoded data

---

## 🖥 How It Works

### 🏠 Home Page

* Displays a trending movie slideshow
* Automatically rotates trending movies
* Shows backdrop, rating, and overview
* “Watch Now” opens detailed movie page

---

### 🎬 Movie Detail Page

When a user selects a movie:

* Fetches full movie details
* Displays poster, rating, release date, overview
* Calls recommendation endpoint
* Displays up to 8 related movies
* Clicking a recommendation loads its details dynamically

---

## ⚙ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/moviebuddy.git
cd moviebuddy
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add TMDB API Key

Create:

```
.streamlit/secrets.toml
```

Add:

```toml
TMDB_API_KEY = "your_api_key_here"
```

⚠ Do NOT commit this file to GitHub.

---

### 5️⃣ Run the App

```bash
streamlit run app.py
```

---

## ⚡ Performance Optimization

MovieBuddy uses:

```python
@st.cache_data(ttl=43200) # 12-hour cache
```

To cache:

* Trending movies
* Movie details
* Recommendations
* Watch Providers

This reduces API calls and improves speed.

---

## 😴 App Hibernation & Performance

**Note on Streamlit Community Cloud:**
On the free Streamlit Community Cloud platform, apps may go into "sleep mode" or hibernate if they remain inactive for a period of time (typically 24-48 hours). This is a platform-level behavior to manage resources and cannot be disabled directly through the application code.

**How MovieBuddy handles this:**
* **Optimized Cold Starts:** The app structure is modular, and heavy data fetching is wrapped in `@st.cache_data` with long TTLs to ensure that once the app wakes up, it remains highly responsive.
* **Efficient API Calls:** Minimal overhead during startup ensures the "wake-up" process is as fast as possible.
* **Pro-Tip:** If you require 24/7 "always-on" availability for a production environment, consider using an external uptime-monitoring service (like Cron-job.org or UptimeRobot) to ping the app URL periodically, or migrate to a dedicated VPS/Docker deployment.

---

## 🎨 UI Design Philosophy

The UI is inspired by modern streaming platforms:

* Dark cinematic background
* Gold gradient branding
* Hover effects on movie cards
* Rounded edges
* Soft shadows
* Clean minimal layout
* Full-width design (no sidebar)

---

## 🔐 Security Best Practices

* API key stored in `secrets.toml`
* `.gitignore` prevents sensitive data from upload
* No exposed credentials in public repository

---

## 🌍 Deployment

You can deploy this app easily on:

### ✅ Streamlit Cloud

* Connect GitHub repository
* Add API key in Streamlit Secrets
* Deploy instantly

### ✅ Render

* Use Python environment
* Add API key as environment variable

---

## 📈 Future Improvements

* 🎞 Genre-based filtering
* 🔍 Smart search with suggestions
* 👤 User login system
* ❤️ Watchlist feature
* 🎭 Actor profile pages
* 📊 Movie analytics dashboard
* 🤖 AI-powered recommendation system
* 🎨 Animated transitions

---

## 👨‍💻 Author

**Shrikanth**
Python Developer | Web App Builder | Streamlit Enthusiast

---

## 📜 License

This project is licensed under the MIT License.

---

# ⭐ If You Like This Project

Give it a star ⭐ on GitHub and feel free to fork it!

---

