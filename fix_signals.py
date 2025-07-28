import re

# Read the signals file
with open('apps/notifications/signals.py', 'r') as f:
    content = f.read()

# Replace all get_full_name() with get_full_name (property access)
content = re.sub(r'\.get_full_name\(\)', '.get_full_name', content)

# Write back to file
with open('apps/notifications/signals.py', 'w') as f:
    f.write(content)

print('Fixed all get_full_name() calls')
