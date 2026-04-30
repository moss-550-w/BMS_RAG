import os

def generate_minimal_png(file_path):
    minimal_png_hex = (
        "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
        "0000000a49444154789c63000100000500010d0a2db40000000049454e44ae426082"
    )
    data = bytes.fromhex(minimal_png_hex)
    with open(file_path, 'wb') as f:
        f.write(data)

assets_dir = r"d:\CODE\BMS_RAG\mp_frontend\assets"
# 仅针对 TabBar 报错的图标进行重置
tabbar_assets = [
    "chat.png", "chat_active.png", 
    "book.png", "book_active.png", 
    "user.png", "user_active.png"
]

for asset in tabbar_assets:
    generate_minimal_png(os.path.join(assets_dir, asset))
    print(f"Reset {asset} to minimal size.")
