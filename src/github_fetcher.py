"""
Fetch repositories and topics from a GitHub organization.
"""

import os
import json
import requests
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Repository:
    """Represents a GitHub repository with its metadata."""
    name: str
    full_name: str
    description: Optional[str]
    url: str
    topics: list[str]
    language: Optional[str]
    stars: int
    forks: int
    updated_at: str
    archived: bool
    is_fork: bool


class GitHubFetcher:
    """Fetches repository data from GitHub API."""

    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        """
        Initialize the fetcher with optional authentication.

        Args:
            token: GitHub personal access token (optional but recommended for higher rate limits)
        """
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def fetch_org_repos(self, org: str, include_forks: bool = False, include_archived: bool = False) -> list[Repository]:
        """
        Fetch all repositories from a GitHub organization.

        Args:
            org: GitHub organization name
            include_forks: Whether to include forked repositories
            include_archived: Whether to include archived repositories

        Returns:
            List of Repository objects
        """
        repos = []
        page = 1
        per_page = 100

        while True:
            url = f"{self.BASE_URL}/orgs/{org}/repos"
            params = {
                "page": page,
                "per_page": per_page,
                "sort": "updated",
                "direction": "desc",
            }

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json()
            if not data:
                break

            for repo_data in data:
                # Filter based on options
                if repo_data.get("fork") and not include_forks:
                    continue
                if repo_data.get("archived") and not include_archived:
                    continue

                repo = Repository(
                    name=repo_data["name"],
                    full_name=repo_data["full_name"],
                    description=repo_data.get("description"),
                    url=repo_data["html_url"],
                    topics=repo_data.get("topics", []),
                    language=repo_data.get("language"),
                    stars=repo_data.get("stargazers_count", 0),
                    forks=repo_data.get("forks_count", 0),
                    updated_at=repo_data.get("updated_at", ""),
                    archived=repo_data.get("archived", False),
                    is_fork=repo_data.get("fork", False),
                )
                repos.append(repo)

            page += 1

        return repos

    def save_to_json(self, repos: list[Repository], output_path: str) -> None:
        """Save repositories to a JSON file."""
        data = {
            "repositories": [asdict(repo) for repo in repos],
            "total_count": len(repos),
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Saved {len(repos)} repositories to {output_path}")


def main():
    """Main entry point for fetching GitHub data."""
    import argparse

    parser = argparse.ArgumentParser(description="Fetch GitHub organization repositories")
    parser.add_argument("--org", required=True, help="GitHub organization name")
    parser.add_argument("--output", default="data/repos.json", help="Output JSON file path")
    parser.add_argument("--include-forks", action="store_true", help="Include forked repositories")
    parser.add_argument("--include-archived", action="store_true", help="Include archived repositories")

    args = parser.parse_args()

    fetcher = GitHubFetcher()
    repos = fetcher.fetch_org_repos(
        org=args.org,
        include_forks=args.include_forks,
        include_archived=args.include_archived,
    )

    fetcher.save_to_json(repos, args.output)

    # Print summary
    all_topics = set()
    for repo in repos:
        all_topics.update(repo.topics)

    print(f"\nSummary:")
    print(f"  Total repositories: {len(repos)}")
    print(f"  Unique topics: {len(all_topics)}")
    print(f"  Topics: {', '.join(sorted(all_topics))}")


if __name__ == "__main__":
    main()

