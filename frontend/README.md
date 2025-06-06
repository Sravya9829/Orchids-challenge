# 🌸 Frontend - Website Cloner Interface

The user interface for the website cloning application. Built with React and Next.js.

## Quick start

```bash
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

**Important:** Make sure the backend is running on port 8000 first.

## What's the design like?

- Beautiful pink and rose colors (Orchids theme)
- Flower pattern background
- Works great on phones, tablets, and computers
- Smooth animations when you interact with things

## The main parts

### 1. Main Page (`src/app/page.tsx`)
This is where everything happens. It manages:
- Switching between the input form and results
- Checking the cloning progress every few seconds
- Showing errors if something goes wrong

### 2. URL Input (`src/components/URLInputs.tsx`)
The form where you type the website URL:
- Checks if the URL looks valid
- Shows a spinning loader when working
- Pretty error messages if something's wrong

### 3. Status Tracker (`src/components/CloneStatus.tsx`)
Shows what's happening during cloning:
- Yellow circle = Starting up
- Blue circle = Working on it
- Green checkmark = Done!
- Red X = Something went wrong

### 4. Preview Area (`src/components/PreviewPane.tsx`)
Shows the results when done:
- Side-by-side view of original and clone
- HTML code viewer
- Download button to save the result

## How the pieces work together

```
User types URL → URLInput sends to backend → 
Page polls for updates → Status shows progress → 
Preview shows final result
```

## The tech stuff

**Built with:**
- Next.js 14 (React framework)
- TypeScript (for catching errors)
- Tailwind CSS (for styling)

**Main files:**
- `src/app/page.tsx` - Main application logic
- `src/components/` - All the UI pieces
- `src/utils/api.ts` - Talks to the backend
- `src/types/index.ts` - TypeScript definitions

## Common problems

**Page won't load?**
- Check if Node.js is installed: `node --version`
- Try: `rm -rf node_modules && npm install`

**Can't clone websites?**
- Make sure backend is running on port 8000
- Check browser console (F12) for errors

**Looks broken on mobile?**
- It should work fine, try refreshing
- Check if you're using a very old browser

## Making changes

The code is organized simply:
- Each component is in its own file
- Styles use Tailwind classes
- TypeScript helps catch mistakes
- Hot reload means changes appear instantly

**Available commands:**
```bash
npm run dev      # Start development
npm run build    # Build for production
npm run lint     # Check for code issues
```

---

Simple, beautiful, and effective frontend for website cloning! 🌸