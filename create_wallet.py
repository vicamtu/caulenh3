# HƯỚNG DẪN CÀI ĐẶT THƯ VIỆN:
# Mở terminal (Command Prompt) và chạy các lệnh sau:
# pip install web3      # Thư viện để tương tác với blockchain Ethereum
# pip install eth-account # Thư viện để tạo và quản lý tài khoản Ethereum
# pip install mnemonic   # Thư viện để tạo cụm từ ghi nhớ (mnemonic)
# pip install tk        # Thư viện để tạo giao diện đồ họa (có sẵn trong Python)

# Chương trình này giúp tạo ví Ethereum với các thành phần:
# 1. Mnemonic: Cụm 12 từ tiếng Anh dùng để khôi phục ví
# 2. Private Key: Khóa bí mật để ký các giao dịch
# 3. Địa chỉ ví: Dùng để nhận tiền điện tử

from eth_account import Account
from mnemonic import Mnemonic
import secrets
import sys
import tkinter as tk
from tkinter import messagebox, ttk
import threading

def tao_vi_ethereum():  # Hàm chính để tạo ví Ethereum
    try:
        # Kích hoạt tính năng tạo tài khoản từ seed
        Account.enable_unaudited_hdwallet_features()

        # Tạo cụm từ mnemonic ngẫu nhiên gồm 12 từ
        mnemo = Mnemonic("english")
        mnemonic_words = mnemo.generate(strength=128)  # 128 bit = 12 từ

        # Tạo tài khoản từ mnemonic
        account = Account.from_mnemonic(mnemonic_words)

        # Lấy private key và địa chỉ ví
        private_key = account.key.hex()
        wallet_address = account.address

        # Chuẩn bị nội dung để ghi vào file
        content = f"""Mnemonic: {mnemonic_words}
Private Key: {private_key}

CẢNH BÁO: KHÔNG CHIA SẺ cụm từ Mnemonic hoặc Private Key với bất kỳ ai!
Nếu người khác có được thông tin này, họ có thể chiếm quyền kiểm soát ví của bạn."""

        # Ghi thông tin vào file
        try:
            with open('wallet_info.txt', 'w', encoding='utf-8') as f:
                f.write(content)
            print("\nĐã lưu thông tin ví vào file 'wallet_info.txt'")
        except IOError:
            print("\nLỗi: Không thể lưu file wallet_info.txt")
            sys.exit(1)

        # Hiển thị địa chỉ ví
        print(f"\nĐịa chỉ ví của bạn: {wallet_address}")
        print("\nLưu ý: Hãy cất giữ file wallet_info.txt ở nơi an toàn!")

    except Exception as e:
        print(f"\nLỗi không mong muốn: {str(e)}")
        sys.exit(1)

class EthereumWalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tạo Ví Ethereum")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')

        # Tạo style cho ttk
        style = ttk.Style()
        style.configure('TButton', padding=10, font=('Segoe UI', 10))
        style.configure('TLabel', font=('Segoe UI', 10), background='#f0f0f0')

        # Frame chính
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Tiêu đề
        title_label = ttk.Label(main_frame, text="CHƯƠNG TRÌNH TẠO VÍ ETHEREUM", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=20)

        # Thông tin chương trình
        info_frame = ttk.LabelFrame(main_frame, text="Thông tin về chương trình", padding=10)
        info_frame.pack(fill=tk.X, pady=10)

        info_text = "Chương trình này sẽ tạo cho bạn:\n"
        info_text += "1. Cụm từ Mnemonic (12 từ tiếng Anh)\n"
        info_text += "2. Khóa bí mật (Private Key)\n"
        info_text += "3. Địa chỉ ví Ethereum"
        
        info_label = ttk.Label(info_frame, text=info_text)
        info_label.pack(pady=10)

        # Cảnh báo
        warning_frame = ttk.LabelFrame(main_frame, text="Cảnh báo an toàn", padding=10)
        warning_frame.pack(fill=tk.X, pady=10)

        warning_text = "KHÔNG CHIA SẺ cụm từ Mnemonic hoặc Private Key với bất kỳ ai!\n"
        warning_text += "Nếu người khác có được thông tin này, họ có thể chiếm quyền kiểm soát ví của bạn."
        
        warning_label = ttk.Label(warning_frame, text=warning_text, foreground='red')
        warning_label.pack(pady=10)

        # Nút tạo ví
        self.create_button = ttk.Button(main_frame, text="Tạo Ví Mới", 
                                      command=self.create_wallet_thread)
        self.create_button.pack(pady=20)

        # Kết quả
        self.result_frame = ttk.LabelFrame(main_frame, text="Kết quả", padding=10)
        self.result_frame.pack(fill=tk.X, pady=10)
        self.result_frame.pack_forget()

        self.result_label = ttk.Label(self.result_frame, text="")
        self.result_label.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')

    def create_wallet_thread(self):
        self.create_button.configure(state='disabled')
        self.progress.pack(pady=10)
        self.progress.start()

        # Tạo thread mới để không block giao diện
        thread = threading.Thread(target=self.create_wallet_process)
        thread.start()

    def create_wallet_process(self):
        try:
            # Kích hoạt tính năng tạo tài khoản từ seed
            Account.enable_unaudited_hdwallet_features()

            # Tạo cụm từ mnemonic ngẫu nhiên gồm 12 từ
            mnemo = Mnemonic("english")
            mnemonic_words = mnemo.generate(strength=128)  # 128 bit = 12 từ

            # Tạo tài khoản từ mnemonic
            account = Account.from_mnemonic(mnemonic_words)

            # Lấy private key và địa chỉ ví
            private_key = account.key.hex()
            wallet_address = account.address

            # Chuẩn bị nội dung để ghi vào file
            content = f"""Mnemonic: {mnemonic_words}
Private Key: {private_key}

CẢNH BÁO: KHÔNG CHIA SẺ cụm từ Mnemonic hoặc Private Key với bất kỳ ai!
Nếu người khác có được thông tin này, họ có thể chiếm quyền kiểm soát ví của bạn."""

            # Ghi thông tin vào file
            with open('wallet_info.txt', 'w', encoding='utf-8') as f:
                f.write(content)

            # Hiển thị kết quả trên giao diện
            self.root.after(0, self.show_result, wallet_address)

        except Exception as e:
            self.root.after(0, self.show_error, str(e))

    def show_result(self, wallet_address):
        self.progress.stop()
        self.progress.pack_forget()
        self.create_button.configure(state='normal')

        self.result_frame.pack(fill=tk.X, pady=10)
        result_text = f"Đã lưu thông tin ví vào file 'wallet_info.txt'\n\n"
        result_text += f"Địa chỉ ví của bạn:\n{wallet_address}"
        self.result_label.configure(text=result_text)

        messagebox.showinfo("Thành công", "Đã tạo ví thành công!\n\nHãy cất giữ file wallet_info.txt ở nơi an toàn!")

    def show_error(self, error_message):
        self.progress.stop()
        self.progress.pack_forget()
        self.create_button.configure(state='normal')
        messagebox.showerror("Lỗi", f"Lỗi khi tạo ví: {error_message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EthereumWalletApp(root)
    root.mainloop()