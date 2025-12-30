#!/usr/bin/env python3
"""
Main build script that orchestrates the full pipeline:
1. Fetch repositories from GitHub
2. Build hierarchy data
3. Generate static site
"""

import argparse
import os
import sys

from src.github_fetcher import GitHubFetcher
from src.hierarchy_builder import HierarchyBuilder
from src.site_generator import SiteGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Build the repository hierarchy visualization site"
    )
    parser.add_argument(
        "--org",
        required=True,
        help="GitHub organization name"
    )
    parser.add_argument(
        "--output-dir",
        default="docs",
        help="Output directory for the static site (default: docs)"
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Directory for intermediate data files (default: data)"
    )
    parser.add_argument(
        "--include-forks",
        action="store_true",
        help="Include forked repositories"
    )
    parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Include archived repositories"
    )
    parser.add_argument(
        "--skip-fetch",
        action="store_true",
        help="Skip fetching data (use existing repos.json)"
    )

    args = parser.parse_args()

    # Ensure data directory exists
    os.makedirs(args.data_dir, exist_ok=True)

    repos_path = os.path.join(args.data_dir, "repos.json")
    hierarchy_path = os.path.join(args.data_dir, "hierarchy.json")

    # Step 1: Fetch repositories
    if not args.skip_fetch:
        print("\n" + "=" * 60)
        print("Step 1: Fetching repositories from GitHub")
        print("=" * 60)

        fetcher = GitHubFetcher()
        repos = fetcher.fetch_org_repos(
            org=args.org,
            include_forks=args.include_forks,
            include_archived=args.include_archived,
        )
        fetcher.save_to_json(repos, repos_path)
    else:
        print("\n" + "=" * 60)
        print("Step 1: Skipping fetch (using existing data)")
        print("=" * 60)

        if not os.path.exists(repos_path):
            print(f"Error: {repos_path} not found. Cannot skip fetch.")
            sys.exit(1)

    # Step 2: Build hierarchy
    print("\n" + "=" * 60)
    print("Step 2: Building hierarchy data")
    print("=" * 60)

    builder = HierarchyBuilder.from_json_file(repos_path)
    hierarchy = builder.build_hierarchy()
    builder.save_hierarchy(hierarchy, hierarchy_path)

    # Print summary
    stats = hierarchy.stats
    print(f"\nHierarchy Summary:")
    print(f"  Total repositories: {stats['total_repositories']}")
    print(f"  Total topics: {stats['total_topics']}")
    print(f"  Total languages: {stats['total_languages']}")
    print(f"  Repos with multiple topics: {stats['repos_with_multiple_topics']}")
    print(f"  Repos without topics: {stats['repos_without_topics']}")

    # Step 3: Generate static site
    print("\n" + "=" * 60)
    print("Step 3: Generating static site")
    print("=" * 60)

    generator = SiteGenerator(hierarchy_path, args.org)
    generator.generate(args.output_dir)

    print("\n" + "=" * 60)
    print("Build Complete!")
    print("=" * 60)
    print(f"\nStatic site generated in: {args.output_dir}/")
    print(f"Open {args.output_dir}/index.html in your browser to view.")


if __name__ == "__main__":
    main()

