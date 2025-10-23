# Deploying to GitHub Pages

This guide explains how to deploy your video index as a static site on GitHub Pages.

## Prerequisites

- A GitHub account
- Git installed on your computer
- Your video transcripts in the `transcripts/` folder

## Step 1: Build the Static Site

Run the build script to bundle all transcripts into a single JSON file:

```bash
python build_static.py
```

This will:
- Read all transcript JSON files from `transcripts/`
- Combine them into `transcripts.json` in the root directory
- Display the bundle size and transcript count

## Step 2: Commit and Push to GitHub

If you haven't already, initialize a git repository and push to GitHub:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Add static video index site"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top right)
3. Scroll down to **Pages** section (left sidebar)
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
5. Click **Save**

GitHub will build and deploy your site. It may take a few minutes.

## Step 4: Access Your Site

Your site will be available at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/
```

## Updating the Site

Whenever you add new transcripts:

1. Run `python build_static.py` to rebuild the bundle
2. Commit and push the changes:
   ```bash
   git add transcripts.json
   git commit -m "Update transcripts"
   git push
   ```

GitHub Pages will automatically redeploy your site.

## Notes

- **Bundle Size**: The `transcripts.json` file contains all your transcripts. If it becomes very large (>10MB), consider:
  - Splitting into multiple files
  - Using compression
  - Implementing lazy loading
  
- **Video Metadata**: The static site uses YouTube's oEmbed API to fetch video titles and channel names. This doesn't require an API key but provides limited information (no upload dates).

- **Search Performance**: All transcripts are loaded into the browser, so search is instant. However, very large collections may slow down initial page load.

## Troubleshooting

**Site not loading?**
- Make sure `docs/transcripts.json` exists
- Check that GitHub Pages is enabled in repository settings
- Wait a few minutes for GitHub to deploy

**Search not working?**
- Open browser console (F12) to check for errors
- Verify transcripts.json is accessible at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/transcripts.json`

**Videos not playing?**
- Ensure video IDs in transcripts are correct
- Some videos may have embedding disabled by the uploader
