# GitHub Deployment & Troubleshooting Guide

This guide will walk you through pushing your project to GitHub professionally. This is essential for building a portfolio that recruiters and senior engineers will appreciate.

---

## 🚀 Step-by-Step GitHub Upload Process

### 1. Initialize the Local Git Repository
Git tracks the changes in your files. Before sending code to GitHub, your folder needs to be a local Git repository.
```powershell
# Ensure you are inside the project folder
cd d:\projects\flask-auth-notes

# Initialize the repository
git init
```
*What it does: Creates a hidden `.git` folder that tracks all history and changes.*

### 2. Verify your `.gitignore`
We have already created a `.gitignore` file for you. This is **critical**. 
If you upload your `.env` file, your database passwords and secret keys will be exposed to the public internet (which is a massive security failure in the industry). Our `.gitignore` file contains `.env`, `venv/`, and `__pycache__/` to explicitly block Git from ever uploading them.

### 3. Stage Your Files
You need to tell Git which files you want to include in this snapshot.
```powershell
git add .
```
*What it does: The `.` means "add everything in this directory" (except the files blocked by `.gitignore`).*

### 4. Create a Meaningful Commit
A commit is a saved snapshot of your code.
```powershell
git commit -m "Initial commit: Production-ready Flask Auth + Notes API"
```
*What it does: Wraps up the staged files into a package with a descriptive label. Recruiters look at commit messages to gauge professionalism.*

### 5. Create a GitHub Repository
1. Go to [GitHub.com](https://github.com) and log in.
2. Click the **+** icon in the top right and select **New repository**.
3. Name it `flask-auth-notes` (or similar).
4. **Leave "Add a README file" UNCHECKED** (we already created a great one!).
5. **Leave "Add .gitignore" UNCHECKED** (we already have one).
6. Click **Create repository**.

### 6. Connect Local Repo to GitHub
On the next page, GitHub will show you some commands. You want to copy the ones under *"…or push an existing repository from the command line"*.

```powershell
# Connects your local folder to the remote GitHub server URL
git remote add origin https://github.com/YOUR_USERNAME/flask-auth-notes.git

# Ensures you are on the 'main' branch (standard modern practice)
git branch -M main

# Uploads the code
git push -u origin main
```
*What it does: `origin` is just a nickname for your GitHub URL. `push -u` uploads the code and links your local `main` branch to the GitHub `main` branch permanently.*

---

## 💡 Best Practices for your Portfolio

1. **Keep Secrets Secret:** Never commit database credentials, AWS keys, or JWT Secrets. The `.env` template in our README tells people what to create themselves.
2. **Clear Instructions:** We wrote a detailed `README.md`. Recruiters almost never actually run code; they read the `README.md` to see if you understand system design, testing, and deployment.
3. **Commit often:** In the future, instead of doing one massive commit, do small ones: `git commit -m "Add note search functionality"`.

---

## ⚠️ Common Git & GitHub Errors

### Error 1: "Authentication failed" or "Support for password authentication was removed"
GitHub no longer allows you to type your account password in the terminal.
**The Fix:** You need a Personal Access Token (PAT).
1. Go to GitHub -> Settings -> Developer Settings -> Personal Access Tokens -> Tokens (classic).
2. Generate a new token (check the `repo` scope).
3. Copy the token. When the terminal asks for a password, paste the token instead.

### Error 2: "fatal: remote origin already exists."
You accidentally ran `git remote add origin ...` twice, or linked it to an old repo.
**The Fix:** 
```powershell
# Remove the old link
git remote remove origin

# Add the correct link
git remote add origin https://github.com/YOUR_USERNAME/flask-auth-notes.git
```

### Error 3: "Updates were rejected because the remote contains work that you do not have locally" (Non-fast-forward push)
This happens if you initialized the GitHub repo with a `README` or `.gitignore` online, and now your local code and GitHub code have different histories.
**The Fix (Safe):**
```powershell
# Pull the GitHub changes to your computer first
git pull origin main --rebase

# Then push again
git push origin main
```
**The Fix (Force - ONLY if you don't care about what's currently on GitHub):**
```powershell
git push -f origin main
```

### How to update your repository later (The Standard Flow)
Whenever you make a change to the code later and want to update GitHub, run these three commands:
```powershell
git add .
git commit -m "Added a new feature or fixed a bug"
git push
```
