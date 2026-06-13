# Frontend Setup Guide

Quick guide to set up and run the React frontend for the Ticket Resolution AI platform.

## 📋 Prerequisites

Before starting, ensure you have:
- **Node.js** v14+ installed ([Download](https://nodejs.org/))
- **npm** v6+ installed (comes with Node.js)
- **Backend API** running on `http://localhost:8000`

Verify your installation:
```bash
node --version
npm --version
```

## 🚀 Installation Steps

### Step 1: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

This will download and install all required packages (React, React DOM, Axios, etc.).

### Step 3: Start Development Server
```bash
npm start
```

The application will automatically open in your browser at `http://localhost:3000`

If it doesn't open automatically, go to: `http://localhost:3000`

## 📝 What You'll See

After starting the development server, you'll see:

1. **Dashboard Tab** - Overview of system status and recent tickets
2. **Create Ticket Tab** - Form to create new issues
3. **Results Tab** - Detailed analysis of selected tickets
4. **Health Indicator** - System status in the header

## 🔌 API Connection

The frontend is configured to proxy requests to the backend:
- Requests to `/health`, `/issues`, etc. are automatically forwarded to `http://localhost:8000`
- This is configured in `package.json` with `"proxy": "http://localhost:8000"`

## 🛠️ Development Commands

### Start Development Server
```bash
npm start
```
Runs the app in development mode with hot reload.

### Build for Production
```bash
npm run build
```
Creates an optimized production build in the `build/` folder.

### Run Tests
```bash
npm test
```
Launches the test runner.

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── CreateIssue.jsx
│   │   ├── HealthStatus.jsx
│   │   └── IssueResult.jsx
│   ├── App.jsx
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## 🎯 Features

- ✅ Dashboard with system overview
- ✅ Create new tickets with issue description and severity
- ✅ View detailed analysis results with root cause and remediation steps
- ✅ Real-time system health status
- ✅ Responsive design (works on desktop, tablet, mobile)
- ✅ Smooth animations and transitions

## 🔧 Customization

### Change API URL
Edit the `"proxy"` field in `package.json`:
```json
"proxy": "http://your-api-server.com"
```

### Change Port
```bash
PORT=3001 npm start
```

### Add Environment Variables
Create a `.env` file:
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_NAME=Ticket Resolution AI
```

Then use in code:
```javascript
const apiUrl = process.env.REACT_APP_API_URL;
```

## 🐛 Troubleshooting

### "npm: command not found"
- Node.js is not installed. Download from [nodejs.org](https://nodejs.org/)

### "Port 3000 already in use"
```bash
# Use a different port
PORT=3001 npm start
```

### API Connection Errors
1. Check if backend is running: `http://localhost:8000/health`
2. Check browser console for CORS errors
3. Verify proxy in `package.json`

### "Module not found" errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Hot reload not working
- Ensure file changes are saved
- Check for syntax errors
- Try restarting: Ctrl+C and `npm start` again

## 📦 Dependencies

- **react** - UI library
- **react-dom** - React DOM rendering
- **react-scripts** - Build scripts and config
- **axios** - HTTP client (optional)

## 🌐 Deployment

### Deploy to Vercel
```bash
npm install -g vercel
vercel
```

### Deploy to Netlify
```bash
npm run build
# Upload 'build' folder to Netlify
```

### Deploy to Azure
See backend deployment guide for Azure App Service integration.

## 📚 Learn More

- [React Documentation](https://react.dev)
- [Create React App Guide](https://create-react-app.dev)
- [Backend Documentation](../README.md)

## ✅ Verification Checklist

- [ ] Node.js and npm installed
- [ ] Backend API running on port 8000
- [ ] Dependencies installed (`npm install`)
- [ ] Development server started (`npm start`)
- [ ] Browser showing the dashboard
- [ ] Can create a new ticket
- [ ] Can see results and analysis

## 🎉 You're Ready!

Your React frontend is now running and connected to the backend API. Start creating tickets!
