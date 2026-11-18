from urllib.parse import quote
from flask import Flask, render_template, request
import os
import json
import smtplib
import ssl
from email.message import EmailMessage

app = Flask(__name__)

WHATSAPP_NUMBER = "5511927206740"
CONTACT_EMAIL = "contato@livizsoftware.com.br"

# Clientes que usam sistemas da Liviz no dia a dia (telas reais; painéis internos com dados de exemplo).
CLIENTS = [
    {
        "slug": "gaucha-lanches",
        "name": "Gaúcha Lanches",
        "category": "Lanchonete · Cardápio digital personalizado",
        "description": "Cardápio digital com a identidade da Gaúcha, pedidos pelo WhatsApp com adicionais, central de pedidos com comanda impressa e taxa de entrega calculada pelo endereço.",
        "logo": "img/clientes/gaucha-lanches-logo.png", "logo_bg": "#1a0d08",
        "link": "https://gestao.livizsoftware.com.br/c/gaucha-lanches", "link_label": "Ver o cardápio no ar",
        "features": ["Cardápio digital com a marca da casa", "Lanches com adicionais e observações", "Central de pedidos em tempo real",
                     "Comanda na impressora térmica, até pelo celular", "Taxa de entrega calculada pela distância", "Estoque de insumos e fechamento do dia"],
        "gallery": [("img/clientes/gaucha-lanches/tela-01.webp", "Cardápio digital no computador"),
                    ("img/clientes/gaucha-lanches/tela-02.webp", "Lanches com foto, preço e adicionais"),
                    ("img/clientes/gaucha-lanches/tela-03.webp", "No celular do cliente", "m")],
    },
    {
        "slug": "brumas-pizzaria",
        "name": "Bruma's Pizzaria",
        "category": "Pizzaria delivery · Montagem de pizza",
        "description": "Cardápio digital em que o cliente monta a pizza (meio a meio, bordas e adicionais), central de pedidos, comanda pelo celular e taxa de entrega por distância.",
        "logo": "img/clientes/brumas-pizzaria-logo.png", "logo_bg": "#14110e",
        "link": "https://gestao.livizsoftware.com.br/c/brumas-pizzaria", "link_label": "Ver o cardápio no ar",
        "features": ["Monte sua pizza: sabores, meio a meio, bordas", "Cardápio escuro e dourado com a marca", "Central de pedidos e fechamento diário",
                     "Comanda na impressora Bluetooth pelo celular", "Taxa de entrega por distância", "Manual de uso em PDF para a equipe"],
        "gallery": [("img/clientes/brumas-pizzaria/tela-01.webp", "Abertura do cardápio com a marca"),
                    ("img/clientes/brumas-pizzaria/tela-02.webp", "Sabores com ingredientes e preços"),
                    ("img/clientes/brumas-pizzaria/tela-03.webp", "Cardápio no celular", "m"),
                    ("img/clientes/brumas-pizzaria/tela-04.webp", "Painel de pedidos e cardápio", "c")],
    },
    {
        "slug": "brisa-burguers",
        "name": "Brisa Burguer's",
        "category": "Hamburgueria delivery · Cardápio personalizado",
        "description": "Cardápio preto e dourado com o lanche em destaque no topo, combos com pagamento no Pix, pedido direto no WhatsApp e cálculo da taxa de entrega.",
        "logo": "img/clientes/brisa-burguers-logo.png", "logo_bg": "#0b0b0b",
        "link": "https://gestao.livizsoftware.com.br/c/brisa-burguers", "link_label": "Ver o cardápio no ar",
        "features": ["Visual exclusivo com a marca", "Lanches artesanais com fotos inteiras", "Combos com pagamento no Pix",
                     "Pedido pronto no WhatsApp da loja", "Taxa de entrega pelo endereço", "Painel de pedidos e relatórios"],
        "gallery": [("img/clientes/brisa-burguers/tela-01.webp", "Topo com o lanche da casa"),
                    ("img/clientes/brisa-burguers/tela-02.webp", "Lanches e combos"),
                    ("img/clientes/brisa-burguers/tela-03.webp", "No celular", "m")],
    },
    {
        "slug": "consulmed",
        "name": "Consulmed",
        "category": "Faturamento médico · Convênios",
        "description": "Sistema de faturamento para clínicas e médicos: produção, envio aos convênios, glosas e recursos, fechamento mensal por cliente e portal próprio com a marca da Consulmed.",
        "logo": "img/clientes/consulmed-logo.png", "logo_bg": "#ffffff",
        "features": ["Lançamento da produção e importação de planilhas", "Lotes por convênio e previsão de recebimento", "Glosas e recursos com prazos",
                     "Fechamento mensal por clínica e médico", "Portal para clínicas e médicos enviarem documentos", "Acessos por perfil da equipe"],
        "gallery": [("img/clientes/consulmed/tela-01.webp", "Painel do faturamento (dados de exemplo)", "c"),
                    ("img/clientes/consulmed/tela-02.webp", "Portal com a marca da Consulmed")],
    },
    {
        "slug": "am-imoveis",
        "name": "A.M. Imóveis",
        "category": "Imobiliária · Gestão completa e vitrine",
        "description": "Sistema da imobiliária da Amanda Magalhães: CRM de leads, imóveis com fotos, agenda de visitas, locações, contratos em PDF e Word, financiamentos, comissões e vitrine online.",
        "logo": "img/clientes/am-imoveis-logo.png", "logo_bg": "#ffffff",
        "features": ["CRM de leads e funil de vendas", "Imóveis com fotos e ficha em PDF", "Agenda de visitas da equipe",
                     "Locações, recibos e reajustes", "Contratos em PDF e no Word da imobiliária", "Financiamentos, comissões e vitrine pública"],
        "gallery": [("img/clientes/am-imoveis/tela-01.webp", "Painel da imobiliária (dados de exemplo)"),
                    ("img/clientes/am-imoveis/tela-02.webp", "CRM da equipe (dados de exemplo)"),
                    ("img/clientes/am-imoveis/tela-03.webp", "Vitrine de imóveis online"),
                    ("img/clientes/am-imoveis/tela-04.webp", "Vitrine no celular", "m")],
    },
    {
        "slug": "ohana-restaurantes",
        "name": "Ohana Restaurantes",
        "category": "Restaurante e marmitaria · Pedidos do WhatsApp",
        "description": "Sistema sob medida para o Cantinho da Ohana: pedidos que chegam pelo WhatsApp viram comanda organizada, cardápio do dia, entregas por bairro, comanda térmica e fechamento.",
        "logo": "img/clientes/ohana-logo.png", "logo_bg": "#ffffff",
        "features": ["Novo pedido rápido no balcão ou WhatsApp", "Cardápio do dia: marmitex, açaí, pizzas e lanches", "Comanda térmica de 58 mm",
                     "Taxa de entrega por bairro", "Custos, CMV e resultado do mês", "Fechamento diário do caixa"],
        "gallery": [("img/clientes/ohana/tela-01.webp", "Novo pedido (dados de exemplo)"),
                    ("img/clientes/ohana/tela-02.webp", "Cardápio do dia e disponibilidade"),
                    ("img/clientes/ohana/tela-03.webp", "Gestão do negócio (dados de exemplo)")],
    },
]

