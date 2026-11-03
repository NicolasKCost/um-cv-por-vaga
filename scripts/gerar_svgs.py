"""Gera os SVGs animados do README (mesmo estilo terminal do perfil NicolasKCost).

Uso: python scripts/gerar_svgs.py   (escreve em docs/svg/)
"""
import os
from html import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "svg")
os.makedirs(OUT, exist_ok=True)

FONT = "Consolas, 'SFMono-Regular', 'DejaVu Sans Mono', 'Liberation Mono', 'Courier New', monospace"
BG, BAR, BORDER = "#0a0e14", "#161b22", "#1f3b2d"
GREEN, GREEN_DIM, CYAN, YELLOW, WHITE, GREY, BLUE = (
    "#00ff9c", "#1f8a5b", "#56d4ff", "#e3b341", "#e6edf3", "#7d8590", "#4c8dff")


def e(s):
    return escape(s, quote=True)


def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
    print("ok", name)


def style(extra=""):
    return f"""<style>
    text {{ font-family: {FONT}; }}
    .blink {{ animation: blink 1s step-end infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    .pulse {{ animation: pulse 1.8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: .35; transform: scale(.75); }} }}
    {extra}
  </style>"""


def window(w, h, title):
    return f"""<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
  <path d="M1 11 a10 10 0 0 1 10 -10 H{w-11} a10 10 0 0 1 10 10 V34 H1 Z" fill="{BAR}"/>
  <line x1="1" y1="34" x2="{w-1}" y2="34" stroke="{BORDER}"/>
  <circle cx="20" cy="17.5" r="6" fill="#ff5f56"/><circle cx="40" cy="17.5" r="6" fill="#ffbd2e"/><circle cx="60" cy="17.5" r="6" fill="#27c93f"/>
  <text x="{w/2}" y="22" text-anchor="middle" font-size="13" fill="{GREY}">{e(title)}</text>"""


def janela(t0, t1, T, nome):
    """keyframes: invisível até t0, visível até t1, some no fim do ciclo."""
    pc = lambda s: f"{100 * s / T:.3f}%"
    return f"@keyframes {nome} {{ 0%,{pc(t0)} {{ opacity: 0; }} {pc(t0+0.15)},{pc(t1)} {{ opacity: 1; }} {pc(t1+0.3)},100% {{ opacity: 0; }} }}"


# ---------------------------------------------------------------- cabeçalho
def hero():
    W, H, T = 900, 300, 14.0
    pc = lambda s: f"{100 * s / T:.3f}%"
    css = []
    cmd = "./adaptar-cv --vaga anuncio.txt"
    cw = 9.0
    n = len(cmd)
    css.append(f"@keyframes tp {{ 0%,{pc(0.3)} {{ clip-path: inset(0 100% 0 0); }} {pc(0.3+n*0.04)},{pc(T-0.4)} {{ clip-path: inset(0 0 0 0); opacity: 1; }} 100% {{ opacity: 0; }} }}")
    passos = [
        ("CV lido", "experiência, formação e competências"),
        ("vaga analisada", "requisitos e palavras-chave"),
        ("compatibilidade calculada", "o que encaixa e o que falta"),
        ("CV reescrito", "só com dados reais do candidato"),
        ("candidatura enviada", "pelo Gmail do próprio utilizador"),
    ]
    linhas = []
    for i, (a, b) in enumerate(passos):
        t = 2.0 + i * 1.1
        css.append(janela(t, T - 0.6, T, f"s{i}"))
        linhas.append(f'<text x="30" y="{150 + i*24}" font-size="14" style="opacity:0;animation:s{i} {T}s infinite" xml:space="preserve">'
                      f'<tspan fill="{GREEN}">✓</tspan> <tspan fill="{WHITE}">{e(a)}</tspan>  <tspan fill="{GREY}">— {e(b)}</tspan></text>')
    # documentos à direita: vaga + CV -> CV adaptado
    dx = 610
    css.append(f".beam {{ animation: beam 2.2s ease-in-out infinite; }} @keyframes beam {{ 0% {{ transform: translateY(0); opacity: 0; }} 15%,85% {{ opacity: .9; }} 100% {{ transform: translateY(96px); opacity: 0; }} }}")
    css.append(".flow { stroke-dasharray: 4 6; animation: flow 1s linear infinite; } @keyframes flow { to { stroke-dashoffset: -20; } }")
    css.append(janela(7.6, T - 0.6, T, "ok"))

    def doc(x, y, titulo, cor, linhas_doc):
        r = [f'<rect x="{x}" y="{y}" width="110" height="130" rx="6" fill="#0f1720" stroke="{cor}" stroke-width="1.5"/>',
             f'<text x="{x+10}" y="{y+20}" font-size="12" fill="{cor}">{e(titulo)}</text>']
        for k, w in enumerate(linhas_doc):
            r.append(f'<rect x="{x+10}" y="{y+34 + k*14}" width="{w}" height="6" rx="2" fill="{GREY}" opacity=".5"/>')
        return "".join(r)

    docs = (doc(dx, 60, "vaga", CYAN, [80, 60, 86, 50, 70, 40]) +
            doc(dx + 150, 60, "CV", YELLOW, [70, 88, 54, 80, 62, 76]))
    adapt = f"""<g style="opacity:0;animation:ok {T}s infinite">
    <rect x="{dx+60}" y="215" width="200" height="54" rx="6" fill="#0f2a1e" stroke="{GREEN}" stroke-width="1.5"/>
    <text x="{dx+160}" y="238" text-anchor="middle" font-size="13" font-weight="bold" fill="{GREEN}">CV adaptado à vaga</text>
    <text x="{dx+160}" y="257" text-anchor="middle" font-size="11.5" fill="{GREY}">sem inventar dados</text></g>"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {style(" ".join(css))}
  {window(W, H, "umcvporvaga.pt — em produção")}
  <text x="30" y="78" font-size="30" font-weight="bold" fill="{WHITE}">Um CV por Vaga</text>
  <circle class="pulse" cx="300" cy="68" r="5" fill="{GREEN}"/><text x="312" y="73" font-size="13" fill="{GREEN}">online</text>
  <text x="30" y="102" font-size="13.5" fill="{GREY}">SaaS que adapta o CV a cada vaga com IA e envia a candidatura</text>
  <text x="30" y="128" font-size="14"><tspan fill="{GREEN}">$</tspan></text>
  <text x="46" y="128" font-size="14" fill="{WHITE}" textLength="{n*cw}" lengthAdjust="spacingAndGlyphs" style="clip-path: inset(0 100% 0 0); animation: tp {T}s infinite steps({n})">{e(cmd)}</text>
  {"".join(linhas)}
  <line x1="{dx-26}" y1="50" x2="{dx-26}" y2="{H-20}" stroke="{BORDER}"/>
  {docs}
  <g clip-path="url(#dc)"><rect class="beam" x="{dx}" y="88" width="260" height="3" fill="{GREEN}"/></g>
  <defs><clipPath id="dc"><rect x="{dx}" y="60" width="260" height="130"/></clipPath></defs>
  <path class="flow" d="M{dx+55} 192 V205 H{dx+160} V213 M{dx+205} 192 V205 H{dx+160}" fill="none" stroke="{GREEN_DIM}" stroke-width="2"/>
  {adapt}
</svg>"""
    write("hero.svg", svg)


