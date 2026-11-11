import requests

URL_WEB_APP = "https://script.google.com/macros/s/AKfycbyAch3eoDxR4TrU5zX4XbD7pBNxHzq890hHpinDxPr1ugewXxH_sQnZhb_nXeC6LYIT/exec"

def obter_produtos():
    try:
        resposta = requests.get(f"{URL_WEB_APP}?tipo=produtos", timeout=10)
        return resposta.json()
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return {"status": "erro", "produtos": [], "precos": {}, "produtos_detalhado": {}}

def obter_alunos():
    try:
        resposta = requests.get(f"{URL_WEB_APP}?tipo=alunos", timeout=10)
        return resposta.json()
    except Exception as e:
        print(f"Erro ao buscar alunos: {e}")
        return {"status": "erro", "alunos_detalhado": {}}

def obter_extrato_fiado(aluno):
    try:
        resposta = requests.get(f"{URL_WEB_APP}?tipo=fiado_aluno&aluno={aluno}", timeout=10)
        return resposta.json()
    except Exception as e:
        print(f"Erro ao buscar fiado: {e}")
        return {"status": "erro", "extrato": [], "saldo_atual": 0}

def obter_extrato_caixa():
    try:
        resposta = requests.get(f"{URL_WEB_APP}?tipo=caixa", timeout=10)
        return resposta.json()
    except Exception as e:
        print(f"Erro ao buscar extrato de caixa: {e}")
        return {"status": "erro", "extrato_caixa": []}

def registrar_venda(aluno, forma_pagamento, itens):
    try:
        payload = {
            "acao": "registrar_venda",
            "aluno": aluno,
            "forma_pagamento": forma_pagamento,
            "itens": itens
        }
        resposta = requests.post(URL_WEB_APP, json=payload, timeout=10)
        return resposta.json()
    except Exception as e:
        print(f"Erro ao registrar venda: {e}")
        return {"status": "erro", "mensagem": str(e)}

def executar_acao_caixa(acao, valor):
    try:
        payload = {
            "acao": acao,
            "valor": float(valor)
        }
        resposta = requests.post(URL_WEB_APP, json=payload, timeout=10)
        return resposta.json()
    except Exception as e:
        print(f"Erro ao executar ação de caixa: {e}")
        return {"status": "erro", "mensagem": str(e)}

def cadastrar_produto(dados_produto):
    try:
        payload = {"acao": "cadastrar_produto"}
        payload.update(dados_produto)
        resposta = requests.post(URL_WEB_APP, json=payload, timeout=10)
        return resposta.json()
    except Exception as e:
        print(f"Erro ao cadastrar produto: {e}")
        return {"status": "erro", "mensagem": str(e)}

def cadastrar_aluno(dados_aluno):
    try:
        payload = {"acao": "cadastrar_aluno"}
        payload.update(dados_aluno)
        resposta = requests.post(URL_WEB_APP, json=payload, timeout=10)
        return resposta.json()
    except Exception as e:
        print(f"Erro ao cadastrar aluno: {e}")
        return {"status": "erro", "mensagem": str(e)}

def obter_relatorio_vendas(data_ini="", data_fim="", aluno=""):
    try:
        url = f"{URL_WEB_APP}?tipo=relatorio_vendas&dataIni={data_ini}&dataFim={data_fim}&aluno={aluno}"
        return requests.get(url, timeout=10).json()
    except Exception as e:
        print(f"Erro: {e}")
        return {"status": "erro", "vendas": [], "recebido_periodo": 0, "a_receber_periodo": 0, "a_receber_total": 0}

def obter_relatorio_diario():
    try:
        return requests.get(f"{URL_WEB_APP}?tipo=relatorio_diario", timeout=10).json()
    except Exception as e:
        print(f"Erro: {e}")
        return {"status": "erro", "diario": []}

def obter_dashboard(data_ini="", data_fim=""):
    try:
        url = f"{URL_WEB_APP}?tipo=dashboard&dataIni={data_ini}&dataFim={data_fim}"
        return requests.get(url, timeout=10).json()
    except Exception as e:
        print(f"Erro: {e}")
        return {"status": "erro"}