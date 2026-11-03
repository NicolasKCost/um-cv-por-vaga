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


# ---------------------------------------------------------------- cabeçalho (visual azul do site)
SANS = "-apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
AZUL, AZUL_E, AZUL_L, TINTA, MUT, LINHA, FUNDO = "#1d4ed8", "#1e3a8a", "#eff6ff", "#111827", "#6b7280", "#e5e7eb", "#f6f7fb"
OK, OK_L, AVISO, AVISO_L = "#047857", "#ecfdf5", "#b45309", "#fffbeb"


def hero():
    W, H, T = 900, 320, 12.0
    pc = lambda s: f"{100 * s / T:.3f}%"
    css = [f"text {{ font-family: {SANS}; }}",
           ".pulse { animation: pulse 1.8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }",
           "@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: .35; } }"]

    def aparece(nome, t, dy=6):
        css.append(f"@keyframes {nome} {{ 0%,{pc(t)} {{ opacity: 0; transform: translateY({dy}px); }} {pc(t+0.4)},{pc(T-0.6)} {{ opacity: 1; transform: none; }} {pc(T-0.2)},100% {{ opacity: 0; }} }}")
        return f"opacity:0; animation: {nome} {T}s infinite"

    # cartão da direita: anúncio -> análise -> CV adaptado
    cx, cy, cw = 500, 34, 370
    css.append(f"@keyframes barra {{ 0%,{pc(2.2)} {{ transform: scaleX(0); }} {pc(3.8)},{pc(T-0.6)} {{ transform: scaleX(.82); }} {pc(T-0.2)},100% {{ transform: scaleX(0); }} }}")
    css.append(f"@keyframes cont {{ 0%,{pc(2.2)} {{ opacity: 0; }} {pc(2.4)},{pc(T-0.6)} {{ opacity: 1; }} {pc(T-0.2)},100% {{ opacity: 0; }} }}")
    num = []
    for k, v in enumerate(range(0, 83, 6)):
        a = 2.2 + k * 0.11
        b = a + 0.11
        nm = f"n{k}"
        css.append(f"@keyframes {nm} {{ 0%,{pc(a)} {{ opacity: 0; }} {pc(a+0.01)},{pc(b)} {{ opacity: 1; }} {pc(b+0.01)},100% {{ opacity: 0; }} }}")
        num.append(f'<text x="{cx+cw-20}" y="{cy+128}" text-anchor="end" font-size="15" font-weight="700" fill="{OK}" style="opacity:0;animation:{nm} {T}s infinite">{v}%</text>')
    fim_n = 2.2 + len(num) * 0.11
    num.append(f'<text x="{cx+cw-20}" y="{cy+128}" text-anchor="end" font-size="15" font-weight="700" fill="{OK}" style="{aparece("nf", fim_n, 0)}">82%</text>')

    def chip(x, y, txt, cor, fundo, nome, t):
        w = len(txt) * 6.9 + 18
        return (f'<g style="{aparece(nome, t)}"><rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="{fundo}"/>'
                f'<text x="{x+9}" y="{y+16}" font-size="12" font-weight="600" fill="{cor}">{e(txt)}</text></g>', w)

    chips, x = [], cx + 20
    for i, (txt, cor, fundo) in enumerate([("✓ atendimento", OK, OK_L), ("✓ reservas", OK, OK_L), ("falta: inglês", AVISO, AVISO_L)]):
        svg_chip, w = chip(x, cy + 146, txt, cor, fundo, f"ch{i}", 4.0 + i * 0.35)
        chips.append(svg_chip)
        x += w + 8
    card = f"""
  <rect x="{cx}" y="{cy}" width="{cw}" height="{H-68}" rx="14" fill="#ffffff" stroke="{LINHA}"/>
  <rect x="{cx+20}" y="{cy+18}" width="132" height="22" rx="11" fill="{FUNDO}"/>
  <text x="{cx+30}" y="{cy+33}" font-size="11" font-weight="700" fill="{MUT}" letter-spacing=".5">EXEMPLO DE ANÚNCIO</text>
  <text x="{cx+cw-20}" y="{cy+33}" text-anchor="end" font-size="12" fill="{MUT}">Hotel · Cascais</text>
  <text x="{cx+20}" y="{cy+66}" font-size="17" font-weight="700" fill="{TINTA}">Rececionista de Hotel</text>
  <rect x="{cx+20}" y="{cy+80}" width="300" height="7" rx="3" fill="{LINHA}"/><rect x="{cx+20}" y="{cy+94}" width="250" height="7" rx="3" fill="{LINHA}"/>
  <g style="opacity:0;animation:cont {T}s infinite">
    <text x="{cx+20}" y="{cy+128}" font-size="13" font-weight="600" fill="{TINTA}">Compatibilidade do teu CV</text>
  </g>
  {"".join(num)}
  <rect x="{cx+20}" y="{cy+136}" width="{cw-40}" height="0" fill="none"/>
  {"".join(chips)}
  <rect x="{cx+20}" y="{cy+182}" width="{cw-40}" height="8" rx="4" fill="{LINHA}"/>
  <rect x="{cx+20}" y="{cy+182}" width="{cw-40}" height="8" rx="4" fill="{OK}" style="transform-box: fill-box; transform-origin: left; animation: barra {T}s infinite"/>
  <g style="{aparece("bt", 6.0)}">
    <rect x="{cx+20}" y="{cy+204}" width="{cw-40}" height="40" rx="10" fill="{AZUL}"/>
    <text x="{cx+cw/2}" y="{cy+229}" text-anchor="middle" font-size="14" font-weight="700" fill="#ffffff">✓ CV adaptado — sem inventar dados</text>
  </g>"""
    passos = ["Cola o anúncio da vaga", "Vê o que encaixa e o que falta", "Recebe o CV reescrito para a vaga", "Envia pelo teu Gmail"]
    lista = "".join(
        f'<g style="{aparece(f"p{i}", 0.6 + i*0.5)}"><circle cx="44" cy="{178 + i*27}" r="10" fill="{AZUL_L}"/>'
        f'<text x="44" y="{182 + i*27}" text-anchor="middle" font-size="11" font-weight="700" fill="{AZUL}">{i+1}</text>'
        f'<text x="64" y="{183 + i*27}" font-size="14" fill="{TINTA}">{e(t)}</text></g>' for i, t in enumerate(passos))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <style>{" ".join(css)}</style>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{FUNDO}" stroke="{LINHA}" stroke-width="2"/>
  <rect x="34" y="36" width="24" height="30" rx="5" fill="{AZUL}"/><rect x="40" y="44" width="12" height="3" rx="1.5" fill="#ffffff"/><rect x="40" y="51" width="12" height="3" rx="1.5" fill="#ffffff"/><rect x="40" y="58" width="8" height="3" rx="1.5" fill="#ffffff"/>
  <text x="66" y="58" font-size="20" font-weight="800" fill="{TINTA}">um<tspan fill="{AZUL}">cv</tspan>porvaga</text>
  <circle class="pulse" cx="232" cy="51" r="4.5" fill="#16a34a"/><text x="242" y="55" font-size="12.5" fill="{OK}" font-weight="600">online</text>
  <text x="34" y="110" font-size="27" font-weight="800" fill="{TINTA}">O teu CV adaptado a</text>
  <text x="34" y="143" font-size="27" font-weight="800" fill="{AZUL}">cada vaga, em 1 minuto.</text>
  {lista}
  <text x="34" y="{H-22}" font-size="12.5" fill="{MUT}">umcvporvaga.pt · PHP · JavaScript · MySQL · Gemini · Stripe</text>
  {card}
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
