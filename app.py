import csv
import os
from datetime import datetime
from urllib.parse import quote

from flask import Flask, render_template, abort, request, jsonify

app = Flask(__name__)

# ============================================
# WhatsApp — destino de todos os CTAs verdes e do ícone flutuante.
# Para trocar o número, altere APENAS a constante abaixo.
# Formato: DDI + DDD + número, somente dígitos.
# ============================================
WHATSAPP_NUMBER = "5541999908400"
WHATSAPP_MESSAGE = ("Olá, estou no site da Unitrier. "
                    "Gostaria de saber mais informações sobre o serviço de vocês")

# ============================================
# Leads captados pelo popup que antecede o WhatsApp.
# Gravados fora de static/ para que o CSV não fique acessível publicamente.
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_FILE = os.path.join(BASE_DIR, "data", "leads.csv")
LEADS_FIELDS = ["data_hora", "nome", "email", "telefone", "empresa", "origem"]

# ============================================
# Blog — artigos (ordenados do mais recente para o mais antigo)
# Para publicar um novo post: adicione um item aqui e crie o
# template correspondente em templates/blog/<slug>.html
# (herdando de "blog/_base_post.html").
# ============================================
BLOG_POSTS = [
    {
        "slug": "alto-indice-de-endividamento",
        "title": "Por que o alto índice de endividamento pode quebrar uma empresa?",
        "excerpt": "Recursos externos mal planejados aumentam o risco de insolvência. "
                   "Entenda os fatores que elevam o endividamento e como reverter esse "
                   "cenário antes que ele comprometa o seu negócio.",
        "category": "Financeiro",
        "date_label": "11 de abril de 2025",
        "image": "images/financeiro/gestão financeira.png",
        "template": "blog/alto-indice-de-endividamento.html",
        "tags": ["Gestão Financeira", "Endividamento", "Capital de Giro", "Planejamento Financeiro"],
    },
    {
        "slug": "comportamento-do-consumidor",
        "title": "Comportamento do consumidor: uma análise simples",
        "excerpt": "Conveniência, sustentabilidade e uso de dados estão redesenhando a "
                   "jornada de compra. Veja as tendências e como o seu supermercado pode "
                   "se adaptar.",
        "category": "Varejo",
        "author": "Kevin Napoleão",
        "date_label": "28 de março de 2025",
        "image": "images/comercial/gestão de categorias.png",
        "template": "blog/comportamento-do-consumidor.html",
        "tags": ["Comportamento do Consumidor", "Experiência de Compra", "Omnichannel", "Dados no Varejo"],
    },
    {
        "slug": "prevencao-de-perdas-em-supermercados",
        "title": "Estratégias eficazes para prevenção de perdas em supermercados",
        "excerpt": "Quebras, vencimentos, furtos e erros operacionais corroem o resultado. "
                   "Veja como integrar pessoas, processos e tecnologia para proteger o lucro "
                   "do seu supermercado.",
        "category": "Prevenção de Perdas",
        "date_label": "12 de março de 2025",
        "image": "images/estoque/v191_811.png",
        "template": "blog/prevencao-de-perdas-em-supermercados.html",
        "tags": ["Prevenção de Perdas", "Gestão de Estoque", "Tecnologia no Varejo",
                 "Treinamento de Equipe", "Eficiência Operacional"],
    },
]

@app.context_processor
def inject_whatsapp():
    """Disponibiliza o link do WhatsApp para todos os templates."""
    return {
        "whatsapp_number": WHATSAPP_NUMBER,
        "whatsapp_message": WHATSAPP_MESSAGE,
        "whatsapp_url": f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(WHATSAPP_MESSAGE)}",
    }


# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quem-somos')
def quem_somos():
    return render_template('quem-somos.html')

@app.route('/servicos/comercial')
def comercial():
    return render_template('comercial.html')

@app.route('/servicos/estoque')
def estoque():
    return render_template('estoque.html')

@app.route('/servicos/financeiro')
def financeiro():
    return render_template('financeiro.html')

@app.route('/servicos/pessoal-operacao')
def pessoal_operacao():
    return render_template('pessoal-operacao.html')

@app.route('/servicos/estrategico')
def estrategico():
    return render_template('estrategico.html')

@app.route('/cases')
def cases():
    return render_template('cases-sucesso.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/diagnostico-360')
def diagnostico_360():
    return render_template('diagnostico-360.html')

@app.route('/produtos/shelf')
def shelf():
    return render_template('software-shelf.html')

@app.route('/blog')
def blog():
    return render_template('blog.html', posts=BLOG_POSTS)

@app.route('/blog/<slug>')
def blog_post(slug):
    post = next((p for p in BLOG_POSTS if p['slug'] == slug), None)
    if post is None:
        abort(404)
    return render_template(post['template'], post=post, posts=BLOG_POSTS)

@app.route('/api/lead', methods=['POST'])
def api_lead():
    """Recebe os dados do popup de captação e grava em data/leads.csv.

    Ponto de integração: para enviar o lead a um CRM (RD Station, HubSpot,
    webhook etc.), faça a chamada logo após a gravação no CSV.
    """
    dados = request.get_json(silent=True) or request.form
    lead = {campo: (dados.get(campo) or "").strip()
            for campo in ("nome", "email", "telefone", "empresa")}

    faltando = [campo for campo, valor in lead.items() if not valor]
    if faltando:
        return jsonify({"ok": False, "campos_faltando": faltando}), 400

    lead["data_hora"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lead["origem"] = (dados.get("origem") or "").strip()

    os.makedirs(os.path.dirname(LEADS_FILE), exist_ok=True)
    arquivo_novo = not os.path.exists(LEADS_FILE)
    # utf-8-sig para que os acentos apareçam corretamente ao abrir no Excel
    with open(LEADS_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=LEADS_FIELDS)
        if arquivo_novo:
            writer.writeheader()
        writer.writerow(lead)

    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5008, debug=True)
