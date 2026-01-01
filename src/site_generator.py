"""
Generate a static HTML site for the repository hierarchy visualization.
Styled to match LangChain's brand guidelines.
"""

import json
import os
from datetime import datetime, timezone


class SiteGenerator:
    """Generates static HTML pages from hierarchy data."""

    # LangChain logo from Wikimedia Commons
    LANGCHAIN_LOGO_URL = 'https://upload.wikimedia.org/wikipedia/commons/6/60/LangChain_Logo.svg'

    def __init__(self, hierarchy_path: str, org_name: str):
        with open(hierarchy_path, "r") as f:
            self.hierarchy = json.load(f)
        self.org_name = org_name

    def generate(self, output_dir: str) -> None:
        """Generate the static site files."""
        os.makedirs(output_dir, exist_ok=True)

        html_content = self._generate_html()

        with open(os.path.join(output_dir, "index.html"), "w") as f:
            f.write(html_content)

        with open(os.path.join(output_dir, "data.json"), "w") as f:
            json.dump(self.hierarchy, f)

        print(f"Generated site in {output_dir}/")

    def _generate_html(self) -> str:
        """Generate the main HTML page with LangChain styling."""
        stats = self.hierarchy.get("stats", {})
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.org_name} - Repository Explorer</title>
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        /* Dark Theme (default) */
        :root {{
            --lc-bg-primary: #09090B;
            --lc-bg-secondary: #0F0F11;
            --lc-bg-tertiary: #18181B;
            --lc-bg-card: #18181B;
            --lc-bg-hover: #27272A;
            --lc-bg-input: #18181B;

            --lc-text-primary: #FAFAFA;
            --lc-text-secondary: #A1A1AA;
            --lc-text-muted: #71717A;

            --lc-border: #27272A;
            --lc-border-hover: #3F3F46;

            /* LangChain Accent Colors */
            --lc-teal: #1DB8A4;
            --lc-teal-hover: #0D9488;
            --lc-teal-muted: rgba(29, 184, 164, 0.12);
            --lc-purple: #8B5CF6;
            --lc-purple-muted: rgba(139, 92, 246, 0.12);
            --lc-gradient: linear-gradient(135deg, #1DB8A4 0%, #8B5CF6 100%);
            --lc-gradient-text: linear-gradient(90deg, #1DB8A4 0%, #8B5CF6 50%, #EC4899 100%);

            /* Mesh Background */
            --mesh-teal: rgba(29, 184, 164, 0.12);
            --mesh-purple: rgba(139, 92, 246, 0.10);
            --mesh-pink: rgba(236, 72, 153, 0.06);

            /* Utilities */
            --radius-sm: 6px;
            --radius-md: 8px;
            --radius-lg: 12px;
            --radius-xl: 16px;
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.4);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.5);
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.6);
        }}

        /* Light Theme */
        [data-theme="light"] {{
            --lc-bg-primary: #FFFFFF;
            --lc-bg-secondary: #FAFAFA;
            --lc-bg-tertiary: #F4F4F5;
            --lc-bg-card: #FFFFFF;
            --lc-bg-hover: #F4F4F5;
            --lc-bg-input: #FFFFFF;

            --lc-text-primary: #18181B;
            --lc-text-secondary: #52525B;
            --lc-text-muted: #71717A;

            --lc-border: #E4E4E7;
            --lc-border-hover: #D4D4D8;

            --lc-teal: #0D9488;
            --lc-teal-hover: #0F766E;
            --lc-teal-muted: rgba(13, 148, 136, 0.1);
            --lc-purple: #7C3AED;
            --lc-purple-muted: rgba(124, 58, 237, 0.1);

            --mesh-teal: rgba(13, 148, 136, 0.06);
            --mesh-purple: rgba(124, 58, 237, 0.05);
            --mesh-pink: rgba(236, 72, 153, 0.03);

            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--lc-bg-primary);
            color: var(--lc-text-primary);
            min-height: 100vh;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        /* Smooth transitions for theme changes */
        *, *::before, *::after {{
            transition: background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }}

        /* Animated gradient mesh background */
        .bg-mesh {{
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse 80% 50% at 20% -20%, var(--mesh-teal) 0%, transparent 50%),
                radial-gradient(ellipse 60% 40% at 80% 0%, var(--mesh-purple) 0%, transparent 50%),
                radial-gradient(ellipse 50% 30% at 50% 100%, var(--mesh-pink) 0%, transparent 40%);
            pointer-events: none;
            z-index: 0;
            transition: background 0.3s ease;
        }}

        /* Theme Toggle */
        .theme-toggle {{
            position: fixed;
            top: 1.5rem;
            right: 1.5rem;
            z-index: 100;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: var(--lc-bg-card);
            border: 1px solid var(--lc-border);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-md);
        }}

        .theme-toggle:hover {{
            border-color: var(--lc-teal);
            transform: scale(1.05);
        }}

        .theme-toggle svg {{
            width: 20px;
            height: 20px;
            color: var(--lc-text-secondary);
            transition: color 0.2s;
        }}

        .theme-toggle:hover svg {{
            color: var(--lc-teal);
        }}

        .theme-toggle .sun-icon {{
            display: none;
        }}

        .theme-toggle .moon-icon {{
            display: block;
        }}

        [data-theme="light"] .theme-toggle .sun-icon {{
            display: block;
        }}

        [data-theme="light"] .theme-toggle .moon-icon {{
            display: none;
        }}

        .container {{
            max-width: 1440px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }}

        /* Header with LangChain logo */
        header {{
            text-align: center;
            margin-bottom: 2rem;
            padding: 2rem 0 1rem;
        }}

        .logo-container {{
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }}

        .logo-icon {{
            height: 48px;
            width: auto;
        }}

        /* Invert logo colors for dark mode (logo is dark by default) */
        :root .logo-icon {{
            filter: brightness(0) invert(1);
        }}

        [data-theme="light"] .logo-icon {{
            filter: none;
        }}

        .logo-text {{
            font-family: 'Manrope', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--lc-text-primary);
            letter-spacing: -0.02em;
        }}

        .logo-text span {{
            background: var(--lc-gradient-text);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        h1 {{
            font-family: 'Manrope', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 1rem;
            background: var(--lc-gradient-text);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .subtitle {{
            color: var(--lc-text-secondary);
            font-size: 1.25rem;
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto;
        }}

        /* Product Panels - Main navigation cards */
        .product-panels {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}

        @media (max-width: 900px) {{
            .product-panels {{
                grid-template-columns: 1fr;
                gap: 1rem;
            }}
        }}

        .product-panel {{
            background: var(--lc-bg-card);
            border: 1px solid var(--lc-border);
            border-radius: var(--radius-xl);
            padding: 1.75rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }}

        .product-panel::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            border-radius: var(--radius-xl) var(--radius-xl) 0 0;
        }}

        .product-panel:hover {{
            transform: translateY(-6px) scale(1.02);
            box-shadow: var(--shadow-lg);
        }}

        .product-panel.active {{
            transform: scale(1.02);
        }}

        /* LangChain Panel - Green flowing gradient */
        .product-panel.langchain {{
            background:
                linear-gradient(135deg, rgba(34, 197, 94, 0.9) 0%, rgba(16, 185, 129, 0.85) 50%, rgba(5, 150, 105, 0.9) 100%),
                radial-gradient(ellipse at 20% 80%, rgba(52, 211, 153, 0.4) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(34, 197, 94, 0.3) 0%, transparent 40%),
                radial-gradient(ellipse at 40% 40%, rgba(16, 185, 129, 0.5) 0%, transparent 60%);
            background-color: #059669;
            border-color: rgba(34, 197, 94, 0.3);
        }}
        .product-panel.langchain::before {{
            background: linear-gradient(90deg, #22C55E 0%, #10B981 50%, #059669 100%);
            opacity: 1;
        }}
        .product-panel.langchain::after {{
            content: '';
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 30% 70%, rgba(255,255,255,0.1) 0%, transparent 40%),
                radial-gradient(circle at 70% 30%, rgba(255,255,255,0.08) 0%, transparent 30%);
            pointer-events: none;
            border-radius: inherit;
        }}
        .product-panel.langchain.active {{
            box-shadow: 0 0 30px rgba(34, 197, 94, 0.4);
        }}
        .product-panel.langchain .product-icon {{
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            backdrop-filter: blur(10px);
        }}
        .product-panel.langchain .product-count {{
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            backdrop-filter: blur(10px);
        }}
        .product-panel.langchain .product-title,
        .product-panel.langchain .product-description {{
            color: #fff;
        }}
        .product-panel.langchain .product-description {{
            color: rgba(255, 255, 255, 0.85);
        }}
        .product-panel.langchain .product-arrow {{
            color: rgba(255, 255, 255, 0.7);
        }}
        .product-panel.langchain:hover .product-arrow {{
            color: #fff;
        }}

        /* LangGraph Panel - Blue/Purple flowing gradient */
        .product-panel.langgraph {{
            background:
                linear-gradient(135deg, rgba(99, 102, 241, 0.9) 0%, rgba(79, 70, 229, 0.85) 40%, rgba(139, 92, 246, 0.9) 100%),
                radial-gradient(ellipse at 80% 80%, rgba(167, 139, 250, 0.4) 0%, transparent 50%),
                radial-gradient(ellipse at 20% 20%, rgba(99, 102, 241, 0.3) 0%, transparent 40%),
                radial-gradient(ellipse at 60% 50%, rgba(139, 92, 246, 0.5) 0%, transparent 60%);
            background-color: #4F46E5;
            border-color: rgba(99, 102, 241, 0.3);
        }}
        .product-panel.langgraph::before {{
            background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 50%, #A78BFA 100%);
            opacity: 1;
        }}
        .product-panel.langgraph::after {{
            content: '';
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 70% 80%, rgba(255,255,255,0.1) 0%, transparent 40%),
                radial-gradient(circle at 30% 20%, rgba(255,255,255,0.08) 0%, transparent 30%);
            pointer-events: none;
            border-radius: inherit;
        }}
        .product-panel.langgraph.active {{
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.4);
        }}
        .product-panel.langgraph .product-icon {{
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            backdrop-filter: blur(10px);
        }}
        .product-panel.langgraph .product-count {{
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            backdrop-filter: blur(10px);
        }}
        .product-panel.langgraph .product-title,
        .product-panel.langgraph .product-description {{
            color: #fff;
        }}
        .product-panel.langgraph .product-description {{
            color: rgba(255, 255, 255, 0.85);
        }}
        .product-panel.langgraph .product-arrow {{
            color: rgba(255, 255, 255, 0.7);
        }}
        .product-panel.langgraph:hover .product-arrow {{
            color: #fff;
        }}

        /* LangSmith Panel - Orange/Amber flowing gradient */
        .product-panel.langsmith {{
            background:
                linear-gradient(135deg, rgba(251, 146, 60, 0.9) 0%, rgba(245, 158, 11, 0.85) 40%, rgba(234, 88, 12, 0.9) 100%),
                radial-gradient(ellipse at 20% 80%, rgba(253, 186, 116, 0.4) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(251, 146, 60, 0.3) 0%, transparent 40%),
                radial-gradient(ellipse at 50% 60%, rgba(245, 158, 11, 0.5) 0%, transparent 60%);
            background-color: #F59E0B;
            border-color: rgba(245, 158, 11, 0.3);
        }}
        .product-panel.langsmith::before {{
            background: linear-gradient(90deg, #FB923C 0%, #F59E0B 50%, #EA580C 100%);
            opacity: 1;
        }}
        .product-panel.langsmith::after {{
            content: '';
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 20% 30%, rgba(255,255,255,0.1) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(255,255,255,0.08) 0%, transparent 30%);
            pointer-events: none;
            border-radius: inherit;
        }}
        .product-panel.langsmith.active {{
            box-shadow: 0 0 30px rgba(245, 158, 11, 0.4);
        }}
        .product-panel.langsmith .product-icon {{
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            backdrop-filter: blur(10px);
        }}
        .product-panel.langsmith .product-count {{
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            backdrop-filter: blur(10px);
        }}
        .product-panel.langsmith .product-title,
        .product-panel.langsmith .product-description {{
            color: #fff;
        }}
        .product-panel.langsmith .product-description {{
            color: rgba(255, 255, 255, 0.85);
        }}
        .product-panel.langsmith .product-arrow {{
            color: rgba(255, 255, 255, 0.7);
        }}
        .product-panel.langsmith:hover .product-arrow {{
            color: #fff;
        }}

        .product-panel-header {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.75rem;
        }}

        .product-icon {{
            width: 48px;
            height: 48px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .product-icon svg {{
            width: 26px;
            height: 26px;
        }}

        .product-title {{
            font-family: 'Manrope', sans-serif;
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--lc-text-primary);
        }}

        .product-description {{
            font-size: 0.9rem;
            color: var(--lc-text-secondary);
            line-height: 1.5;
            margin-bottom: 1rem;
        }}

        .product-footer {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .product-count {{
            font-size: 0.8rem;
            font-weight: 600;
            padding: 0.35rem 0.75rem;
            border-radius: 50px;
        }}

        .product-arrow {{
            width: 20px;
            height: 20px;
            color: var(--lc-text-muted);
            transition: transform 0.2s, color 0.2s;
        }}

        .product-panel:hover .product-arrow {{
            transform: translateX(4px);
            color: var(--lc-text-primary);
        }}

        /* Product panel animations */
        .product-panel {{
            animation: fadeInUp 0.5s ease-out;
            animation-fill-mode: backwards;
        }}

        .product-panel:nth-child(1) {{ animation-delay: 0.1s; }}
        .product-panel:nth-child(2) {{ animation-delay: 0.2s; }}
        .product-panel:nth-child(3) {{ animation-delay: 0.3s; }}

        /* Controls */
        .controls {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}

        .search-box {{
            flex: 1;
            min-width: 300px;
            position: relative;
        }}

        .search-box input {{
            width: 100%;
            padding: 0.875rem 1rem 0.875rem 3rem;
            background: var(--lc-bg-input);
            border: 1px solid var(--lc-border);
            border-radius: var(--radius-md);
            color: var(--lc-text-primary);
            font-size: 0.9375rem;
            font-family: inherit;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: var(--lc-teal);
            box-shadow: 0 0 0 3px var(--lc-teal-muted);
        }}

        .search-box input::placeholder {{
            color: var(--lc-text-muted);
        }}

        .search-box svg {{
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            width: 20px;
            height: 20px;
            stroke: var(--lc-text-muted);
        }}

        .view-toggles {{
            display: flex;
            gap: 0.5rem;
            background: var(--lc-bg-card);
            padding: 0.375rem;
            border-radius: var(--radius-md);
            border: 1px solid var(--lc-border);
        }}

        .view-btn {{
            padding: 0.625rem 1.25rem;
            background: transparent;
            border: none;
            border-radius: var(--radius-sm);
            color: var(--lc-text-secondary);
            font-size: 0.875rem;
            font-family: inherit;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .view-btn:hover {{
            color: var(--lc-text-primary);
            background: var(--lc-bg-hover);
        }}

        .view-btn.active {{
            background: var(--lc-teal);
            color: var(--lc-bg-primary);
            font-weight: 600;
        }}

        /* Main Content Layout */
        .content-area {{
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 2rem;
        }}

        @media (max-width: 900px) {{
            .content-area {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Sidebar */
        .topics-sidebar {{
            background: var(--lc-bg-card);
            border: 1px solid var(--lc-border);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            height: fit-content;
            position: sticky;
            top: 1rem;
            box-shadow: var(--shadow-sm);
        }}

        .sidebar-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--lc-border);
        }}

        .sidebar-title {{
            font-family: 'Manrope', sans-serif;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: var(--lc-text-muted);
        }}

        .clear-btn {{
            padding: 0.375rem 0.75rem;
            background: transparent;
            border: 1px solid var(--lc-border);
            border-radius: var(--radius-sm);
            color: var(--lc-text-muted);
            font-size: 0.7rem;
            font-family: inherit;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .clear-btn:hover {{
            border-color: var(--lc-teal);
            color: var(--lc-teal);
            background: var(--lc-teal-muted);
        }}

        .clear-btn.hidden {{
            display: none;
        }}

        .topic-list {{
            display: flex;
            flex-direction: column;
            gap: 0.375rem;
            max-height: 60vh;
            overflow-y: auto;
        }}

        .topic-list::-webkit-scrollbar {{
            width: 4px;
        }}

        .topic-list::-webkit-scrollbar-track {{
            background: transparent;
        }}

        .topic-list::-webkit-scrollbar-thumb {{
            background: var(--lc-border);
            border-radius: 2px;
        }}

        .topic-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem 1rem;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.15s;
        }}

        .topic-item:hover {{
            background: var(--lc-bg-hover);
        }}

        .topic-item.active {{
            background: var(--lc-teal-muted);
        }}

        .topic-item.active .topic-name {{
            color: var(--lc-teal);
            font-weight: 600;
        }}

        .topic-item.disabled {{
            opacity: 0.4;
            cursor: default;
        }}

        .topic-item.disabled:hover {{
            background: transparent;
        }}

        .topic-name {{
            font-size: 0.9rem;
            color: var(--lc-text-primary);
            font-weight: 500;
        }}

        .topic-count {{
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--lc-text-muted);
            background: var(--lc-bg-tertiary);
            padding: 0.25rem 0.625rem;
            border-radius: 50px;
            min-width: 28px;
            text-align: center;
        }}

        /* Topic Groups (Nested) */
        .topic-group {{
            margin-bottom: 0.75rem;
        }}

        .topic-group-header {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 0.75rem;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--lc-text-muted);
            cursor: pointer;
            border-radius: var(--radius-sm);
            transition: all 0.15s;
        }}

        .topic-group-header:hover {{
            background: var(--lc-bg-hover);
            color: var(--lc-text-secondary);
        }}

        .topic-group-header svg {{
            width: 12px;
            height: 12px;
            transition: transform 0.2s;
        }}

        .topic-group.collapsed .topic-group-header svg {{
            transform: rotate(-90deg);
        }}

        .topic-group-items {{
            padding-left: 0.5rem;
            border-left: 2px solid var(--lc-border);
            margin-left: 0.75rem;
        }}

        .topic-group.collapsed .topic-group-items {{
            display: none;
        }}

        /* Product Category Styles */
        .product-category .topic-group-header {{
            gap: 0.5rem;
        }}

        .category-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .category-icon svg {{
            width: 16px;
            height: 16px;
            color: var(--lc-teal);
        }}

        .subcategory-item {{
            flex-direction: column;
            align-items: flex-start !important;
            gap: 0.25rem;
        }}

        .subcategory-item .subcategory-info {{
            display: flex;
            flex-direction: column;
            gap: 0.125rem;
        }}

        .subcategory-item .subcategory-desc {{
            font-size: 0.7rem;
            color: var(--lc-text-muted);
            font-weight: 400;
        }}

        .subcategory-item .topic-count {{
            position: absolute;
            right: 1rem;
            top: 50%;
            transform: translateY(-50%);
        }}

        .subcategory-item {{
            position: relative;
        }}

        /* Difficulty Levels */
        .difficulty-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.875rem 1rem;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.15s;
            margin-bottom: 0.375rem;
        }}

        .difficulty-item:hover {{
            background: var(--lc-bg-hover);
        }}

        .difficulty-item.active {{
            background: var(--lc-teal-muted);
        }}

        .difficulty-item.active .difficulty-name {{
            color: var(--lc-teal);
            font-weight: 600;
        }}

        .difficulty-item.disabled {{
            opacity: 0.4;
            cursor: default;
        }}

        .difficulty-item.disabled:hover {{
            background: transparent;
        }}

        .difficulty-info {{
            display: flex;
            align-items: center;
            gap: 0.625rem;
        }}

        .difficulty-icon {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .difficulty-icon.beginner {{
            background: rgba(34, 197, 94, 0.15);
            color: #22C55E;
        }}

        .difficulty-icon.intermediate {{
            background: rgba(234, 179, 8, 0.15);
            color: #EAB308;
        }}

        .difficulty-icon.advanced {{
            background: rgba(239, 68, 68, 0.15);
            color: #EF4444;
        }}

        .difficulty-icon.expert {{
            background: rgba(139, 92, 246, 0.15);
            color: #8B5CF6;
        }}

        .difficulty-icon svg {{
            width: 12px;
            height: 12px;
        }}

        .difficulty-name {{
            font-size: 0.9rem;
            color: var(--lc-text-primary);
            font-weight: 500;
        }}

        .difficulty-desc {{
            font-size: 0.75rem;
            color: var(--lc-text-muted);
            margin-top: 0.125rem;
        }}

        /* Repository Grid */
        .repos-container {{
            background: var(--lc-bg-card);
            border: 1px solid var(--lc-border);
            border-radius: var(--radius-lg);
            padding: 1.75rem;
            box-shadow: var(--shadow-sm);
        }}

        .repos-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1.25rem;
            border-bottom: 1px solid var(--lc-border);
        }}

        .repos-title {{
            font-family: 'Manrope', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
        }}

        .repos-count {{
            color: var(--lc-text-secondary);
            font-size: 0.9rem;
            font-weight: 500;
        }}

        .repos-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.25rem;
        }}

        .repo-card {{
            background: var(--lc-bg-tertiary);
            border: 1px solid var(--lc-border);
            border-radius: var(--radius-md);
            padding: 1.5rem;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            text-decoration: none;
            display: block;
            position: relative;
        }}

        .repo-card::before {{
            content: '';
            position: absolute;
            inset: 0;
            border-radius: var(--radius-md);
            padding: 1px;
            background: var(--lc-gradient);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            opacity: 0;
            transition: opacity 0.25s;
        }}

        .repo-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: transparent;
        }}

        .repo-card:hover::before {{
            opacity: 1;
        }}

        .repo-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }}

        .repo-name {{
            font-family: 'Manrope', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--lc-teal);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .repo-name svg {{
            width: 18px;
            height: 18px;
            opacity: 0.7;
            flex-shrink: 0;
        }}

        .repo-category-badge {{
            font-size: 0.65rem;
            padding: 0.2rem 0.5rem;
            background: var(--lc-purple-muted);
            color: var(--lc-purple);
            border-radius: 50px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            white-space: nowrap;
            flex-shrink: 0;
        }}

        .repo-description {{
            font-size: 0.9rem;
            color: var(--lc-text-secondary);
            margin-bottom: 1rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            line-height: 1.5;
        }}

        .repo-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            font-size: 0.8rem;
            color: var(--lc-text-muted);
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
            gap: 0.5rem;
            margin-top: 1rem;
        }}

        .repo-topic {{
            font-size: 0.7rem;
            padding: 0.3rem 0.6rem;
            background: var(--lc-teal-muted);
            color: var(--lc-teal);
            border-radius: 50px;
            font-weight: 600;
            text-transform: lowercase;
        }}

        /* Language colors */
        .lang-python {{ color: #3572A5; }}
        .lang-javascript {{ color: #F7DF1E; }}
        .lang-typescript {{ color: #3178C6; }}
        .lang-html {{ color: #E34F26; }}
        .lang-jupyter {{ color: #F37626; }}

        /* Empty State */
        .empty-state {{
            text-align: center;
            padding: 4rem 2rem;
            color: var(--lc-text-muted);
        }}

        .empty-state svg {{
            width: 56px;
            height: 56px;
            margin-bottom: 1.25rem;
            opacity: 0.4;
            stroke: var(--lc-text-muted);
        }}

        .empty-state p {{
            font-size: 1rem;
        }}

        /* Footer */
        footer {{
            text-align: center;
            padding: 3rem 2rem;
            margin-top: 4rem;
            border-top: 1px solid var(--lc-border);
        }}

        footer p {{
            color: var(--lc-text-muted);
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }}

        footer a {{
            color: var(--lc-teal);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }}

        footer a:hover {{
            color: var(--lc-teal-hover);
            text-decoration: underline;
        }}

        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(16px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .repo-card {{
            animation: fadeInUp 0.4s ease-out;
            animation-fill-mode: backwards;
        }}

        .repo-card:nth-child(1) {{ animation-delay: 0.03s; }}
        .repo-card:nth-child(2) {{ animation-delay: 0.06s; }}
        .repo-card:nth-child(3) {{ animation-delay: 0.09s; }}
        .repo-card:nth-child(4) {{ animation-delay: 0.12s; }}
        .repo-card:nth-child(5) {{ animation-delay: 0.15s; }}
        .repo-card:nth-child(6) {{ animation-delay: 0.18s; }}
        .repo-card:nth-child(7) {{ animation-delay: 0.21s; }}
        .repo-card:nth-child(8) {{ animation-delay: 0.24s; }}
        .repo-card:nth-child(9) {{ animation-delay: 0.27s; }}
    </style>
</head>
<body>
    <div class="bg-mesh"></div>

    <!-- Theme Toggle Button -->
    <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">
        <svg class="moon-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z" />
        </svg>
        <svg class="sun-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
        </svg>
    </button>

    <div class="container">
        <header>
            <div class="logo-container">
                <img src="{self.LANGCHAIN_LOGO_URL}" alt="LangChain Logo" class="logo-icon">
            </div>
            <h1>Samples Repository Explorer</h1>
            <p class="subtitle">Discover code examples, cookbooks, reference implementations, and workshop materials from the LangChain team.</p>
        </header>

        <!-- Product Panels -->
        <div class="product-panels" id="product-panels">
            <div class="product-panel langchain" data-product="langchain">
                <div class="product-panel-header">
                    <div class="product-icon">
                        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                        </svg>
                    </div>
                    <div class="product-title">LangChain</div>
                </div>
                <div class="product-description">Framework integrations, utilities, guardrails, and middleware patterns.</div>
                <div class="product-footer">
                    <span class="product-count" id="langchain-count">0 repos</span>
                    <svg class="product-arrow" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
                    </svg>
                </div>
            </div>

            <div class="product-panel langgraph" data-product="langgraph">
                <div class="product-panel-header">
                    <div class="product-icon">
                        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21 3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
                        </svg>
                    </div>
                    <div class="product-title">LangGraph</div>
                </div>
                <div class="product-description">Agent workflows, state machines, multi-agent systems, and complex orchestration.</div>
                <div class="product-footer">
                    <span class="product-count" id="langgraph-count">0 repos</span>
                    <svg class="product-arrow" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
                    </svg>
                </div>
            </div>

            <div class="product-panel langsmith" data-product="langsmith">
                <div class="product-panel-header">
                    <div class="product-icon">
                        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 1-6.23.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                        </svg>
                    </div>
                    <div class="product-title">LangSmith</div>
                </div>
                <div class="product-description">Observability, tracing, evaluation, debugging, and deployment pipelines.</div>
                <div class="product-footer">
                    <span class="product-count" id="langsmith-count">0 repos</span>
                    <svg class="product-arrow" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
                    </svg>
                </div>
            </div>
        </div>

        <div class="controls">
            <div class="search-box">
                <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input type="text" id="search" placeholder="Search repositories, topics, or descriptions...">
            </div>
            <div class="view-toggles">
                <button class="view-btn active" data-view="topics">By Topic</button>
                <button class="view-btn" data-view="language">By Language</button>
                <button class="view-btn" data-view="difficulty">By Difficulty</button>
            </div>
        </div>

        <div class="content-area">
            <aside class="topics-sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-title" id="sidebar-title">Topics</div>
                    <button class="clear-btn hidden" id="clear-btn">Clear All</button>
                </div>
                <div class="topic-list" id="topic-list"></div>
            </aside>

            <main class="repos-container">
                <div class="repos-header">
                    <div class="repos-title" id="repos-title">All Repositories</div>
                    <div class="repos-count" id="repos-count"></div>
                </div>
                <div class="repos-grid" id="repos-grid"></div>
            </main>
        </div>

        <footer>
            <p>Auto-generated on {generated_at}</p>
            <p>
                <a href="https://github.com/{self.org_name}" target="_blank" rel="noopener">View {self.org_name} on GitHub</a>
                &nbsp;·&nbsp;
                <a href="https://www.langchain.com" target="_blank" rel="noopener">LangChain</a>
            </p>
        </footer>
    </div>

    <script>
        // Theme Management
        (function() {{
            const savedTheme = localStorage.getItem('theme');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const theme = savedTheme || (prefersDark ? 'dark' : 'light');
            if (theme === 'light') {{
                document.documentElement.setAttribute('data-theme', 'light');
            }}
        }})();

        const hierarchyData = {json.dumps(self.hierarchy)};

        let currentView = 'topics';
        let selectedTopics = [];
        let selectedProduct = null;
        let searchQuery = '';

        const topicList = document.getElementById('topic-list');
        const reposGrid = document.getElementById('repos-grid');
        const reposTitle = document.getElementById('repos-title');
        const reposCount = document.getElementById('repos-count');
        const searchInput = document.getElementById('search');
        const viewButtons = document.querySelectorAll('.view-btn');
        const clearBtn = document.getElementById('clear-btn');
        const sidebarTitle = document.getElementById('sidebar-title');
        const themeToggle = document.getElementById('theme-toggle');

        document.addEventListener('DOMContentLoaded', () => {{
            renderTopics();
            renderRepositories();
            setupEventListeners();
            setupThemeToggle();
            setupProductPanels();
            updateProductCounts();
        }});

        function setupThemeToggle() {{
            themeToggle.addEventListener('click', () => {{
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';

                if (newTheme === 'light') {{
                    document.documentElement.setAttribute('data-theme', 'light');
                }} else {{
                    document.documentElement.removeAttribute('data-theme');
                }}

                localStorage.setItem('theme', newTheme);
            }});
        }}

        // Product panel classification
        function classifyRepoByProduct(repo) {{
            const name = repo.name.toLowerCase();
            const desc = (repo.description || '').toLowerCase();
            const topics = (repo.topics || []).map(t => t.toLowerCase());
            const combined = name + ' ' + desc + ' ' + topics.join(' ');

            if (name === '.github') return null;

            // LangSmith
            const langsmithKeywords = ['langsmith', 'tracing', 'trace', 'eval', 'debug', 'observability', 'otel', 'cicd', 'deployment', 'ls-deployment'];
            if (langsmithKeywords.some(kw => combined.includes(kw))) return 'langsmith';

            // LangGraph
            const langgraphKeywords = ['langgraph', 'graph', 'agent-builder', 'agent2agent', 'agent-oauth', 'azure-langgraph', 'remote-graph'];
            if (langgraphKeywords.some(kw => combined.includes(kw))) return 'langgraph';

            // LangChain
            const langchainKeywords = ['langchain', 'guardrail', 'middleware', 'framework', 'prompt'];
            if (langchainKeywords.some(kw => combined.includes(kw))) return 'langchain';

            return null;
        }}

        function setupProductPanels() {{
            const panels = document.querySelectorAll('.product-panel');
            panels.forEach(panel => {{
                panel.addEventListener('click', () => {{
                    const product = panel.dataset.product;
                    if (selectedProduct === product) {{
                        selectedProduct = null;
                    }} else {{
                        selectedProduct = product;
                    }}
                    selectedTopics = [];
                    updateClearButton();
                    updateProductPanelStates();
                    renderSidebar();
                    renderRepositories();
                }});
            }});
        }}

        function updateProductPanelStates() {{
            const panels = document.querySelectorAll('.product-panel');
            panels.forEach(panel => {{
                const product = panel.dataset.product;
                if (selectedProduct === product) {{
                    panel.classList.add('active');
                }} else {{
                    panel.classList.remove('active');
                }}
            }});
        }}

        function updateProductCounts() {{
            const repos = hierarchyData.all_repositories || [];
            const counts = {{ langchain: 0, langgraph: 0, langsmith: 0 }};
            repos.forEach(repo => {{
                const product = classifyRepoByProduct(repo);
                if (product && counts[product] !== undefined) counts[product]++;
            }});
            document.getElementById('langchain-count').textContent = `${{counts.langchain}} repos`;
            document.getElementById('langgraph-count').textContent = `${{counts.langgraph}} repos`;
            document.getElementById('langsmith-count').textContent = `${{counts.langsmith}} repos`;
        }}

        function setupEventListeners() {{
            searchInput.addEventListener('input', (e) => {{
                searchQuery = e.target.value.toLowerCase();
                renderRepositories();
            }});

            viewButtons.forEach(btn => {{
                btn.addEventListener('click', () => {{
                    viewButtons.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentView = btn.dataset.view;
                    selectedTopics = [];
                    selectedProduct = null;
                    updateProductPanelStates();
                    updateClearButton();
                    renderSidebar();
                    renderRepositories();
                }});
            }});

            topicList.addEventListener('click', (e) => {{
                const topicItem = e.target.closest('.topic-item') || e.target.closest('.difficulty-item');
                if (topicItem && !topicItem.classList.contains('disabled')) {{
                    const topic = topicItem.dataset.topic;
                    toggleTopic(topic);
                }}
            }});

            clearBtn.addEventListener('click', () => {{
                selectedTopics = [];
                selectedProduct = null;
                updateClearButton();
                updateProductPanelStates();
                renderSidebar();
                renderRepositories();
            }});
        }}

        function toggleTopic(topic) {{
            const index = selectedTopics.indexOf(topic);
            if (index === -1) {{
                selectedTopics.push(topic);
            }} else {{
                selectedTopics.splice(index, 1);
            }}
            selectedProduct = null;
            updateProductPanelStates();
            updateClearButton();
            renderSidebar();
            renderRepositories();
        }}

        function updateClearButton() {{
            if (selectedTopics.length > 0 || selectedProduct) {{
                clearBtn.classList.remove('hidden');
                if (selectedProduct) {{
                    clearBtn.textContent = 'Clear Filter';
                }} else {{
                    clearBtn.textContent = `Clear Filter (${{selectedTopics.length}})`;
                }}
            }} else {{
                clearBtn.classList.add('hidden');
            }}
        }}

        function renderSidebar() {{
            if (currentView === 'language') {{
                sidebarTitle.textContent = 'Languages';
                renderLanguages();
            }} else if (currentView === 'difficulty') {{
                sidebarTitle.textContent = 'Difficulty';
                renderDifficulty();
            }} else {{
                sidebarTitle.textContent = 'Topics';
                renderTopics();
            }}
        }}

        // Difficulty classification
        const difficultyLevels = {{
            beginner: {{ name: 'Beginner', desc: 'Getting started & basics', keywords: ['intro', 'getting-started', 'basics', 'tutorial', 'quickstart', 'hello', 'simple', 'starter', 'demo', 'example'] }},
            intermediate: {{ name: 'Intermediate', desc: 'Integrations & patterns', keywords: ['integration', 'cookbook', 'workshop', 'custom', 'chat', 'rag', 'retrieval'] }},
            advanced: {{ name: 'Advanced', desc: 'Production & complex flows', keywords: ['production', 'deployment', 'cicd', 'pipeline', 'agent', 'langgraph', 'distributed', 'remote'] }},
            expert: {{ name: 'Expert', desc: 'Deep customization & evals', keywords: ['eval', 'guardrail', 'security', 'optimization', 'framework', 'context-failure', 'mcp', 'auth'] }}
        }};

        function classifyDifficulty(repo) {{
            const name = repo.name.toLowerCase();
            const desc = (repo.description || '').toLowerCase();
            const topics = (repo.topics || []).map(t => t.toLowerCase());
            const combined = name + ' ' + desc + ' ' + topics.join(' ');
            for (const [level, config] of Object.entries(difficultyLevels)) {{
                if (config.keywords.some(kw => combined.includes(kw))) return level;
            }}
            if (repo.topics && repo.topics.length > 2) return 'intermediate';
            return 'beginner';
        }}

        function renderDifficulty() {{
            const filteredRepos = getFilteredRepos();
            const counts = {{}};
            Object.keys(difficultyLevels).forEach(level => {{
                counts[level] = filteredRepos.filter(r => classifyDifficulty(r) === level).length;
            }});

            topicList.innerHTML = Object.entries(difficultyLevels).map(([level, config]) => {{
                const count = counts[level] || 0;
                const isDisabled = count === 0 && !selectedTopics.includes(level);
                return `
                    <div class="difficulty-item ${{selectedTopics.includes(level) ? 'active' : ''}} ${{isDisabled ? 'disabled' : ''}}" data-topic="${{level}}">
                        <div class="difficulty-info">
                            <div class="difficulty-icon ${{level}}">
                                <svg fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.568 3H5.25A2.25 2.25 0 0 0 3 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 0 0 5.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 0 0 9.568 3Z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6Z" />
                                </svg>
                            </div>
                            <div>
                                <div class="difficulty-name">${{config.name}}</div>
                                <div class="difficulty-desc">${{config.desc}}</div>
                            </div>
                        </div>
                        <span class="topic-count">${{count}}</span>
                    </div>
                `;
            }}).join('');
        }}

        // Topic groupings
        const topicGroups = {{
            'Agents & Graphs': ['langgraph', 'agent', 'agents', 'deepagent', 'deep-agent', 'tool', 'tools'],
            'Observability & Evals': ['langsmith', 'eval', 'evals', 'evaluation', 'tracing', 'observability'],
            'Testing & CI/CD': ['testing', 'test', 'cicd', 'ci-cd', 'pipeline', 'offline-eval'],
            'Security & Auth': ['guardrails', 'guardrail', 'security', 'auth', 'mcp'],
            'RAG & Retrieval': ['rag', 'retrieval', 'search', 'vector', 'embedding'],
            'Chat & UI': ['chat', 'ui', 'frontend', 'gen-ui', 'custom-output', 'slide', 'annotation'],
            'Infrastructure': ['deployment', 'production', 'distributed', 'remote', 'azure']
        }};

        function getTopicGroup(topicName) {{
            for (const [group, keywords] of Object.entries(topicGroups)) {{
                if (keywords.some(kw => topicName.toLowerCase().includes(kw))) return group;
            }}
            return 'Other';
        }}

        function renderTopics() {{
            const topics = hierarchyData.topics || {{}};
            const filteredRepos = getFilteredRepos();

            const topicCounts = {{}};
            Object.keys(topics).forEach(topicName => {{
                if (topicName === 'uncategorized') {{
                    topicCounts[topicName] = filteredRepos.filter(r => (r.topics || []).length === 0).length;
                }} else {{
                    topicCounts[topicName] = filteredRepos.filter(r => (r.topics || []).includes(topicName)).length;
                }}
            }});

            const grouped = {{}};
            Object.entries(topics).forEach(([name, data]) => {{
                const group = getTopicGroup(name);
                if (!grouped[group]) grouped[group] = [];
                grouped[group].push({{ name, data, count: topicCounts[name] || 0 }});
            }});

            Object.keys(grouped).forEach(group => {{
                grouped[group].sort((a, b) => b.data.count - a.data.count);
            }});

            const groupOrder = ['Agents & Graphs', 'Observability & Evals', 'Testing & CI/CD', 'Security & Auth', 'RAG & Retrieval', 'Chat & UI', 'Infrastructure', 'Other'];

            let html = '';
            groupOrder.forEach(groupName => {{
                const groupTopics = grouped[groupName];
                if (!groupTopics || groupTopics.length === 0) return;
                const groupCount = groupTopics.reduce((sum, t) => sum + t.count, 0);

                html += `
                    <div class="topic-group" data-group="${{groupName}}">
                        <div class="topic-group-header" onclick="this.parentElement.classList.toggle('collapsed')">
                            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                            </svg>
                            ${{groupName}}
                            <span class="topic-count" style="margin-left: auto;">${{groupCount}}</span>
                        </div>
                        <div class="topic-group-items">
                            ${{groupTopics.map(t => {{
                                const isDisabled = t.count === 0 && !selectedTopics.includes(t.name);
                                return `
                                    <div class="topic-item ${{selectedTopics.includes(t.name) ? 'active' : ''}} ${{isDisabled ? 'disabled' : ''}}" data-topic="${{t.name}}">
                                        <span class="topic-name">${{t.name}}</span>
                                        <span class="topic-count">${{t.count}}</span>
                                    </div>
                                `;
                            }}).join('')}}
                        </div>
                    </div>
                `;
            }});

            topicList.innerHTML = html;
        }}

        function renderLanguages() {{
            const languages = hierarchyData.languages || {{}};
            const filteredRepos = getFilteredRepos();

            const langCounts = {{}};
            Object.keys(languages).forEach(lang => {{
                if (lang === 'Unknown') {{
                    langCounts[lang] = filteredRepos.filter(r => !r.language).length;
                }} else {{
                    langCounts[lang] = filteredRepos.filter(r => r.language === lang).length;
                }}
            }});

            const sortedLanguages = Object.entries(languages).sort((a, b) => b[1].length - a[1].length);

            topicList.innerHTML = sortedLanguages.map(([name, repos]) => {{
                const filteredCount = langCounts[name] || 0;
                const isDisabled = filteredCount === 0 && !selectedTopics.includes(name);
                return `
                    <div class="topic-item ${{selectedTopics.includes(name) ? 'active' : ''}} ${{isDisabled ? 'disabled' : ''}}" data-topic="${{name}}">
                        <span class="topic-name">${{name}}</span>
                        <span class="topic-count">${{filteredCount}}</span>
                    </div>
                `;
            }}).join('');
        }}

        function getFilteredRepos() {{
            let repos = hierarchyData.all_repositories || [];
            repos = repos.filter(r => r.name !== '.github');

            if (selectedProduct) {{
                repos = repos.filter(repo => classifyRepoByProduct(repo) === selectedProduct);
            }}

            if (selectedTopics.length > 0) {{
                if (currentView === 'language') {{
                    repos = repos.filter(repo => {{
                        const repoLang = repo.language || 'Unknown';
                        return selectedTopics.includes(repoLang);
                    }});
                }} else if (currentView === 'difficulty') {{
                    repos = repos.filter(repo => {{
                        const repoLevel = classifyDifficulty(repo);
                        return selectedTopics.includes(repoLevel);
                    }});
                }} else {{
                    repos = repos.filter(repo => {{
                        const repoTopics = repo.topics || [];
                        return selectedTopics.every(selectedTopic => {{
                            if (selectedTopic === 'uncategorized') return repoTopics.length === 0;
                            return repoTopics.includes(selectedTopic);
                        }});
                    }});
                }}
            }}

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

            if (selectedProduct) {{
                const productNames = {{ langchain: 'LangChain', langgraph: 'LangGraph', langsmith: 'LangSmith' }};
                reposTitle.textContent = productNames[selectedProduct] + ' Repositories';
            }} else if (selectedTopics.length > 0) {{
                if (selectedTopics.length === 1) {{
                    reposTitle.textContent = selectedTopics[0];
                }} else if (selectedTopics.length <= 3) {{
                    reposTitle.textContent = selectedTopics.join(', ');
                }} else {{
                    reposTitle.textContent = `${{selectedTopics.slice(0, 2).join(', ')}} +${{selectedTopics.length - 2}} more`;
                }}
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

            reposGrid.innerHTML = repos.map(repo => {{
                const product = classifyRepoByProduct(repo);
                const categoryBadge = product ? `<span class="repo-category-badge">${{product}}</span>` : '';

                return `
                <a href="${{repo.url}}" target="_blank" rel="noopener" class="repo-card">
                    <div class="repo-header">
                        <div class="repo-name">
                            <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                            </svg>
                            ${{repo.name}}
                        </div>
                        ${{categoryBadge}}
                    </div>
                    <div class="repo-description">${{repo.description || 'No description available'}}</div>
                    <div class="repo-meta">
                        ${{repo.language ? `
                            <span class="repo-meta-item lang-${{repo.language?.toLowerCase().replace(' ', '-')}}">
                                <svg viewBox="0 0 16 16" fill="currentColor"><circle cx="8" cy="8" r="5"/></svg>
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
                        ${{repo.forks > 0 ? `
                            <span class="repo-meta-item">
                                <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M7.217 10.907a2.25 2.25 0 1 0 0 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186 9.566-5.314m-9.566 7.5 9.566 5.314m0 0a2.25 2.25 0 1 0 3.935 2.186 2.25 2.25 0 0 0-3.935-2.186Zm0-12.814a2.25 2.25 0 1 0 3.933-2.185 2.25 2.25 0 0 0-3.933 2.185Z" />
                                </svg>
                                ${{repo.forks}}
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
            `}}).join('');
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
