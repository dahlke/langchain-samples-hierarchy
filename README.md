# GitHub Organization Hierarchy Builder

A tool that creates a beautiful static site visualizing your GitHub organization's repositories, organized by topics (tags). Perfect for exploring large organizations and discovering how projects are categorized.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)

## ✨ Features

- **Topic-based hierarchy**: Browse repositories grouped by GitHub topics
- **Language filtering**: Filter repositories by programming language
- **Search**: Quick search across repository names, descriptions, and topics
- **Beautiful UI**: Dark theme with smooth animations and responsive design
- **Automated updates**: GitHub Actions workflow rebuilds on schedule or repo changes
- **Zero dependencies frontend**: Pure HTML/CSS/JS - no build step required

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- A GitHub personal access token (optional but recommended for higher rate limits)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/dahlke/langchain-samples-hierarchy-builder.git
   cd langchain-samples-hierarchy-builder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up GitHub token** (optional but recommended)
   ```bash
   export GITHUB_TOKEN=your_github_token
   ```

4. **Run the build script**
   ```bash
   python build.py --org langchain-samples
   ```

5. **View the site**
   Open `docs/index.html` in your browser

### Command Line Options

```bash
python build.py --help

Options:
  --org TEXT            GitHub organization name (required)
  --output-dir TEXT     Output directory for static site (default: docs)
  --data-dir TEXT       Directory for intermediate data (default: data)
  --include-forks       Include forked repositories
  --include-archived    Include archived repositories
  --skip-fetch          Skip fetching data (use existing repos.json)
```

## 🔄 Automated Updates with GitHub Actions

The project includes GitHub Actions workflows for automated updates:

### Automatic Triggers

1. **Scheduled**: Runs daily at midnight UTC
2. **Push to main**: Rebuilds on any push to main branch
3. **Manual**: Can be triggered manually from Actions tab

### Setting Up GitHub Pages

1. Go to your repository **Settings** > **Pages**
2. Under "Build and deployment", select **GitHub Actions** as the source
3. The workflow will automatically deploy to GitHub Pages

### Organization Webhook Integration

For real-time updates when repositories are created/modified in your org:

1. Create a GitHub App with repository webhook permissions
2. Install the app on your organization
3. Configure the app to send `repository_dispatch` events to this repo
4. The `org-webhook-listener.yml` workflow will trigger rebuilds

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       ├── build-and-deploy.yml    # Main CI/CD workflow
│       └── org-webhook-listener.yml # Webhook handler
├── src/
│   ├── __init__.py
│   ├── github_fetcher.py    # Fetches repo data from GitHub API
│   ├── hierarchy_builder.py # Builds topic hierarchy
│   └── site_generator.py    # Generates static HTML
├── data/                    # Generated data files (gitignored)
│   ├── repos.json
│   └── hierarchy.json
├── docs/                    # Generated static site
│   ├── index.html
│   └── data.json
├── build.py                 # Main build script
├── requirements.txt
└── README.md
```

## 🎨 Customization

### Styling

The site uses CSS custom properties (variables) for theming. To customize colors, edit the `:root` section in `src/site_generator.py`:

```css
:root {
    --bg-primary: #0d1117;
    --accent-cyan: #58a6ff;
    /* ... more variables */
}
```

### Data Sources

You can modify `github_fetcher.py` to:
- Add additional metadata fields
- Filter repositories differently
- Include private repositories (requires appropriate token permissions)

## 🔐 GitHub Token Permissions

For public organizations, no token is required but rate limits apply (60 requests/hour).

With a token, you get:
- 5,000 requests/hour
- Access to private repositories (if permitted)

Create a token at: https://github.com/settings/tokens

Required scopes:
- `public_repo` (for public repositories)
- `repo` (for private repositories)

## 📊 Example Output

The generated site includes:

- **Stats overview**: Total repos, topics, languages, stars
- **Topic sidebar**: Clickable topic list with counts
- **Repository cards**: Name, description, language, stars, and topic tags
- **Search**: Real-time filtering across all fields
- **View toggles**: Switch between topic view, language view, or all repos

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use this for your own organizations!

## 🙏 Acknowledgments

Built for exploring the [LangChain Samples](https://github.com/langchain-samples) organization and other large GitHub organizations.

# langchain-samples-hierarchy