# ---------------------------------------------------------------- arquitetura com pacotes a circular
def arquitetura():
    W, H = 900, 330
    nos = {
        "user": (40, 140, 130, "Utilizador", "browser · telemóvel", WHITE),
        "php": (300, 140, 150, "Backend PHP", "regras · validação", GREEN),
        "ia": (600, 50, 180, "Gemini API", "+ alternativa se falhar", CYAN),
        "db": (600, 140, 180, "MySQL", "utilizadores · créditos", YELLOW),
        "mail": (600, 230, 180, "Gmail API · Brevo", "envio · DKIM/DMARC", BLUE),
        "stripe": (300, 222, 150, "Stripe", "checkout · webhooks", "#c678dd"),
    }
    caixas = []
    for k, (x, y, w, t, s, c) in nos.items():
        caixas.append(f'<rect x="{x}" y="{y}" width="{w}" height="52" rx="8" fill="#0f1720" stroke="{c}" stroke-width="1.6"/>'
                      f'<text x="{x+w/2}" y="{y+22}" text-anchor="middle" font-size="14" font-weight="bold" fill="{c}">{e(t)}</text>'
                      f'<text x="{x+w/2}" y="{y+40}" text-anchor="middle" font-size="11" fill="{GREY}">{e(s)}</text>')

    def mid(k, lado):
        x, y, w = nos[k][0], nos[k][1], nos[k][2]
        return {"l": (x, y + 26), "r": (x + w, y + 26), "t": (x + w / 2, y), "b": (x + w / 2, y + 52)}[lado]

    ligacoes = [("user", "r", "php", "l", 0.0), ("php", "r", "ia", "l", 0.6), ("php", "r", "db", "l", 1.2),
                ("php", "r", "mail", "l", 1.8), ("php", "b", "stripe", "t", 2.4)]
    paths, pacotes, css = [], [], []
    for i, (a, la, b, lb, d) in enumerate(ligacoes):
        (x1, y1), (x2, y2) = mid(a, la), mid(b, lb)
        if la == "r" and lb == "l" and y1 != y2:
            mx = (x1 + x2) / 2
            dpath = f"M{x1} {y1} H{mx} V{y2} H{x2}"
        else:
            dpath = f"M{x1} {y1} L{x2} {y2}"
        paths.append(f'<path d="{dpath}" fill="none" stroke="{GREEN_DIM}" stroke-width="1.6" stroke-dasharray="4 5"/>')
        for k in range(2):
            pacotes.append(f'<circle r="4" fill="{GREEN}" style="offset-path: path(\'{dpath}\'); animation: ida 2.4s linear infinite; animation-delay: {d + k*1.2:.1f}s; opacity:0"/>')
    css.append("@keyframes ida { 0% { offset-distance: 0%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { offset-distance: 100%; opacity: 0; } }")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {style(" ".join(css))}
  {window(W, H, "arquitetura — como os pedidos circulam")}
  {"".join(paths)}
  {"".join(pacotes)}
  {"".join(caixas)}
  <text x="40" y="{H-16}" font-size="12" fill="{GREY}">A IA nunca fala diretamente com o utilizador: o PHP valida cada resposta antes de a mostrar.</text>
