import os
import yaml

class ChroniclerVault:
    """
    Decentralized, offline Markdown-based storage system for the agency's worldbuilding,
    project states, and persistent memory vault. Compatible with Chronicler/Obsidian vaults.
    """
    def __init__(self, vault_path="./chronicler_vault"):
        self.vault_path = vault_path
        os.makedirs(self.vault_path, exist_ok=True)
        self._ensure_index()

    def _ensure_index(self):
        """Ensures a central index.md page exists in the vault."""
        index_path = os.path.join(self.vault_path, "index.md")
        if not os.path.exists(index_path):
            with open(index_path, "w", encoding="utf-8") as f:
                f.write("# The Sovereign Agency Chronicle Index\n\nWelcome to the decentralized brain of the agency.\n\n## Project Directory\n\n")

    def store_project(self, project_id: str, scope: str, deliverable: str, metadata: dict):
        """Stores a project as a wiki-style markdown page in the vault."""
        filename = f"{project_id}.md"
        filepath = os.path.join(self.vault_path, filename)
        
        # Format frontmatter
        frontmatter = {
            "title": f"Project {project_id}",
            "tags": ["project", metadata.get("status", "completed")],
            "price_usdt": metadata.get("price_usdt", 0.0),
            "assigned_agents": metadata.get("assigned_agents", []),
            "timestamp": metadata.get("timestamp", "")
        }
        
        yaml_str = yaml.dump(frontmatter, default_flow_style=False)
        
        content = f"""---
{yaml_str}---

# Project {project_id}

## Scope
{scope}

## Final Deliverables
{deliverable}

---
*Backlink: [[index]]*
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        # Append to index.md
        index_path = os.path.join(self.vault_path, "index.md")
        with open(index_path, "a", encoding="utf-8") as f:
            f.write(f"- [[{project_id}]] - {frontmatter['title']} ({metadata.get('status', 'completed')})\n")

        print(f"[CHRONICLER] Saved project state to {filepath}")

# Singleton vault instance
chronicler_vault = ChroniclerVault()
