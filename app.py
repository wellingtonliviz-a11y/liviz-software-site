from urllib.parse import quote
from flask import Flask, render_template, request

app = Flask(__name__)

WHATSAPP_NUMBER = "5511927206740"
CONTACT_EMAIL = "contato@livizsoftware.com.br"

PROJECTS = [
    {
        "slug": "ws-zeladoria",
        "name": "WS Zeladoria",
        "category": "Gestão de atendimentos",
        "description": "Sistema sob medida para organizar clientes, chamados, execução de serviços e faturamento em uma única operação.",
        "logo": "img/projects/ws-zeladoria.png",
        "gallery_folder": "img/projects/ws-zeladoria",
        "features": ["Dashboard operacional", "Clientes e histórico", "Controle de atendimentos", "Acompanhamento de faturamento", "Acesso online"],
    },
    {
        "slug": "dr-reparos-erp",
        "name": "DR Reparos ERP",
        "category": "Gestão empresarial",
        "description": "ERP criado a partir de uma operação real para centralizar clientes, orçamentos, serviços, faturamento, custos e indicadores.",
        "logo": "img/projects/dr-reparos.png",
        "gallery_folder": "img/projects/dr-reparos",
        "features": ["Clientes", "Orçamentos e PDFs", "Serviços", "Faturamento", "Custos e indicadores"],
    },
    {
        "slug": "nagahashi-controle",
        "name": "Nagahashi Controle",
        "category": "Controle financeiro",
        "description": "Aplicação personalizada para acompanhar clientes, capital emprestado, juros, vencimentos e pagamentos com mais clareza.",
        "logo": "img/projects/nagahashi.png",
        "gallery_folder": "img/projects/nagahashi",
        "features": ["Clientes", "Capital emprestado", "Juros por ciclo", "Pagamentos", "Acompanhamento de vencimentos"],
    },
]


def whatsapp_url(message="Olá! Conheci a Liviz Software pelo site e gostaria de conversar sobre um sistema para o meu negócio."):
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"


@app.context_processor
def inject_company_data():
    return {
        "whatsapp_url": whatsapp_url(),
        "whatsapp_number_display": "(11) 92720-6740",
        "contact_email": CONTACT_EMAIL,
    }


@app.route("/")
def home():
    return render_template("index.html", projects=PROJECTS)


@app.route("/projetos")
def projetos():
    return render_template("projetos.html", projects=PROJECTS)


@app.route("/projetos/<slug>")
def projeto(slug):
    project_data = next((item for item in PROJECTS if item["slug"] == slug), None)
    if not project_data:
        return "Projeto não encontrado", 404
    project_whatsapp = whatsapp_url(
        f"Olá! Vi o projeto {project_data['name']} no site da Liviz Software e gostaria de conversar sobre uma solução para o meu negócio."
    )
    return render_template("projeto.html", project=project_data, project_whatsapp=project_whatsapp)


@app.route("/contato", methods=["GET", "POST"])
def contato():
    whatsapp_contact = None
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        empresa = request.form.get("empresa", "").strip()
        mensagem = request.form.get("mensagem", "").strip()
        texto = f"Olá! Meu nome é {nome or 'cliente'}"
        if empresa:
            texto += f", da empresa {empresa}"
        texto += f". Entrei em contato pelo site da Liviz Software.\n\n{mensagem}"
        whatsapp_contact = whatsapp_url(texto)
    return render_template("contato.html", whatsapp_contact=whatsapp_contact)


if __name__ == "__main__":
    app.run(debug=True)
