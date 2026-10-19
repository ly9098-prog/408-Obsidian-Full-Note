from pathlib import Path
import xml.etree.ElementTree as ET

import yaml
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'CS408-Obsidian-Note-latest/4计算机网络/6 应用层/attachments'
WORK = Path(__file__).parent
SCALE = 2
FONTS = Path('/mnt/c/Windows/Fonts')
INK = '#193142'
BLUE = '#126D9B'
STROKE = '#8FA7B5'


def get_font(size, bold=False, mono=False):
    filename = 'consola.ttf' if mono else ('msyhbd.ttc' if bold else 'msyh.ttc')
    return ImageFont.truetype(str(FONTS / filename), size * SCALE)


for kind in ('request', 'response'):
    request = kind == 'request'
    title = 'HTTP 请求报文' if request else 'HTTP 响应报文'
    stem = 'HTTP请求报文结构图' if request else 'HTTP响应报文结构图'
    image = Image.new('RGB', (1280 * SCALE, 800 * SCALE), 'white')
    draw = ImageDraw.Draw(image)
    nodes = []

    def box(identifier, x, y, width, height, label, fill='white', color=INK,
            size=24, bold=False, mono=False, align='center'):
        draw.rectangle((x * SCALE, y * SCALE, (x + width) * SCALE,
                        (y + height) * SCALE), fill=fill,
                       outline=STROKE, width=2 * SCALE)
        tx = x + width / 2 if align == 'center' else x + 22
        draw.multiline_text(
            (tx * SCALE, (y + height / 2) * SCALE), label,
            font=get_font(size, bold, mono), fill=color,
            anchor='mm' if align == 'center' else 'lm',
            align=align, spacing=8 * SCALE,
        )
        nodes.append({
            'id': identifier, 'label': label, 'type': 'service',
            'bounds': {'x': x, 'y': y, 'width': width, 'height': height},
            'style': {
                'rounded': 0, 'fillColor': fill, 'strokeColor': STROKE,
                'strokeWidth': 2,
                'fontFamily': 'Consolas' if mono else 'Microsoft YaHei',
                'fontSize': size, 'fontColor': color,
                'fontStyle': 1 if bold else 0, 'align': align,
                'verticalAlign': 'middle',
                'spacingLeft': 22 if align == 'left' else 0,
            },
        })

    def text(identifier, x, y, width, height, label, size=24, color=INK,
             bold=False):
        draw.text((x * SCALE, (y + height / 2) * SCALE), label,
                  font=get_font(size, bold), fill=color, anchor='lm')
        nodes.append({
            'id': identifier, 'label': label, 'type': 'text',
            'bounds': {'x': x, 'y': y, 'width': width, 'height': height},
            'style': {
                'fontFamily': 'Microsoft YaHei', 'fontSize': size,
                'fontColor': color, 'fontStyle': 1 if bold else 0,
                'align': 'left', 'verticalAlign': 'middle',
            },
        })

    text('title', 48, 30, 760, 60, title, 36, bold=True)
    text('subtitle', 48, 94, 1160, 40,
         'HTTP/1.1 示例 · 字段按传输顺序排列，宽度不代表字节数', 22, '#526C7A')
    start, main_width, y, height = 240, 928, 160, 88
    if request:
        fields = [
            ('method', 160, '方法\nPOST'), ('sp1', 40, 'SP'),
            ('target', 288, 'URL / 请求目标\n/login'), ('sp2', 40, 'SP'),
            ('version', 288, '版本\nHTTP/1.1'), ('endline', 112, 'CRLF'),
        ]
    else:
        fields = [
            ('version', 288, '版本\nHTTP/1.1'), ('sp1', 40, 'SP'),
            ('status', 160, '状态码\n200'), ('sp2', 40, 'SP'),
            ('reason', 288, '原因短语\nOK'), ('endline', 112, 'CRLF'),
        ]
    text('line-label', 48, y, 180, height,
         '请求行' if request else '状态行', 28, BLUE, True)
    x = start
    for identifier, width, label in fields:
        special = identifier.startswith('sp') or identifier == 'endline'
        box(identifier, x, y, width, height, label,
            '#EAF2F7' if special else '#E0F1FC',
            BLUE if special else INK,
            17 if identifier.startswith('sp') else 24, bold=not special)
        x += width

    headers = [
        'Host: example.com',
        'Content-Type: application/x-www-form-urlencoded',
        'Content-Length: 10',
    ] if request else ['Content-Type: text/html', 'Content-Length: 14']
    text('headers-label', 48, y + height, 180, len(headers) * 64,
         '首部行', 28, BLUE, True)
    for index, label in enumerate(headers):
        yy = y + height + index * 64
        box('header' + str(index), start, yy, main_width - 112, 64,
            label, '#F7FAFC', size=22, mono=True, align='left')
        box('header-end' + str(index), start + main_width - 112, yy,
            112, 64, 'CRLF', '#EAF2F7', BLUE, 22)

    blank_y = y + height + len(headers) * 64
    text('blank-label', 48, blank_y, 180, 64, '空行', 28, '#A76B0A', True)
    box('empty-line', start, blank_y, main_width, 64,
        'CRLF', '#FFF0CD', '#8D5900', 26, True)
    body = 'name=alice' if request else '<h1>Hello</h1>'
    body_y = blank_y + 64
    text('body-label', 48, body_y, 180, 104, '实体主体', 28, '#2D7350', True)
    box('body', start, body_y, main_width, 104, body,
        '#EAF6EF', '#245C40', 30, mono=True)
    text('bytes', start, body_y + 108, main_width, 36,
         ('10' if request else '14') + ' B；本例含主体，实际报文的主体可为空。',
         21, '#526C7A')
    text('legend1', 48, 684, 1160, 36,
         'SP = 空格（1 B）     CRLF = 回车换行（2 B）', 24, BLUE, True)
    text('legend2', 48, 728, 1160, 36,
         '识图重点：起始行 → 若干首部行 → 空行 → 实体主体；空行标记首部结束。',
         22, '#526C7A')

    image.save(OUTPUT / (stem + '.png'), dpi=(300, 300))
    spec = {
        'meta': {'profile': 'default', 'theme': 'tech-blue',
                 'layout': 'vertical', 'canvas': '1280x800',
                 'title': title, 'source': 'generated'},
        'nodes': nodes, 'edges': [],
    }
    (WORK / (stem + '.spec.yaml')).write_text(
        yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding='utf-8')
    # Native cells preserve field geometry for later diagram editing.
    mxfile = ET.Element('mxfile', {'host': 'app.diagrams.net'})
    diagram = ET.SubElement(mxfile, 'diagram', {'id': kind, 'name': title})
    model = ET.SubElement(diagram, 'mxGraphModel', {
        'grid': '1', 'gridSize': '8', 'page': '1',
        'pageWidth': '1280', 'pageHeight': '800', 'background': '#FFFFFF',
    })
    graph = ET.SubElement(model, 'root')
    ET.SubElement(graph, 'mxCell', {'id': '0'})
    ET.SubElement(graph, 'mxCell', {'id': '1', 'parent': '0'})
    for node in nodes:
        style = dict(node['style'])
        style.update({'whiteSpace': 'wrap', 'html': 0})
        if node['type'] == 'text':
            style.update({'fillColor': 'none', 'strokeColor': 'none'})
        cell = ET.SubElement(graph, 'mxCell', {
            'id': node['id'], 'value': node['label'], 'vertex': '1',
            'parent': '1',
            'style': ';'.join(str(k) + '=' + str(v) for k, v in style.items()) + ';',
        })
        ET.SubElement(cell, 'mxGeometry', {
            **{k: str(v) for k, v in node['bounds'].items()}, 'as': 'geometry',
        })
    ET.indent(mxfile)
    ET.ElementTree(mxfile).write(
        OUTPUT / (stem + '.drawio'), encoding='utf-8', xml_declaration=True)
    print('Created', OUTPUT / (stem + '.png'))
