import os
import sys
from audio_pipeline import run_audiblez_pipeline

def run_pipeline():
    print("[MARKETING AUDIO PIPELINE] Initiating zero-cost content creation...")
    
    # Check if there is an existing marketing copy to convert
    default_text = (
        "Welcome to the Sovereign AI Agency. We build autonomous, decentralized, "
        "and self-healing AI agent conglomerates that operate with zero overhead and "
        "maximize returns. Our multi-agent swarms operate across DeFi, earth sciences, "
        "and patent discovery."
    )
    
    # We can read from marketing_copy.md if it exists
    copy_path = "../../brain/897999ce-21b3-489b-9f31-fd3967262cbe/marketing_copy.md"
    if os.path.exists(copy_path):
        print(f"[MARKETING AUDIO PIPELINE] Found client marketing copy at {copy_path}. Reading...")
        with open(copy_path, "r", encoding="utf-8") as f:
            text_to_convert = f.read()
    else:
        print("[MARKETING AUDIO PIPELINE] No copy path found. Using default marketing text.")
        text_to_convert = default_text
        
    print("[MARKETING AUDIO PIPELINE] Compiling text to voice track...")
    result = run_audiblez_pipeline(text_to_convert, voice="af_sky", output_name="sovereign_agency_promo")
    print(f"[MARKETING AUDIO PIPELINE] Result: {result}")

if __name__ == "__main__":
    run_pipeline()
