from urllib.parse import quote
from flask import Flask, render_template, request
import os
import smtplib
import ssl
from email.message import EmailMessage

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
