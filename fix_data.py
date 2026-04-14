import os
import django

# Fix data.py
data_path = 'chatbot/data.py'
with open(data_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"category": "TVET"', '"category": "TVET / TESDA"')
content = content.replace('"question": "What TVET programs are offered?"', '"question": "What TVET or TESDA programs are offered?"')
content = content.replace('"answer": "SPUS TVET offers Registered', '"answer": "As a fully TESDA-registered training center, SPUS TVET offers Registered')

with open(data_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated data.py with TESDA keywords.")
