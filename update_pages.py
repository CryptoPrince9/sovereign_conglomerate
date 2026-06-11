import re

def replace_main(filepath, new_main_content):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Use regex to replace everything between <main class="pt-20"> and </main>
    # We'll match up to </main>
    pattern = re.compile(r'(<main class="pt-20">).*?(</main>)', re.DOTALL)
    new_content = pattern.sub(r'\1\n' + new_main_content + r'\n\2', content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

docs_main = """
<section class="px-margin-mobile md:px-margin-desktop py-32 max-w-4xl mx-auto">
    <div class="glass-panel p-xl rounded-xl">
        <h1 class="font-display-lg text-display-lg-mobile md:text-display-lg text-primary-container mb-lg">Documentation</h1>
        <div class="space-y-md text-on-surface-variant font-body-lg">
            <h2 class="font-headline-md text-on-surface">1. Introduction</h2>
            <p>Welcome to the Sovereign Agency API documentation. Our system utilizes a decentralized agentic workforce capable of autonomous execution across multiple domains.</p>
            
            <h2 class="font-headline-md text-on-surface mt-lg">2. Getting Started</h2>
            <p>To begin deployment, navigate to the Home page and use the <strong>Initialize Deployment</strong> portal. Submit your project scope, and our Closer Agent will assess and provide a computational quote in USDT.</p>
            
            <h2 class="font-headline-md text-on-surface mt-lg">3. Web3 Escrow Integration</h2>
            <p>Our platform enforces an ironclad gating mechanism via Polygon smart contracts. Agents are dispatched only upon confirmed Web3 deposits, ensuring secure B2B transactions.</p>
        </div>
    </div>
</section>
"""

privacy_main = """
<section class="px-margin-mobile md:px-margin-desktop py-32 max-w-4xl mx-auto">
    <div class="glass-panel p-xl rounded-xl">
        <h1 class="font-display-lg text-display-lg-mobile md:text-display-lg text-primary-container mb-lg">Privacy Policy</h1>
        <div class="space-y-md text-on-surface-variant font-body-lg">
            <p>Last Updated: October 2024</p>
            <h2 class="font-headline-md text-on-surface mt-lg">1. Data Collection</h2>
            <p>We collect only essential deployment metadata required for our autonomous agents to execute your requested scopes. All processing is strictly confidential.</p>
            
            <h2 class="font-headline-md text-on-surface mt-lg">2. Data Security</h2>
            <p>All stored intelligence is protected via SHA-256 encryption. We utilize isolated sandboxes for each client deployment to prevent cross-contamination of proprietary business logic.</p>
            
            <h2 class="font-headline-md text-on-surface mt-lg">3. Blockchain Privacy</h2>
            <p>On-chain payment data on the Polygon network is inherently public, but the association with your proprietary project scope remains securely off-chain.</p>
        </div>
    </div>
</section>
"""

terms_main = """
<section class="px-margin-mobile md:px-margin-desktop py-32 max-w-4xl mx-auto">
    <div class="glass-panel p-xl rounded-xl">
        <h1 class="font-display-lg text-display-lg-mobile md:text-display-lg text-primary-container mb-lg">Terms of Service</h1>
        <div class="space-y-md text-on-surface-variant font-body-lg">
            <p>Last Updated: October 2024</p>
            <h2 class="font-headline-md text-on-surface mt-lg">1. Agreement to Terms</h2>
            <p>By accessing the Sovereign Agency API and utilizing our autonomous agents, you agree to be bound by these Terms of Service.</p>
            
            <h2 class="font-headline-md text-on-surface mt-lg">2. Escrow & Payments</h2>
            <p>All quotes are generated dynamically and finalized upon deposit. Deposits to the escrow contract are non-refundable once agent execution commences unless automated QA fails to deliver the promised scope.</p>
            
            <h2 class="font-headline-md text-on-surface mt-lg">3. Limitation of Liability</h2>
            <p>While our agents operate with high-alpha precision, Sovereign Agency is not liable for indirect or consequential damages arising from deployed code or financial models.</p>
        </div>
    </div>
</section>
"""

services_main = """
<section class="px-margin-mobile md:px-margin-desktop py-32 max-w-4xl mx-auto">
    <div class="glass-panel p-xl rounded-xl">
        <h1 class="font-display-lg text-display-lg-mobile md:text-display-lg text-primary-container mb-lg">Our Services</h1>
        <div class="space-y-md text-on-surface-variant font-body-lg">
            <h2 class="font-headline-md text-on-surface">Comprehensive Agentic Deployment</h2>
            <p>We provide a full-spectrum workforce powered by LLM-driven agents. Our primary services include:</p>
            <ul class="list-disc pl-lg mt-sm space-y-sm">
                <li><strong>DeFi Architecture:</strong> Automated smart contract generation and tokenomics modeling.</li>
                <li><strong>Micro-SaaS Scaffolding:</strong> Full-stack API and UI development at extreme velocity.</li>
                <li><strong>B2B Automation:</strong> Deep integrations of disparate internal tools using custom orchestrators.</li>
                <li><strong>Executive QA:</strong> Rigorous autonomous code review and vulnerability analysis.</li>
            </ul>
        </div>
    </div>
</section>
"""

network_main = """
<section class="px-margin-mobile md:px-margin-desktop py-32 max-w-4xl mx-auto">
    <div class="glass-panel p-xl rounded-xl">
        <h1 class="font-display-lg text-display-lg-mobile md:text-display-lg text-primary-container mb-lg">Agent Network</h1>
        <div class="space-y-md text-on-surface-variant font-body-lg">
            <h2 class="font-headline-md text-on-surface">The Swarm Infrastructure</h2>
            <p>Our autonomous network consists of highly specialized computational agents operating in parallel. By utilizing a LangGraph matrix, our agents communicate, delegate, and execute complex logic trees entirely independently of human intervention.</p>
            <div class="p-md bg-surface-container border border-white/10 rounded-lg mt-md">
                <p class="font-mono-data text-primary">STATUS: ALL NODES OPERATIONAL</p>
                <p class="font-mono-data text-on-surface-variant mt-xs">Active Agents: 142</p>
                <p class="font-mono-data text-on-surface-variant mt-xs">Network Load: 12%</p>
            </div>
        </div>
    </div>
</section>
"""

contact_main = """
<section class="px-margin-mobile md:px-margin-desktop py-32 max-w-4xl mx-auto">
    <div class="glass-panel p-xl rounded-xl">
        <h1 class="font-display-lg text-display-lg-mobile md:text-display-lg text-primary-container mb-lg">Contact Operations</h1>
        <div class="space-y-md text-on-surface-variant font-body-lg">
            <p>Direct communication with Sovereign Agency operations.</p>
            <form class="space-y-md mt-lg" onsubmit="event.preventDefault(); alert('Message dispatched to Sovereign Command.');">
                <div>
                    <label class="block font-label-caps text-label-caps text-on-surface-variant mb-xs">Identity Hash / Email</label>
                    <input type="text" class="w-full bg-surface-container-low/50 border border-white/10 rounded-lg p-md text-on-surface focus:outline-none focus:border-primary-container" required>
                </div>
                <div>
                    <label class="block font-label-caps text-label-caps text-on-surface-variant mb-xs">Message</label>
                    <textarea class="w-full h-32 bg-surface-container-low/50 border border-white/10 rounded-lg p-md text-on-surface focus:outline-none focus:border-primary-container" required></textarea>
                </div>
                <button type="submit" class="bg-primary-container text-on-primary font-label-caps text-label-caps px-xl py-md rounded-lg primary-glow transition-all">
                    Dispatch Transmission
                </button>
            </form>
        </div>
    </div>
</section>
"""

replace_main("frontend/docs.html", docs_main)
replace_main("frontend/privacy.html", privacy_main)
replace_main("frontend/terms.html", terms_main)
replace_main("frontend/services.html", services_main)
replace_main("frontend/network.html", network_main)
replace_main("frontend/contact.html", contact_main)
print("Updated all html files.")
