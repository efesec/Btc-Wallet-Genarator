import os
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

def generate_btc_wallets():
    print(f"{Fore.CYAN}{Style.BRIGHT}=== BITCOIN WALLET GENERATOR ==={Style.RESET_ALL}")
    
    try:
        user_input = input(f"{Fore.YELLOW}How many wallets do you want to generate? {Fore.WHITE}")
        count = int(user_input)
    except ValueError:
        print(f"{Fore.RED}Error: Please enter a valid number.")
        return

    mnemo = Mnemonic("english")
    file_name = "btcwallet.txt"

    # Using absolute path to ensure the file is created in the script's directory
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            for i in range(1, count + 1):
                # Generate 12-word mnemonic
                words = mnemo.generate(strength=128)
                
                # Derive Seed and Address
                seed_bytes = Bip39SeedGenerator(words).Generate()
                bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
                address = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
                
                # Terminal UI
                header = f"{Fore.GREEN}--- Wallet #{i} ---"
                seed_text = f"{Fore.BLUE}Seed: {Fore.WHITE}{words}"
                addr_text = f"{Fore.MAGENTA}Address: {Fore.YELLOW}{address}"
                
                print(f"\n{header}\n{seed_text}\n{addr_text}")
                
                # Write to TXT
                f.write(f"Wallet #{i}\nSeed: {words}\nAddress: {address}\n{'-'*50}\n")
                f.flush() # Forces writing to disk

        print(f"\n{Fore.CYAN}{Style.BRIGHT}Success! Wallets saved to: {Fore.WHITE}{file_path}")
    
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")

if __name__ == "__main__":
    generate_btc_wallets()