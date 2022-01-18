import os
import markdown

class ProjectUtil:

    def get_images():
        items = os.listdir('./suchiblog/static/assets/programming-languages')
        return [ os.path.basename(item) for item in items if '.svg' in item ]

    def to_html(md):
        md = md.replace('\r\n', '\n')
        ending = False
        while md.count('```'):
            if ending:
                md = md.replace('```', '</pre>', 1)
                ending = False
            else:
                ending = True
                pos = int(md.find('```'))+3
                newline = int(md.find('\n', pos))
                prog = md[pos:newline].strip()
                if prog != '':
                    md = md[0:pos] + md[newline::]
                    md = md.replace('```', f'<pre class="code-block code-{prog}">', 1)
                else:
                    md = md.replace('```', '<pre class="code-block">', 1)

        
        md = markdown.markdown(md)
        md = md.replace('<code>', '<span class="highlight-block">')
        md = md.replace('</code>', '</span>')
        return md