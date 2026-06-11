import os
import time
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
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.treasury_address = os.getenv("TREASURY_WALLET_ADDRESS", "0x0000000000000000000000000000000000000000")
        self.usdt_address = os.getenv("USDT_CONTRACT_ADDRESS", "0xc2132D05D31c914a87C6611C10748AEb04B58e8F")
        
        if self.w3.is_connected():
            self.usdt_contract = self.w3.eth.contract(address=self.w3.to_checksum_address(self.usdt_address), abi=ERC20_ABI)
        else:
            print("[TREASURY] Warning: Failed to connect to Web3 Provider.")

    def verify_payment(self, expected_amount_usdt: float, client_address: str = None) -> bool:
        """
        Polls for a Transfer event to the treasury wallet matching the expected amount.
        Blocks strictly until payment is verified. No mocks.
        """
        print(f"[TREASURY] Awaiting payment of {expected_amount_usdt} USDT to {self.treasury_address} on Polygon...")
        
        if not self.w3.is_connected():
            raise Exception("[TREASURY ERROR] Web3 Provider is disconnected. Cannot verify payment.")

        target_value_wei = int(expected_amount_usdt * 10**6)
        
        while True:
            try:
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
                print(f"[TREASURY] Error scanning for payments: {e}")
                
            print("[TREASURY] Payment not detected yet. Retrying in 10 seconds...")
            time.sleep(10)

treasury = Web3Treasury()
