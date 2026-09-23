import re
import json

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const questions = (\[[\s\S]*?\n\]);', html)
if m:
    raw_js = m.group(1)
    clean_js = re.sub(r'(\b(?:q|options|answer)\b)\s*:', r'"\1":', raw_js)
    clean_js = re.sub(r',\s*([\]}])', r'\1', clean_js)
    try:
        data = json.loads(clean_js)
        print('Parsed', len(data), 'voice questions!')
        for i, item in enumerate(data):
            item['id'] = i + 1
            item['category'] = 'Active & Passive Voice'
        with open('public/voice_questions.json', 'w', encoding='utf-8') as out:
            json.dump(data, out, indent=2, ensure_ascii=False)
        print('Saved to public/voice_questions.json')
    except Exception as e:
        print('Parse error:', e)
