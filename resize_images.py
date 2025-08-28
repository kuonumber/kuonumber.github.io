#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
圖片尺寸調整器 - 為網頁使用優化 (Logo + 頭像)
"""

from PIL import Image
import os

def resize_avatar_for_web():
    """將頭像調整為網頁適合的尺寸"""
    
    # 檢查原始頭像是否存在
    avatar_path = "images/author_.jpg"
    if not os.path.exists(avatar_path):
        print("❌ 找不到原始頭像文件: images/author_.jpg")
        return
    
    try:
        # 打開原始頭像
        original_avatar = Image.open(avatar_path)
        print(f"✅ 原始頭像尺寸: {original_avatar.size[0]} x {original_avatar.size[1]} 像素")
        
        # 定義網頁頭像使用的尺寸 (比之前大一些)
        avatar_sizes = {
            "avatar_large": (150, 150),      # 大頭像 (About頁面)
            "avatar_medium": (120, 120),     # 中等頭像 (側邊欄)
            "avatar_small": (80, 80),        # 小頭像 (評論區)
            "avatar_navbar": (60, 60),       # 導航欄頭像
            "avatar_favicon": (48, 48)       # 極小頭像
        }
        
        print("\n🔄 正在生成不同尺寸的頭像...")
        
        # 為每個尺寸生成頭像
        for size_name, (width, height) in avatar_sizes.items():
            # 調整尺寸，保持寬高比
            resized_avatar = original_avatar.resize((width, height), Image.Resampling.LANCZOS)
            
            # 生成文件名
            filename = f"images/author_{size_name}.jpg"
            
            # 保存調整後的頭像，使用JPEG格式以減少文件大小
            resized_avatar.save(filename, "JPEG", quality=90, optimize=True)
            
            # 獲取文件大小
            file_size = os.path.getsize(filename)
            file_size_kb = file_size / 1024
            
            print(f"✅ {size_name}: {width}x{height}px - {file_size_kb:.1f} KB")
        
        # 創建一個專門用於網站的標準頭像 (尺寸比之前大)
        web_avatar = original_avatar.resize((120, 120), Image.Resampling.LANCZOS)
        web_avatar.save("images/author_web.jpg", "JPEG", quality=90, optimize=True)
        
        # 獲取文件大小
        web_file_size = os.path.getsize("images/author_web.jpg")
        web_file_size_kb = web_file_size / 1024
        
        print(f"\n✅ 網站標準頭像: 120x120px - {web_file_size_kb:.1f} KB")
        
        print("\n📁 生成的頭像文件：")
        for size_name, (width, height) in avatar_sizes.items():
            filename = f"images/author_{size_name}.jpg"
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                file_size_kb = file_size / 1024
                print(f"   - {filename} ({width}x{height}px, {file_size_kb:.1f} KB)")
        
        print(f"   - images/author_web.jpg (120x120px, {web_file_size_kb:.1f} KB)")
        
        print("\n💡 頭像使用建議：")
        print("   - author_large.jpg (150x150): About頁面使用")
        print("   - author_medium.jpg (120x120): 側邊欄使用")
        print("   - author_web.jpg (120x120): 通用網站頭像")
        print("   - author_small.jpg (80x80): 評論區使用")
        print("   - author_navbar.jpg (60x60): 導航欄使用")
        
        # 檢查原始文件大小
        original_size = os.path.getsize(avatar_path)
        original_size_kb = original_size / 1024
        print(f"\n📊 頭像文件大小對比：")
        print(f"   原始頭像: {original_size_kb:.1f} KB")
        print(f"   網站頭像: {web_file_size_kb:.1f} KB")
        print(f"   節省空間: {original_size_kb - web_file_size_kb:.1f} KB")
        
    except Exception as e:
        print(f"❌ 處理頭像時發生錯誤: {str(e)}")

def resize_logo_for_web():
    """將logo調整為網頁適合的尺寸"""
    
    # 檢查原始logo是否存在
    original_path = "images/logo.png"
    if not os.path.exists(original_path):
        print("❌ 找不到原始logo文件: images/logo.png")
        return
    
    try:
        # 打開原始logo
        original_logo = Image.open(original_path)
        print(f"✅ 原始logo尺寸: {original_logo.size[0]} x {original_logo.size[1]} 像素")
        
        # 定義網頁使用的尺寸
        web_sizes = {
            "logo_navbar": (180, 180),      # 導航欄logo
            "logo_header": (240, 240),      # 頁面標題logo
            "logo_medium": (120, 120),      # 中等尺寸
            "logo_small": (80, 80),         # 小尺寸
            "favicon": (64, 64),            # favicon
            "favicon_small": (32, 32)       # 小favicon
        }
        
        print("\n🔄 正在生成不同尺寸的logo...")
        
        # 為每個尺寸生成logo
        for size_name, (width, height) in web_sizes.items():
            # 調整尺寸，保持寬高比
            resized_logo = original_logo.resize((width, height), Image.Resampling.LANCZOS)
            
            # 生成文件名
            filename = f"images/logo_{size_name}.png"
            
            # 保存調整後的logo
            resized_logo.save(filename, "PNG", optimize=True)
            
            # 獲取文件大小
            file_size = os.path.getsize(filename)
            file_size_kb = file_size / 1024
            
            print(f"✅ {size_name}: {width}x{height}px - {file_size_kb:.1f} KB")
        
        # 創建一個專門用於網站的標準logo (替換原始文件)
        web_logo = original_logo.resize((200, 200), Image.Resampling.LANCZOS)
        web_logo.save("images/logo_web.png", "PNG", optimize=True)
        
        # 獲取文件大小
        web_file_size = os.path.getsize("images/logo_web.png")
        web_file_size_kb = web_file_size / 1024
        
        print(f"\n✅ 網站標準logo: 200x200px - {web_file_size_kb:.1f} KB")
        
        print("\n📁 生成的logo文件：")
        for size_name, (width, height) in web_sizes.items():
            filename = f"images/logo_{size_name}.png"
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                file_size_kb = file_size / 1024
                print(f"   - {filename} ({width}x{height}px, {file_size_kb:.1f} KB)")
        
        print(f"   - images/logo_web.png (200x200px, {web_file_size_kb:.1f} KB)")
        
        print("\n💡 Logo使用建議：")
        print("   - logo_navbar.png (180x180): 導航欄使用")
        print("   - logo_header.png (240x240): 頁面標題使用")
        print("   - logo_web.png (200x200): 通用網站logo")
        print("   - favicon.png (64x64): 瀏覽器標籤頁圖標")
        
        # 檢查原始文件大小
        original_size = os.path.getsize(original_path)
        original_size_kb = original_size / 1024
        print(f"\n📊 Logo文件大小對比：")
        print(f"   原始logo: {original_size_kb:.1f} KB")
        print(f"   網站logo: {web_file_size_kb:.1f} KB")
        print(f"   節省空間: {original_size_kb - web_file_size_kb:.1f} KB")
        
    except Exception as e:
        print(f"❌ 處理logo時發生錯誤: {str(e)}")

def create_favicon():
    """創建favicon.ico文件"""
    try:
        # 打開64x64的logo
        favicon_path = "images/logo_favicon.png"
        if os.path.exists(favicon_path):
            favicon = Image.open(favicon_path)
            
            # 轉換為ICO格式
            ico_path = "images/favicon.ico"
            favicon.save(ico_path, format='ICO', sizes=[(32, 32), (64, 64)])
            
            file_size = os.path.getsize(ico_path)
            file_size_kb = file_size / 1024
            print(f"✅ favicon.ico 已創建: {file_size_kb:.1f} KB")
        else:
            print("⚠️ 找不到favicon.png文件")
            
    except Exception as e:
        print(f"❌ 創建favicon時發生錯誤: {str(e)}")

if __name__ == "__main__":
    print("🎨 圖片尺寸調整器 (Logo + 頭像)")
    print("=" * 50)
    
    # 調整頭像尺寸
    print("🔄 處理頭像圖片...")
    resize_avatar_for_web()
    
    print("\n" + "=" * 50)
    
    # 調整logo尺寸
    print("🔄 處理Logo圖片...")
    resize_logo_for_web()
    
    print("\n" + "=" * 50)
    print("🔄 創建favicon...")
    
    # 創建favicon
    create_favicon()
    
    print("\n🎉 所有網頁尺寸的圖片已生成完成！")
    print("\n💡 現在你可以：")
    print("   1. 使用 author_web.jpg 作為主要頭像")
    print("   2. 使用 logo_web.png 作為主要logo")
    print("   3. 根據不同用途選擇最適合的尺寸")
