#!/usr/bin/env python3
import re
import sys

def md_to_html(md_file, output_file, title):
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Simple markdown to HTML conversion
    html_content = content
    
    # Headers
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    
    # Bold
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    
    # Links
    html_content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html_content)
    
    # List items
    html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^❌ (.+)$', r'<li>❌ \1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^✅ (.+)$', r'<li>✅ \1</li>', html_content, flags=re.MULTILINE)
    
    # Wrap consecutive list items in <ul>
    html_content = re.sub(r'(<li>.*?</li>\n)+', lambda m: '<ul>\n' + m.group(0) + '</ul>\n', html_content, flags=re.DOTALL)
    
    # Paragraphs
    lines = html_content.split('\n')
    result = []
    in_paragraph = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('<') or stripped.startswith('---'):
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            if stripped == '---':
                result.append('<hr>')
            elif stripped:
                result.append(line)
        else:
            if not in_paragraph:
                result.append('<p>')
                in_paragraph = True
            result.append(line)
    
    if in_paragraph:
        result.append('</p>')
    
    html_content = '\n'.join(result)
    
    # Create full HTML document
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Aperioesca</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
            color: #ECEDEE;
            padding: 40px 20px;
            min-height: 100vh;
            line-height: 1.6;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 50px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        h1 {{
            background: linear-gradient(135deg, #FF6B9D 0%, #6FEDD6 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5em;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #6FEDD6;
            font-size: 1.8em;
            margin-top: 40px;
            margin-bottom: 15px;
        }}
        h3 {{
            color: #FF6B9D;
            font-size: 1.3em;
            margin-top: 25px;
            margin-bottom: 10px;
        }}
        p {{
            margin-bottom: 15px;
            color: #D0D0D0;
        }}
        ul {{
            margin: 15px 0 15px 30px;
        }}
        li {{
            margin-bottom: 8px;
            color: #D0D0D0;
        }}
        a {{
            color: #6FEDD6;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: border-color 0.3s;
        }}
        a:hover {{
            border-bottom-color: #6FEDD6;
        }}
        strong {{
            color: #FFFFFF;
        }}
        hr {{
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin: 30px 0;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #A0A0A0;
            font-size: 0.9em;
        }}
        .back-link:hover {{
            color: #6FEDD6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">← Back to Legal Documents</a>
        {html_content}
    </div>
</body>
</html>'''
    
    with open(output_file, 'w') as f:
        f.write(full_html)
    
    print(f"Created {output_file}")

if __name__ == '__main__':
    # Convert privacy.md
    md_to_html(
        '/Users/himaschal/workspace/ashlunar-legal/aperioesca/privacy.md',
        '/Users/himaschal/workspace/ashlunar-legal/aperioesca/privacy.html',
        'Privacy Policy'
    )
    
    # Convert terms.md
    md_to_html(
        '/Users/himaschal/workspace/ashlunar-legal/aperioesca/terms.md',
        '/Users/himaschal/workspace/ashlunar-legal/aperioesca/terms.html',
        'Terms of Service'
    )
