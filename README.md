# Liviz Software — Site V3

Site institucional/comercial em Flask.

## Atualizações V3
- Hero comercial revisado.
- Novo efeito visual na tela inicial: aro luminoso animado + órbitas, sem girar o logo.
- Tela de abertura suave mantida apenas na entrada/reload.
- CTA de orçamento via WhatsApp.
- WhatsApp: (11) 92720-6740.
- E-mail profissional preparado: contato@livizsoftware.com.br (aguardando conclusão da configuração DNS/Locaweb).
- Clientes ativos: Gaúcha Lanches, Bruma's Pizzaria, Brisa Burguer's, Consulmed, A.M. Imóveis e Ohana Restaurantes (dados em `CLIENTS`, app.py).
- Modelos prontos: 24 sistemas do catálogo em `sistemas.json`, com carrossel e filtro por segmento; página /sistemas.
- Seção Sobre e posicionamento comercial.
- Formulário prepara a mensagem e encaminha a conversa para WhatsApp (não depende do e-mail estar ativo).
- Layout responsivo.

## Rodar localmente
```bash
pip install -r requirements.txt
python app.py
```

Acesse: http://127.0.0.1:5000

## Próximas etapas
- Ativar o e-mail contato@livizsoftware.com.br após validação do domínio.
- Publicar e apontar livizsoftware.com.br para a hospedagem.
