# 🌸 Orchids Website Cloner

AI-powered website cloning application that recreates any website with modern design.

## What does this do?

Give it any website URL, and it will create a beautiful modern version of that website for you. It uses AI to understand the original design and recreates it with a fresh, responsive layout.

## What you need on your laptop

1. **Node.js** (version 18 or newer) - Download from https://nodejs.org/
2. **Python** (version 3.8 or newer) - Download from https://python.org/downloads/
3. **uv** (Python package manager) - Install with: `pip install uv`
4. **Google Gemini API Key** (free) - Get from https://makersuite.google.com/app/apikey

## How to set it up

### Step 1: Get the code
```bash
# Download or clone this project
cd ORCHIDS-CHALLENGE
```

### Step 2: Set up the backend
```bash
cd backend

# Install everything needed
uv sync
uv add playwright beautifulsoup4 requests pillow google-generativeai python-dotenv
uv run playwright install chromium

# Create the .env file
touch .env
```

Open `backend/.env` and add your API key:
```
GEMINI_API_KEY=your_api_key_here
```

### Step 3: Set up the frontend
```bash
cd frontend
npm install
```

## How to run it

You need two terminal windows open:

**Terminal 1 (Backend):**
```bash
cd backend
uv run fastapi dev
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Then open your browser and go to: `http://localhost:3000`

## How to use it

1. Enter any website URL (like `https://example.com`)
2. Click "Clone Website"
3. Wait for it to analyze and recreate the website
4. See the beautiful result and download it if you want

## What's inside

```
ORCHIDS-CHALLENGE/
├── backend/           # Python API that does the cloning
│   ├── services/
│   │   ├── scraper.py    # Gets content from websites
│   │   └── ai_cloner.py  # Uses AI to recreate websites
│   └── routers/
│       └── clone.py      # API endpoints
├── frontend/          # React website interface
│   ├── src/
│   │   ├── components/   # UI pieces
│   │   └── app/         # Main pages
└── README.md          # This file
```

## If something goes wrong

**Backend won't start?**
- Make sure Python is installed: `python --version`
- Check if uv is working: `uv --version`
- Try reinstalling: `cd backend && uv sync`

**Frontend won't start?**
- Make sure Node.js is installed: `node --version`
- Try: `cd frontend && rm -rf node_modules && npm install`

**Can't connect to the cloning service?**
- Make sure both backend and frontend are running
- Check `http://localhost:8000/docs` works
- Your API key might be wrong - check `backend/.env`

**Cloning fails or times out?**
- Some websites block automated access
- Try with simple sites like `https://example.com` first
- The system has fallbacks, so it should still work

## Need help?

1. Check the terminal for error messages
2. Visit `http://localhost:8000/docs` to see if the backend is working
3. Check your browser's developer tools (F12) for any errors

---

Made for the Orchids SWE Internship with ❤️