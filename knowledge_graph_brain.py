import os
import re
import sqlite3
import argparse

class KnowledgeGraphBrain:
    def __init__(self, db_path="knowledge_graph.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_schema()

    def create_schema(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS entities (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    type TEXT,
                    description TEXT,
                    source_file TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS relationships (
                    source_id TEXT,
                    target_id TEXT,
                    type TEXT,
                    description TEXT,
                    PRIMARY KEY (source_id, target_id, type)
                )
            """)

    def add_entity(self, eid, name, etype, desc, source):
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO entities (id, name, type, description, source_file)
                VALUES (?, ?, ?, ?, ?)
            """, (eid, name, etype, desc, source))

    def add_relationship(self, source, target, rtype, desc):
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO relationships (source_id, target_id, type, description)
                VALUES (?, ?, ?, ?)
            """, (source, target, rtype, desc))

    def scan_folder(self, folder_path):
        print(f"[GRAPH RAG] Indexing Markdown files in {folder_path}...")
        if not os.path.exists(folder_path):
            print(f"Error: Folder {folder_path} does not exist.")
            return
            
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, folder_path)
                    self.parse_markdown_file(filepath, rel_path)
                    
        print("[GRAPH RAG] Knowledge Graph indexing completed.")

    def parse_markdown_file(self, filepath, rel_path):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Add the document itself as an entity
        doc_id = rel_path.lower().replace("\\", "/").replace(".md", "")
        self.add_entity(doc_id, rel_path, "Document", f"Markdown file in Chronicle Vault: {rel_path}", rel_path)

        # 1. Parse headers as sections
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.M)
        for level, title in headers:
            section_id = f"{doc_id}#{title.lower().replace(' ', '_')}"
            self.add_entity(section_id, title, f"Header_L{len(level)}", f"Section: {title}", rel_path)
            self.add_relationship(doc_id, section_id, "CONTAINS", "Document contains section")

        # 2. Parse Markdown file links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for label, path in links:
            if ".md" in path or "chronicler_vault" in path:
                # Resolve target ID
                target_name = os.path.basename(path).replace(".md", "")
                target_id = target_name.lower()
                self.add_relationship(doc_id, target_id, "LINKS_TO", f"Linked via label: {label}")

        # 3. Parse agent mentions
        agents_pool = ["closer_agent", "defi_architect_agent", "geology_agent", "qa_agent", "orchestrator_agent", "consultant_agent", "micro_saas_dev_agent"]
        for agent in agents_pool:
            if agent in content:
                agent_id = agent.lower()
                self.add_entity(agent_id, agent, "Agent", f"Sovereign Conglomerate specialist: {agent}", rel_path)
                self.add_relationship(doc_id, agent_id, "MENTIONS", "Document mentions agent")

    def query_graph(self, term):
        cursor = self.conn.cursor()
        
        # Look for matching entities
        cursor.execute("SELECT id, name, type, description FROM entities WHERE id LIKE ? OR name LIKE ?", (f"%{term}%", f"%{term}%"))
        entities = cursor.fetchall()
        
        if not entities:
            return f"No entities found in Knowledge Graph matching: '{term}'"
            
        result_str = f"=== Knowledge Graph Query Results for '{term}' ===\n\n"
        
        for eid, name, etype, desc in entities:
            result_str += f"Entity: {name} ({etype})\nDescription: {desc}\n"
            
            # Fetch relationships where this entity is the source
            cursor.execute("""
                SELECT target_id, type, description FROM relationships WHERE source_id = ?
            """, (eid,))
            rels_out = cursor.fetchall()
            if rels_out:
                result_str += "  Outgoing connections:\n"
                for target, rtype, rdesc in rels_out:
                    # Get target name
                    cursor.execute("SELECT name FROM entities WHERE id = ?", (target,))
                    t_name_row = cursor.fetchone()
                    t_name = t_name_row[0] if t_name_row else target
                    result_str += f"    --[{rtype}]--> {t_name} ({rdesc})\n"
                    
            # Fetch relationships where this entity is the target
            cursor.execute("""
                SELECT source_id, type, description FROM relationships WHERE target_id = ?
            """, (eid,))
            rels_in = cursor.fetchall()
            if rels_in:
                result_str += "  Incoming connections:\n"
                for source, rtype, rdesc in rels_in:
                    cursor.execute("SELECT name FROM entities WHERE id = ?", (source,))
                    s_name_row = cursor.fetchone()
                    s_name = s_name_row[0] if s_name_row else source
                    result_str += f"    <--[{rtype}]-- {s_name} ({rdesc})\n"
                    
            result_str += "\n"
            
        return result_str

def main():
    parser = argparse.ArgumentParser(description="Second Brain Knowledge Graph RAG Indexer")
    parser.add_argument("--scan", action="store_true", help="Scan local chronicler_vault folder to compile graph")
    parser.add_argument("--query", help="Query a term in the indexed Knowledge Graph")
    args = parser.parse_args()
    
    brain = KnowledgeGraphBrain()
    
    if args.scan:
        brain.scan_folder("chronicler_vault")
    elif args.query:
        print(brain.query_graph(args.query))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
