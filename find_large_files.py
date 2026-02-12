import os

root_dir = r"d:\2025 - S2\HTTMDT\E-Web-Project\frontend\src"
over_100 = []

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith((".jsx", ".js")):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) > 100:
                        over_100.append((len(lines), filepath))
            except Exception as e:
                pass

over_100.sort(key=lambda x: x[0], reverse=True)
for count, path in over_100:
    print(f"{count} : {path}")