for _p in CLIENTS:
    _p["client"] = True
ALL_PROJECTS = CLIENTS

# Sistemas prontos (mesmos cartões do catálogo do WhatsApp). Gerado de sistemas.json.
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sistemas.json"), encoding="utf-8") as _f:
    SYSTEMS = json.load(_f)
SYSTEM_CATS = [("todos", "Todos"), ("alimentacao", "Alimentação"), ("saude", "Saúde e bem-estar"),
               ("veiculos", "Veículos"), ("servicos", "Serviços e locação")]


def whatsapp_url(message="Olá! Conheci a Liviz Software pelo site e gostaria de conversar sobre um sistema para o meu negócio."):
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"


def systems_wa():
    """Modelos prontos com a mensagem de WhatsApp já preenchida para cada um."""
    return [dict(x, whatsapp=whatsapp_url(f"Olá! Vi o {x['full']} no site da Liviz Software e gostaria de saber mais."))
            for x in SYSTEMS]


@app.context_processor
def inject_company_data():
    return {
        "whatsapp_url": whatsapp_url(),
        "whatsapp_number_display": "(11) 92720-6740",
        "contact_email": CONTACT_EMAIL,
    }


@app.route("/")
def home():
    return render_template("index.html", clients=CLIENTS, systems=systems_wa(), system_cats=SYSTEM_CATS)