</svg>"""
    write("arquitetura.svg", svg)


# ---------------------------------------------------------------- pipeline de publicação (loop)
def deploy():
    W, H, T = 900, 230, 12.0
    pc = lambda s: f"{100 * s / T:.3f}%"
    etapas = [("testes", "testes automáticos"), ("backup", "cópia de segurança"),
              ("sync", "ficheiros + migrações"), ("verificar", "o site responde por HTTP")]
    css, partes = [], []
    x0, larg, gap, y = 30, 190, 22, 92
    for i, (nome, desc) in enumerate(etapas):
        x = x0 + i * (larg + gap)
        t0, t1 = 0.6 + i * 1.8, 0.6 + i * 1.8 + 1.5
        css.append(f"@keyframes b{i} {{ 0%,{pc(t0)} {{ transform: scaleX(0); }} {pc(t1)},{pc(T-0.5)} {{ transform: scaleX(1); }} 100% {{ transform: scaleX(0); }} }}")
        css.append(f"@keyframes c{i} {{ 0%,{pc(t1)} {{ stroke: #1f3b2d; }} {pc(t1+0.1)},{pc(T-0.5)} {{ stroke: #00ff9c; }} 100% {{ stroke: #1f3b2d; }} }}")
        css.append(janela(t1, T - 0.5, T, f"k{i}"))
        css.append(f"@keyframes r{i} {{ 0%,{pc(t0)} {{ opacity: 0; }} {pc(t0+0.05)},{pc(t1)} {{ opacity: 1; }} {pc(t1+0.05)},100% {{ opacity: 0; }} }}")
        partes.append(f"""<rect x="{x}" y="{y-34}" width="{larg}" height="92" rx="8" fill="#0f1720" stroke-width="1.6" style="animation: c{i} {T}s infinite"/>
    <text x="{x+14}" y="{y-10}" font-size="12" fill="{GREY}">{i+1:02d}</text>
    <text x="{x+40}" y="{y-10}" font-size="15" font-weight="bold" fill="{WHITE}">{e(nome)}</text>
    <text x="{x+14}" y="{y+12}" font-size="11.5" fill="{GREY}">{e(desc)}</text>
    <rect x="{x+14}" y="{y+26}" width="{larg-28}" height="8" rx="2" fill="#132019"/>
    <rect x="{x+14}" y="{y+26}" width="{larg-28}" height="8" rx="2" fill="{GREEN}" style="transform-box: fill-box; transform-origin: left; animation: b{i} {T}s infinite"/>
    <text x="{x+larg-14}" y="{y-10}" text-anchor="end" font-size="15" fill="{GREEN}" style="opacity:0;animation:k{i} {T}s infinite">✓</text>
    <text x="{x+larg-14}" y="{y-10}" text-anchor="end" font-size="12" fill="{YELLOW}" style="opacity:0;animation:r{i} {T}s infinite">a correr</text>""")
        if i < len(etapas) - 1:
            partes.append(f'<path d="M{x+larg+4} {y+12} l{gap-8} 0 m-5 -4 l5 4 l-5 4" fill="none" stroke="{GREEN_DIM}" stroke-width="1.6"/>')
    fim = 0.6 + len(etapas) * 1.8
    css.append(janela(fim, T - 0.5, T, "fim"))
    css.append(f"@keyframes nao {{ 0%,{pc(0.2)} {{ opacity: 0; }} {pc(0.4)},{pc(fim)} {{ opacity: 1; }} {pc(fim+0.1)},100% {{ opacity: 0; }} }}")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {style(" ".join(css))}
  {window(W, H, "publicação — cada atualização passa por aqui")}
  {"".join(partes)}
  <text x="30" y="{H-24}" font-size="14" style="opacity:0;animation:nao {T}s infinite" fill="{GREY}">se um teste falhar, a publicação para aqui e nada chega ao site</text>
  <text x="30" y="{H-24}" font-size="14" style="opacity:0;animation:fim {T}s infinite"><tspan fill="{GREEN}">✓ em produção</tspan><tspan fill="{WHITE}"> → umcvporvaga.pt </tspan><tspan class="blink" fill="{GREEN}">█</tspan></text>
</svg>"""
    write("deploy.svg", svg)


if __name__ == "__main__":
    hero()
    arquitetura()
    deploy()
