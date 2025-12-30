# LangChain Samples - Repository Explorer

A beautiful static site that visualizes the [LangChain Samples](https://github.com/langchain-samples) GitHub organization's repositories, organized by topics.

Built with LangChain's brand styling and auto-deployed via GitHub Actions.

## ✨ Features

- **Topic-based hierarchy**: Browse repositories grouped by GitHub topics
- **Language filtering**: Filter repositories by programming language
- **Real-time search**: Quick search across names, descriptions, and topics
- **LangChain styling**: Dark theme matching [langchain.com](https://www.langchain.com)
- **Automated updates**: GitHub Actions rebuilds daily and on repo changes
- **Zero dependencies frontend**: Pure HTML/CSS/JS - no build step required

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- GitHub token (optional, for higher rate limits)

### Local Development

```bash
# Clone and install
git clone https://github.com/dahlke/langchain-samples-hierarchy-builder.git
cd langchain-samples-hierarchy-builder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Optional: set token for higher rate limits
export GITHUB_TOKEN=your_github_token

# Build the site
python build.py --org langchain-samples

# View
open docs/index.html
```

### Command Line Options

```bash
python build.py --help

Options:
  --org TEXT            GitHub organization name (required)
  --output-dir TEXT     Output directory (default: docs)
  --data-dir TEXT       Data directory (default: data)
  --include-forks       Include forked repositories
  --include-archived    Include archived repositories
  --skip-fetch          Use existing data
```

## 🔄 GitHub Actions

The included workflow automatically:

1. **Daily rebuild** at midnight UTC
2. **Rebuild on push** to main branch
3. **Manual trigger** from Actions tab
4. **Deploy to GitHub Pages**

### Setup GitHub Pages

1. Go to **Settings → Pages**
2. Select **GitHub Actions** as the source
3. Done! Site deploys to `https://your-username.github.io/repo-name/`

## 📁 Project Structure

```
├── src/
│   ├── github_fetcher.py    # GitHub API client
│   ├── hierarchy_builder.py # Topic hierarchy builder
│   └── site_generator.py    # Static site generator
├── .github/workflows/
│   └── build-and-deploy.yml # CI/CD pipeline
├── docs/                    # Generated site
├── data/                    # Generated data
├── build.py                 # Build script
└── requirements.txt
```

## 🎨 Styling

The site uses LangChain's brand colors:
- **Teal**: `#1DB8A4`
- **Purple**: `#7C3AED`
- **Pink**: `#EC4899`
- **Background**: `#0D0D0D`

## 📝 License

MIT License

---

Built for exploring [LangChain Samples](https://github.com/langchain-samples) · [LangChain](https://www.langchain.com)