@app.route("/projetos")
def projetos():
    return render_template("projetos.html", clients=CLIENTS, systems=systems_wa(), system_cats=SYSTEM_CATS)


@app.route("/sistemas")
def sistemas():
    return render_template("sistemas.html", systems=systems_wa(), system_cats=SYSTEM_CATS)


@app.route("/projetos/<slug>")
def projeto(slug):
    project_data = next((item for item in ALL_PROJECTS if item["slug"] == slug), None)
    if not project_data:
        return "Projeto não encontrado", 404
    project_whatsapp = whatsapp_url(
        f"Olá! Vi o projeto {project_data['name']} no site da Liviz Software e gostaria de conversar sobre uma solução para o meu negócio."
    )
    return render_template("projeto.html", project=project_data, project_whatsapp=project_whatsapp)


@app.route("/contato", methods=["GET", "POST"])
def contato():
    status = None
    form_data = {"nome": "", "email": "", "telefone": "", "empresa": "", "mensagem": ""}

    if request.method == "POST":
        for field in form_data:
            form_data[field] = request.form.get(field, "").strip()

        # Campo invisível: bots costumam preenchê-lo.
        if request.form.get("website", "").strip():
            return render_template("contato.html", status="success", form_data=form_data)

        if not form_data["nome"] or not form_data["email"] or not form_data["mensagem"]:
            status = "required"
        else:
            smtp_host = os.getenv("SMTP_HOST", "email-ssl.com.br")
            smtp_port = int(os.getenv("SMTP_PORT", "465"))
            smtp_user = os.getenv("SMTP_USER", CONTACT_EMAIL)
            smtp_password = os.getenv("SMTP_PASSWORD", "")

            if not smtp_password:
                app.logger.error("SMTP_PASSWORD não configurada no ambiente.")
                status = "error"
            else:
                try:
                    msg = EmailMessage()
                    msg["Subject"] = f"Novo contato pelo site — {form_data['nome']}"
                    msg["From"] = f"Liviz Software <{smtp_user}>"
                    msg["To"] = CONTACT_EMAIL
                    msg["Reply-To"] = form_data["email"]
                    msg.set_content(
                        "Nova solicitação recebida pelo site da Liviz Software\n\n"
                        f"Nome: {form_data['nome']}\n"
                        f"E-mail: {form_data['email']}\n"
                        f"Telefone: {form_data['telefone'] or 'Não informado'}\n"
                        f"Empresa: {form_data['empresa'] or 'Não informada'}\n\n"
                        f"Mensagem:\n{form_data['mensagem']}\n"
                    )

                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=20) as server:
                        server.login(smtp_user, smtp_password)
                        server.send_message(msg)
                    status = "success"
                    form_data = {key: "" for key in form_data}
                except Exception:
                    app.logger.exception("Falha ao enviar formulário de contato por SMTP")
                    status = "error"

    return render_template("contato.html", status=status, form_data=form_data)


if __name__ == "__main__":
    app.run(debug=True)
