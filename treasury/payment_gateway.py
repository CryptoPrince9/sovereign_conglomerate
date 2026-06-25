import os
import time
import sqlite3
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Standard ERC-20 ABI for Transfer event
ERC20_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    }
]

class Web3Treasury:
    """
    Autonomous Web3 Treasury Layer for The Sovereign Conglomerate.
    Listens for incoming USDT payments on EVM-compatible networks.
    """
    def __init__(self):
        self.rpc_url = os.getenv("POLYGON_RPC_URL", "https://polygon.llamarpc.com")
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url, request_kwargs={'timeout': 3}))
        self.treasury_address = os.getenv("TREASURY_WALLET_ADDRESS", "0x0000000000000000000000000000000000000000")
        self.usdt_address = os.getenv("USDT_CONTRACT_ADDRESS", "0xc2132D05D31c914a87C6611C10748AEb04B58e8F")
        
        if self.w3.is_connected():
            self.usdt_contract = self.w3.eth.contract(address=self.w3.to_checksum_address(self.usdt_address), abi=ERC20_ABI)
        else:
            self.usdt_contract = None
            print("[TREASURY] Warning: Failed to connect to Web3 Provider.")

    def verify_payment(self, expected_amount_usdt: float, client_address: str = None, project_id: str = None) -> bool:
        """
        Polls for a Transfer event to the treasury wallet matching the expected amount.
        Blocks strictly until payment is verified. Checked against local SQLite override first.
        """
        print(f"[TREASURY] Awaiting payment of {expected_amount_usdt} USDT to {self.treasury_address} on Polygon (Project: {project_id})...")
        if expected_amount_usdt <= 0:
            print("[TREASURY] Bypass detected: expected amount is 0 USDT.")
            return True
        
        while True:
            # 1. Check local SQLite database for manual/simulated payment confirmation
            if project_id:
                try:
                    conn = sqlite3.connect("agency_database.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT state FROM projects WHERE id = ?", (project_id,))
                    row = cursor.fetchone()
                    conn.close()
                    if row:
                        state_dict = json.loads(row[0])
                        if state_dict.get("payment_status") == "PAID":
                            print(f"[TREASURY] ✅ Payment verified via Database flag for project {project_id}")
                            return True
                except Exception as db_err:
                    print(f"[TREASURY] Error checking DB inside verify_payment: {db_err}")

            # 2. Check Blockchain if Web3 is connected
            if self.w3.is_connected() and self.usdt_contract is not None:
                try:
                    target_value_wei = int(expected_amount_usdt * 10**6)
                    current_block = self.w3.eth.block_number
                    event_filter = self.usdt_contract.events.Transfer.create_filter(
                        fromBlock=current_block - 100,
                        toBlock='latest',
                        argument_filters={'to': self.w3.to_checksum_address(self.treasury_address)}
                    )
                    
                    entries = event_filter.get_all_entries()
                    for entry in entries:
                        value = entry['args']['value']
                        sender = entry['args']['from']
                        
                        if value >= target_value_wei:
                            if client_address and sender.lower() != client_address.lower():
                                continue
                            print(f"[TREASURY] ✅ Verified Transfer of {value / 10**6} USDT from {sender} at block {entry['blockNumber']}")
                            return True
                            
                except Exception as e:
                    print(f"[TREASURY] Error scanning for blockchain payments: {e}")
            else:
                # Avoid logging this continuously to reduce terminal spam
                pass
                
            print("[TREASURY] Payment not detected yet. Retrying in 10 seconds...")
            time.sleep(10)

treasury = Web3Treasury()
