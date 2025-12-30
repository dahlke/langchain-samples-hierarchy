"""
Build hierarchical structures from repository topics.
"""

import json
from collections import defaultdict
from dataclasses import dataclass, asdict, field
from typing import Optional


@dataclass
class TopicNode:
    """Represents a topic node in the hierarchy."""
    name: str
    repositories: list[dict] = field(default_factory=list)
    count: int = 0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "repositories": self.repositories,
            "count": self.count,
        }


@dataclass
class HierarchyData:
    """Complete hierarchy data structure for the visualization."""
    topics: dict[str, TopicNode]
    all_repositories: list[dict]
    topic_connections: list[dict]  # repos that share multiple topics
    languages: dict[str, list[dict]]
    stats: dict

    def to_dict(self) -> dict:
        return {
            "topics": {k: v.to_dict() for k, v in self.topics.items()},
            "all_repositories": self.all_repositories,
            "topic_connections": self.topic_connections,
            "languages": self.languages,
            "stats": self.stats,
        }


class HierarchyBuilder:
    """Builds hierarchical data structures from repository data."""

    def __init__(self, repos_data: dict):
        """
        Initialize with repository data.

        Args:
            repos_data: Dictionary containing repository information
        """
        self.repositories = repos_data.get("repositories", [])

    @classmethod
    def from_json_file(cls, filepath: str) -> "HierarchyBuilder":
        """Load repository data from a JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls(data)

    def build_hierarchy(self) -> HierarchyData:
        """
        Build the complete hierarchy from repository data.

        Returns:
            HierarchyData object containing organized data
        """
        # Group by topics
        topics: dict[str, TopicNode] = {}
        languages: dict[str, list[dict]] = defaultdict(list)
        topic_connections: list[dict] = []

        for repo in self.repositories:
            repo_topics = repo.get("topics", [])
            repo_language = repo.get("language")

            # Add to topic groups
            for topic in repo_topics:
                if topic not in topics:
                    topics[topic] = TopicNode(name=topic)
                topics[topic].repositories.append(repo)
                topics[topic].count += 1

            # Track repos with no topics
            if not repo_topics:
                if "uncategorized" not in topics:
                    topics["uncategorized"] = TopicNode(name="uncategorized")
                topics["uncategorized"].repositories.append(repo)
                topics["uncategorized"].count += 1

            # Group by language
            if repo_language:
                languages[repo_language].append(repo)
            else:
                languages["Unknown"].append(repo)

            # Track topic connections (repos with multiple topics)
            if len(repo_topics) > 1:
                topic_connections.append({
                    "repository": repo["name"],
                    "topics": repo_topics,
                    "url": repo["url"],
                })

        # Calculate stats
        stats = self._calculate_stats(topics, languages)

        return HierarchyData(
            topics=topics,
            all_repositories=self.repositories,
            topic_connections=topic_connections,
            languages=dict(languages),
            stats=stats,
        )

    def _calculate_stats(self, topics: dict[str, TopicNode], languages: dict) -> dict:
        """Calculate summary statistics."""
        total_stars = sum(repo.get("stars", 0) for repo in self.repositories)
        total_forks = sum(repo.get("forks", 0) for repo in self.repositories)

        # Most popular topics by repo count
        sorted_topics = sorted(
            topics.items(),
            key=lambda x: x[1].count,
            reverse=True
        )

        # Most popular languages
        sorted_languages = sorted(
            languages.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )

        return {
            "total_repositories": len(self.repositories),
            "total_topics": len([t for t in topics if t != "uncategorized"]),
            "total_languages": len([l for l in languages if l != "Unknown"]),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "top_topics": [
                {"name": name, "count": node.count}
                for name, node in sorted_topics[:10]
            ],
            "top_languages": [
                {"name": name, "count": len(repos)}
                for name, repos in sorted_languages[:10]
            ],
            "repos_with_multiple_topics": len([
                r for r in self.repositories
                if len(r.get("topics", [])) > 1
            ]),
            "repos_without_topics": len([
                r for r in self.repositories
                if not r.get("topics")
            ]),
        }

    def save_hierarchy(self, hierarchy: HierarchyData, output_path: str) -> None:
        """Save hierarchy data to a JSON file."""
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(hierarchy.to_dict(), f, indent=2)

        print(f"Saved hierarchy data to {output_path}")


def main():
    """Main entry point for building hierarchy."""
    import argparse

    parser = argparse.ArgumentParser(description="Build hierarchy from repository data")
    parser.add_argument("--input", default="data/repos.json", help="Input JSON file with repo data")
    parser.add_argument("--output", default="data/hierarchy.json", help="Output JSON file path")

    args = parser.parse_args()

    builder = HierarchyBuilder.from_json_file(args.input)
    hierarchy = builder.build_hierarchy()
    builder.save_hierarchy(hierarchy, args.output)

    # Print summary
    stats = hierarchy.stats
    print(f"\nHierarchy Summary:")
    print(f"  Total repositories: {stats['total_repositories']}")
    print(f"  Total topics: {stats['total_topics']}")
    print(f"  Total languages: {stats['total_languages']}")
    print(f"  Repos with multiple topics: {stats['repos_with_multiple_topics']}")
    print(f"  Repos without topics: {stats['repos_without_topics']}")

    print(f"\nTop Topics:")
    for topic in stats['top_topics'][:5]:
        print(f"  {topic['name']}: {topic['count']} repos")


if __name__ == "__main__":
    main()

