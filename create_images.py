from PIL import Image, ImageDraw
import os

# Create category placeholders
categories = [
    ('gaming', 'Gaming', '#1a1a2e'),
    ('artisan', 'Artisan Accessories', '#2d2d44'),
    ('perfumes', 'Perfumes', '#1f1f3d'),
    ('cosmetics', 'Cosmetics', '#2a1f3d')
]

for slug, name, color in categories:
    img = Image.new('RGB', (400, 300), color)
    img.save(f'c:/Users/mk-tech/OneDrive/Desktop/python/static/images/categories/{slug}.jpg')

# Create product placeholders
products = [
    ('gaming-headset', '#16213e'),
    ('gaming-keyboard', '#1a1a2e'),
    ('gaming-monitor', '#0f3460'),
    ('gaming-mouse', '#1a1a2e'),
    ('gaming-controller', '#533483'),
    ('leather-wallet', '#8B4513'),
    ('artisan-watch', '#FFD700'),
    ('silk-scarf', '#E6E6FA'),
    ('custom-belt', '#8B4513'),
    ('messenger-bag', '#654321'),
    ('perfume-oud', '#4a1942'),
    ('perfume-floral', '#ffc0cb'),
    ('perfume-citrus', '#ffd700'),
    ('perfume-vanilla', '#f5deb3'),
    ('perfume-woody', '#8b4513'),
    ('skincare-set', '#ffe4e1'),
    ('lipstick-set', '#dc143c'),
    ('makeup-palette', '#ff69b4'),
    ('face-mask', '#e6e6fa'),
    ('foundation', '#d2b48c')
]

for slug, color in products:
    img = Image.new('RGB', (400, 400), color)
    img.save(f'c:/Users/mk-tech/OneDrive/Desktop/python/static/images/products/{slug}.jpg')

print('Placeholder images created successfully!')

