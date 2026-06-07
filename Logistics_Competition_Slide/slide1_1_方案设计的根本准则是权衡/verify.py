from html.parser import HTMLParser
import re

class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.stack = []
        self.void = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def handle_starttag(self, t, a):
        if t not in self.void:
            self.stack.append(t)
    def handle_endtag(self, t):
        if t in self.void:
            return
        if self.stack and self.stack[-1] == t:
            self.stack.pop()
        else:
            self.errors.append(f'Unexpected </{t}>')

with open('index.html', encoding='utf-8') as f:
    c = f.read()

chk = Check()
chk.feed(c)
if chk.errors:
    for e in chk.errors:
        print('ERROR:', e)
else:
    slides = len(re.findall(r'<textarea\s+data-template>', c))
    panels = c.count('class="panel"')
    cards = c.count('class="card ')
    fragments = c.count('class="fragment')
    tags = c.count('不推荐')
    print(f'OK - {len(c)} bytes, {slides} slides')
    print(f'panel={panels}  card={cards}  fragment={fragments}')
    print(f'不推荐 tags: {tags}')
