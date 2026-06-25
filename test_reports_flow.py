import subprocess
import time
import urllib.request
import json
import sys
import os

def run_tests():
    print("[TEST] Launching uvicorn server...")
    log_path = "uvicorn_test_server.log"
    log_file = open(log_path, "w", encoding="utf-8")
    
    python_exe = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        python_exe = "python"
        
    # Add -u flag to disable buffering
    proc = subprocess.Popen(
        [python_exe, "-u", "-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8123"],
        stdout=log_file,
        stderr=log_file
    )
    
    # Wait for server to boot
    time.sleep(25)
    
    base_url = "http://127.0.0.1:8123"
    
    try:
        # Test 1: Purchase Geology Report
        print("[TEST] Testing /api/purchase-report for report-rare-earths...")
        req = urllib.request.Request(
            f"{base_url}/api/purchase-report",
            data=json.dumps({"report_id": "report-rare-earths"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            print("[TEST] Purchase response:", data)
            project_id = data["project_id"]
            price = data["quoted_price_usdt"]
            assert "report-report-rare-earths-" in project_id, "Project ID prefix mismatch"
            assert price == 150.0, "Geology report price mismatch"
            
        # Test 2: Check status (Pending Payment)
        print(f"[TEST] Testing /api/status/{project_id}...")
        with urllib.request.urlopen(f"{base_url}/api/status/{project_id}") as res:
            status_data = json.loads(res.read().decode("utf-8"))
            print("[TEST] Initial status:", status_data)
            assert status_data["payment_status"] == "PENDING", "Payment status should be PENDING"
            
        # Test 3: Simulating pay via POST /api/pay/{project_id}
        print(f"[TEST] Testing /api/pay/{project_id}...")
        req_pay = urllib.request.Request(
            f"{base_url}/api/pay/{project_id}",
            data=b"",
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_pay) as res:
            pay_data = json.loads(res.read().decode("utf-8"))
            print("[TEST] Pay response:", pay_data)
            assert pay_data["status"] == "success", "Payment should succeed"
            
        # Test 4: Check status again (Should be PAID)
        print(f"[TEST] Verifying updated status of {project_id}...")
        with urllib.request.urlopen(f"{base_url}/api/status/{project_id}") as res:
            updated_status = json.loads(res.read().decode("utf-8"))
            print("[TEST] Updated status:", updated_status)
            assert updated_status["payment_status"] == "PAID", "Payment status should be PAID"
            
        # Test 5: Fetch deliverables
        print(f"[TEST] Testing /api/deliverable/{project_id}...")
        with urllib.request.urlopen(f"{base_url}/api/deliverable/{project_id}") as res:
            deliv_data = json.loads(res.read().decode("utf-8"))
            print("[TEST] Deliverables fetched. Previewing first 100 characters:")
            preview = deliv_data["deliverable"][:100]
            print(f"       {preview}...")
            assert "# Decentralized Rare Earth" in deliv_data["deliverable"], "Deliverable content mismatch"
            
        # Test 6: Verify normal project intake still works (bypass mode)
        print("[TEST] Testing standard intake with bypass...")
        req_intake = urllib.request.Request(
            f"{base_url}/api/intake",
            data=json.dumps({"project_scope": "Testing normal operations. test_wallet_bypass"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_intake) as res:
            intake_data = json.loads(res.read().decode("utf-8"))
            print("[TEST] Intake response:", intake_data)
            
        print("[TEST] All tests passed successfully! [SUCCESS]")
        sys.exit(0)
        
    except Exception as e:
        print(f"[TEST ERROR] Test failed: {e}", file=sys.stderr)
        log_file.close()
        # Print server logs to see what failed
        if os.path.exists(log_path):
            print("\n=== UVICORN SERVER LOGS ===")
            with open(log_path, "r", encoding="utf-8") as f:
                print(f.read())
            print("===========================\n")
        sys.exit(1)
        
    finally:
        print("[TEST] Terminating uvicorn server...")
        log_file.close()
        proc.terminate()
        proc.wait()
        # Clean up log
        if os.path.exists(log_path):
            try:
                os.remove(log_path)
            except:
                pass

if __name__ == "__main__":
    run_tests()
