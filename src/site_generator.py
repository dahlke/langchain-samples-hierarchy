"""
Generate a static HTML site for the repository hierarchy visualization.
"""

import json
import os
from datetime import datetime, timezone
from string import Template


class SiteGenerator:
    """Generates static HTML pages from hierarchy data."""

    def __init__(self, hierarchy_path: str, org_name: str):
        """
        Initialize the site generator.

        Args:
            hierarchy_path: Path to the hierarchy JSON file
            org_name: GitHub organization name
        """
        with open(hierarchy_path, "r") as f:
            self.hierarchy = json.load(f)
        self.org_name = org_name

    def generate(self, output_dir: str) -> None:
        """Generate the static site files."""
        os.makedirs(output_dir, exist_ok=True)

        # Generate main HTML file
        html_content = self._generate_html()

        with open(os.path.join(output_dir, "index.html"), "w") as f:
            f.write(html_content)

        # Copy data file for JavaScript access
        with open(os.path.join(output_dir, "data.json"), "w") as f:
            json.dump(self.hierarchy, f)

        print(f"Generated site in {output_dir}/")

    def _generate_html(self) -> str:
        """Generate the main HTML page."""
        stats = self.hierarchy.get("stats", {})
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.org_name} - Repository Hierarchy</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --bg-hover: #30363d;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --text-muted: #6e7681;
            --border-default: #30363d;
            --accent-cyan: #58a6ff;
            --accent-green: #3fb950;
            --accent-purple: #a371f7;
            --accent-orange: #f0883e;
            --accent-pink: #f778ba;
            --accent-yellow: #d29922;
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.4);
            --radius-sm: 6px;
            --radius-md: 8px;
            --radius-lg: 12px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
        }}

        /* Animated gradient background */
        .bg-pattern {{
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse at 20% 20%, rgba(88, 166, 255, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(163, 113, 247, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(63, 185, 80, 0.04) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }}

        /* Header */
        header {{
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
        }}

        .org-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-default);
            padding: 0.5rem 1rem;
            border-radius: 50px;
            margin-bottom: 1.5rem;
            font-size: 0.875rem;
            color: var(--text-secondary);
        }}

        .org-badge svg {{
            width: 20px;
            height: 20px;
            fill: var(--text-secondary);
        }}

        h1 {{
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.75rem;
            letter-spacing: -0.02em;
        }}

        .subtitle {{
            color: var(--text-secondary);
            font-size: 1.125rem;
            font-weight: 400;
        }}

        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            margin-bottom: 2.5rem;
        }}

        .stat-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-default);
            border-radius: var(--radius-lg);
            padding: 1.25rem;
            text-align: center;
            transition: transform 0.2s, border-color 0.2s;
        }}

        .stat-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-cyan);
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent-cyan);
        }}

        .stat-label {{
            font-size: 0.8rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.25rem;
        }}

        /* Search & Filter */
        .controls {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}

        .search-box {{
            flex: 1;
            min-width: 280px;
            position: relative;
        }}

        .search-box input {{
            width: 100%;
            padding: 0.875rem 1rem 0.875rem 2.75rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-default);
            border-radius: var(--radius-md);
            color: var(--text-primary);
            font-size: 0.95rem;
            font-family: inherit;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
        }}

        .search-box input::placeholder {{
            color: var(--text-muted);
        }}

        .search-box svg {{
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            width: 18px;
            height: 18px;
            stroke: var(--text-muted);
        }}

        .view-toggles {{
            display: flex;
            gap: 0.5rem;
        }}

        .view-btn {{
            padding: 0.75rem 1.25rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-default);
            border-radius: var(--radius-md);
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-family: inherit;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .view-btn:hover {{
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }}

        .view-btn.active {{
            background: var(--accent-cyan);
            border-color: var(--accent-cyan);
            color: var(--bg-primary);
        }}

        /* Main Content Area */
        .content-area {{
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 1.5rem;
        }}

        @media (max-width: 900px) {{
            .content-area {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Topics Sidebar */
        .topics-sidebar {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-default);
            border-radius: var(--radius-lg);
            padding: 1.25rem;
            height: fit-content;
            position: sticky;
            top: 1rem;
        }}

        .sidebar-title {{
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-default);
        }}

        .topic-list {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .topic-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.625rem 0.875rem;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: background 0.15s;
        }}

        .topic-item:hover {{
            background: var(--bg-hover);
        }}

        .topic-item.active {{
            background: rgba(88, 166, 255, 0.15);
        }}

        .topic-item.active .topic-name {{
            color: var(--accent-cyan);
        }}

        .topic-name {{
            font-size: 0.9rem;
            color: var(--text-primary);
            font-weight: 500;
        }}

        .topic-count {{
            font-size: 0.8rem;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-muted);
            background: var(--bg-tertiary);
            padding: 0.125rem 0.5rem;
            border-radius: 50px;
        }}

        /* Repository Grid */
        .repos-container {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-default);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
        }}

        .repos-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-default);
        }}

        .repos-title {{
            font-size: 1.125rem;
            font-weight: 600;
        }}

        .repos-count {{
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}

        .repos-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
        }}

        .repo-card {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-default);
            border-radius: var(--radius-md);
            padding: 1.25rem;
            transition: all 0.2s;
            cursor: pointer;
            text-decoration: none;
            display: block;
        }}

        .repo-card:hover {{
            border-color: var(--accent-cyan);
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}

        .repo-name {{
            font-size: 1rem;
            font-weight: 600;
            color: var(--accent-cyan);
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .repo-name svg {{
            width: 16px;
            height: 16px;
            opacity: 0.7;
        }}

        .repo-description {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .repo-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            font-size: 0.8rem;
            color: var(--text-muted);
        }}

        .repo-meta-item {{
            display: flex;
            align-items: center;
            gap: 0.375rem;
        }}

        .repo-meta-item svg {{
            width: 14px;
            height: 14px;
        }}

        .repo-topics {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.375rem;
            margin-top: 0.75rem;
        }}

        .repo-topic {{
            font-size: 0.7rem;
            padding: 0.25rem 0.5rem;
            background: rgba(88, 166, 255, 0.1);
            color: var(--accent-cyan);
            border-radius: 50px;
            font-weight: 500;
        }}

        /* Language Badge Colors */
        .lang-python {{ color: var(--accent-yellow); }}
        .lang-javascript {{ color: var(--accent-yellow); }}
        .lang-typescript {{ color: var(--accent-cyan); }}
        .lang-html {{ color: var(--accent-orange); }}
        .lang-jupyter {{ color: var(--accent-orange); }}

        /* Empty State */
        .empty-state {{
            text-align: center;
            padding: 3rem 1rem;
            color: var(--text-muted);
        }}

        .empty-state svg {{
            width: 48px;
            height: 48px;
            margin-bottom: 1rem;
            opacity: 0.5;
        }}

        /* Footer */
        footer {{
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            border-top: 1px solid var(--border-default);
            color: var(--text-muted);
            font-size: 0.875rem;
        }}

        footer a {{
            color: var(--accent-cyan);
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .repo-card {{
            animation: fadeIn 0.3s ease-out;
            animation-fill-mode: backwards;
        }}

        .repo-card:nth-child(1) {{ animation-delay: 0.02s; }}
        .repo-card:nth-child(2) {{ animation-delay: 0.04s; }}
        .repo-card:nth-child(3) {{ animation-delay: 0.06s; }}
        .repo-card:nth-child(4) {{ animation-delay: 0.08s; }}
        .repo-card:nth-child(5) {{ animation-delay: 0.1s; }}
        .repo-card:nth-child(6) {{ animation-delay: 0.12s; }}
    </style>
</head>
<body>
    <div class="bg-pattern"></div>

    <div class="container">
        <header>
            <div class="org-badge">
                <svg viewBox="0 0 16 16"><path d="M1.75 16A1.75 1.75 0 0 1 0 14.25V1.75C0 .784.784 0 1.75 0h8.5C11.216 0 12 .784 12 1.75v12.5c0 .085-.006.168-.018.25h2.268a.25.25 0 0 0 .25-.25V8.285a.25.25 0 0 0-.111-.208l-1.055-.703a.749.749 0 1 1 .832-1.248l1.055.703c.487.325.779.871.779 1.456v5.965A1.75 1.75 0 0 1 14.25 16h-3.5a.766.766 0 0 1-.197-.026c-.099.017-.2.026-.303.026h-3a.75.75 0 0 1-.75-.75V14h-1v1.25a.75.75 0 0 1-.75.75Zm-.25-1.75c0 .138.112.25.25.25H4v-1.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 .75.75v1.25h2.25a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25ZM3.75 6h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5ZM3 3.75A.75.75 0 0 1 3.75 3h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 3.75Zm4 3A.75.75 0 0 1 7.75 6h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 7 6.75ZM7.75 3h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5ZM3 9.75A.75.75 0 0 1 3.75 9h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 9.75ZM7.75 9h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5Z"/></svg>
                <span>GitHub Organization</span>
            </div>
            <h1>{self.org_name}</h1>
            <p class="subtitle">Repository Hierarchy Explorer</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats.get('total_repositories', 0)}</div>
                <div class="stat-label">Repositories</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats.get('total_topics', 0)}</div>
                <div class="stat-label">Topics</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats.get('total_languages', 0)}</div>
                <div class="stat-label">Languages</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats.get('total_stars', 0)}</div>
                <div class="stat-label">Total Stars</div>
            </div>
        </div>

        <div class="controls">
            <div class="search-box">
                <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input type="text" id="search" placeholder="Search repositories...">
            </div>
            <div class="view-toggles">
                <button class="view-btn active" data-view="topics">By Topic</button>
                <button class="view-btn" data-view="language">By Language</button>
                <button class="view-btn" data-view="all">All Repos</button>
            </div>
        </div>

        <div class="content-area">
            <aside class="topics-sidebar">
                <div class="sidebar-title">Topics</div>
                <div class="topic-list" id="topic-list">
                    <!-- Populated by JavaScript -->
                </div>
            </aside>

            <main class="repos-container">
                <div class="repos-header">
                    <div class="repos-title" id="repos-title">All Repositories</div>
                    <div class="repos-count" id="repos-count"></div>
                </div>
                <div class="repos-grid" id="repos-grid">
                    <!-- Populated by JavaScript -->
                </div>
            </main>
        </div>

        <footer>
            <p>Generated on {generated_at}</p>
            <p>
                <a href="https://github.com/{self.org_name}" target="_blank">View on GitHub</a>
            </p>
        </footer>
    </div>

    <script>
        // Embedded data
        const hierarchyData = {json.dumps(self.hierarchy)};

        // State
        let currentView = 'topics';
        let currentTopic = null;
        let searchQuery = '';

        // DOM Elements
        const topicList = document.getElementById('topic-list');
        const reposGrid = document.getElementById('repos-grid');
        const reposTitle = document.getElementById('repos-title');
        const reposCount = document.getElementById('repos-count');
        const searchInput = document.getElementById('search');
        const viewButtons = document.querySelectorAll('.view-btn');

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            renderTopics();
            renderRepositories();
            setupEventListeners();
        }});

        function setupEventListeners() {{
            // Search
            searchInput.addEventListener('input', (e) => {{
                searchQuery = e.target.value.toLowerCase();
                renderRepositories();
            }});

            // View toggles
            viewButtons.forEach(btn => {{
                btn.addEventListener('click', () => {{
                    viewButtons.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentView = btn.dataset.view;
                    currentTopic = null;
                    renderSidebar();
                    renderRepositories();
                }});
            }});

            // Topic selection
            topicList.addEventListener('click', (e) => {{
                const topicItem = e.target.closest('.topic-item');
                if (topicItem) {{
                    const topic = topicItem.dataset.topic;
                    currentTopic = currentTopic === topic ? null : topic;
                    renderTopics();
                    renderRepositories();
                }}
            }});
        }}

        function renderSidebar() {{
            if (currentView === 'language') {{
                document.querySelector('.sidebar-title').textContent = 'Languages';
                renderLanguages();
            }} else {{
                document.querySelector('.sidebar-title').textContent = 'Topics';
                renderTopics();
            }}
        }}

        function renderTopics() {{
            const topics = hierarchyData.topics || {{}};
            const sortedTopics = Object.entries(topics)
                .sort((a, b) => b[1].count - a[1].count);

            topicList.innerHTML = sortedTopics.map(([name, data]) => `
                <div class="topic-item ${{currentTopic === name ? 'active' : ''}}" data-topic="${{name}}">
                    <span class="topic-name">${{name}}</span>
                    <span class="topic-count">${{data.count}}</span>
                </div>
            `).join('');
        }}

        function renderLanguages() {{
            const languages = hierarchyData.languages || {{}};
            const sortedLanguages = Object.entries(languages)
                .sort((a, b) => b[1].length - a[1].length);

            topicList.innerHTML = sortedLanguages.map(([name, repos]) => `
                <div class="topic-item ${{currentTopic === name ? 'active' : ''}}" data-topic="${{name}}">
                    <span class="topic-name">${{name}}</span>
                    <span class="topic-count">${{repos.length}}</span>
                </div>
            `).join('');
        }}

        function getFilteredRepos() {{
            let repos = hierarchyData.all_repositories || [];

            // Filter by current selection
            if (currentTopic) {{
                if (currentView === 'language') {{
                    repos = hierarchyData.languages[currentTopic] || [];
                }} else {{
                    repos = (hierarchyData.topics[currentTopic]?.repositories) || [];
                }}
            }}

            // Filter by search
            if (searchQuery) {{
                repos = repos.filter(repo =>
                    repo.name.toLowerCase().includes(searchQuery) ||
                    (repo.description || '').toLowerCase().includes(searchQuery) ||
                    (repo.topics || []).some(t => t.toLowerCase().includes(searchQuery))
                );
            }}

            return repos;
        }}

        function renderRepositories() {{
            const repos = getFilteredRepos();

            // Update header
            if (currentTopic) {{
                reposTitle.textContent = currentTopic;
            }} else if (currentView === 'language') {{
                reposTitle.textContent = 'All Repositories';
            }} else if (currentView === 'all') {{
                reposTitle.textContent = 'All Repositories';
            }} else {{
                reposTitle.textContent = 'All Repositories';
            }}

            reposCount.textContent = `${{repos.length}} ${{repos.length === 1 ? 'repository' : 'repositories'}}`;

            if (repos.length === 0) {{
                reposGrid.innerHTML = `
                    <div class="empty-state" style="grid-column: 1 / -1;">
                        <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
                        </svg>
                        <p>No repositories found</p>
                    </div>
                `;
                return;
            }}

            reposGrid.innerHTML = repos.map(repo => `
                <a href="${{repo.url}}" target="_blank" class="repo-card">
                    <div class="repo-name">
                        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                        </svg>
                        ${{repo.name}}
                    </div>
                    <div class="repo-description">${{repo.description || 'No description'}}</div>
                    <div class="repo-meta">
                        ${{repo.language ? `
                            <span class="repo-meta-item lang-${{repo.language?.toLowerCase().replace(' ', '-')}}">
                                <svg viewBox="0 0 16 16" fill="currentColor"><circle cx="8" cy="8" r="4"/></svg>
                                ${{repo.language}}
                            </span>
                        ` : ''}}
                        ${{repo.stars > 0 ? `
                            <span class="repo-meta-item">
                                <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                                </svg>
                                ${{repo.stars}}
                            </span>
                        ` : ''}}
                    </div>
                    ${{(repo.topics || []).length > 0 ? `
                        <div class="repo-topics">
                            ${{repo.topics.slice(0, 4).map(t => `<span class="repo-topic">${{t}}</span>`).join('')}}
                            ${{repo.topics.length > 4 ? `<span class="repo-topic">+${{repo.topics.length - 4}}</span>` : ''}}
                        </div>
                    ` : ''}}
                </a>
            `).join('');
        }}
    </script>
</body>
</html>'''


def main():
    """Main entry point for generating the static site."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate static site for hierarchy visualization")
    parser.add_argument("--input", default="data/hierarchy.json", help="Input hierarchy JSON file")
    parser.add_argument("--output", default="docs", help="Output directory for static site")
    parser.add_argument("--org", required=True, help="GitHub organization name")

    args = parser.parse_args()

    generator = SiteGenerator(args.input, args.org)
    generator.generate(args.output)


if __name__ == "__main__":
    main()

