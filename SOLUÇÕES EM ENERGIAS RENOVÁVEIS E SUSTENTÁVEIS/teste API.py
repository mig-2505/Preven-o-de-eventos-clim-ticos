import requests
import pandas as pd

dados_excel = []

API_KEY = "3cb63b4911b355aa49a1ea675bfba6b0"
cidade = input("Digite a Cidade que deseja procurar: ")
dias = 16

# Atual:
link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br"

# Previsão de 5 dias (a cada 3h)
url = f"https://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={API_KEY}&lang=pt_br"

# Request
requisicao_atual = requests.get(link)
requisicao_previsao = requests.get(url)

# Transformando em json
requisicao_dic = requisicao_atual.json()
requisicao_dic_previsao = requisicao_previsao.json()

# Criando variaveis com dados atuais para cada coisa presente no dicionario
descricao = requisicao_dic["weather"][0]["description"]
temperatura = requisicao_dic["main"]["temp"] - 273.15
umidade = requisicao_dic["main"]["humidity"]
vento = requisicao_dic["wind"]["speed"] * 3.6  # m/s para km/h
chuva = requisicao_dic.get("rain", {}).get("1h")

# Lista do que o usuario quer fazer, por meio de escolhas
while True:
    print("==== MENU ====")
    print("1- Ver dados atuais")
    print("2- Ver dados dos proximos 5 dias")
    print("3- Verificar se há algum tipo de evento extremo nos proximos dias")
    print("4- Sair do programa")
    opcao = input("Digite aqui:... ")

    if opcao not in ["1", "2", "3", "4"]:
        print("Digite um número válido.\n")
        continue

# Printando as varivaveis escolhidas
    if opcao == "1":
        print("==== DADOS ATUAIS ====")
        print(f"Descrição: {descricao}")
        print(f"Temperatura: {temperatura:.2f}ºC")
        print(f"Umidade: {umidade}")
        print(f"Vento: {vento:.1f} km/h")

        if chuva is not None:
            print(f"Chuva: {chuva} mm na última hora\n")
        else:
            print("Hoje não deve chover.\n")

# Criando variaveis e printando com previsao de 5 dias
    if opcao == "2":
        print("==== PREVISÃO PARA OS PRÓXIMOS DIAS ====")
        for i in range(0, len(requisicao_dic_previsao["list"]), 8):
            previsao = requisicao_dic_previsao["list"][i]
            data = previsao["dt_txt"]
            desc = previsao["weather"][0]["description"]
            temp_prev = previsao["main"]["temp"] - 273.15
            umidade_prev = previsao["main"]["humidity"]
            vento_prev = previsao["wind"]["speed"] * 3.6
            chuva_prev = previsao.get("rain", {}).get("3h", 0)

            print(f"\nData: {data}")
            print(f"Descrição: {desc}")
            print(f"Temperatura: {temp_prev:.1f}ºC")
            print(f"Umidade: {umidade_prev}%")
            print(f"Vento: {vento_prev:.1f} km/h")
            print(f"Chuva: {chuva_prev} mm\n")

            dados_excel.append({
                "Data": data,
                "Descrição": desc,
                "Temperatura (ºC)": round(temp_prev, 1),
                "Umidade (%)": umidade_prev,
                "Vento (km/h)": round(vento_prev, 1),
                "Chuva (mm)": chuva_prev
            })

        # Criar DataFrame e salvar no Excel
        df = pd.DataFrame(dados_excel)
        df.to_excel(f"previsao_tempo_{cidade}.xlsx", index=False)

        salvar = input("Deseja salvar essas informaçoes em excel ? (1-sim / 2-nao): ")
        if salvar == "1":
            df = pd.DataFrame(dados_excel)
            df.to_excel("previsao_tempo.xlsx", index=False)
            print("Previsão exportada para o arquivo 'previsao_tempo.xlsx'\n")
        else:
            print("Previsão não salva.\n")

# Verificação de eventos extremos
    if opcao == "3":
        print("==== EVENTOS EXTREMOS NOS PRÓXIMOS DIAS ====")
        for i in range(0, len(requisicao_dic_previsao["list"]), 8):
            previsao = requisicao_dic_previsao["list"][i]
            data = previsao["dt_txt"]
            temp_prev = previsao["main"]["temp"] - 273.15
            vento_prev = previsao["wind"]["speed"] * 3.6
            chuva_prev = previsao.get("rain", {}).get("3h", 0)

            print(f"\nData: {data}")
            if temp_prev >= 30:
                print("⚠️ ALTA TEMPERATURA: possível onda de calor!")
                print("Sugestão: Usar paines solares inteligentes com protecao termica para aproveitar ao maximo da alta temperatura")
            elif temp_prev <= 10:
                print("⚠️ BAIXA TEMPERATURA: possível onda de frio!")
                print("Sugestão: Ficar em casa e se manter aquecido")
            elif vento_prev > 50:
                print("⚠️ VENTOS FORTES: risco de tempestade!")
                print("Sugestão: Desligar placas moveis para evitar danos, e ficar em casa seguro")
            elif chuva_prev > 10:
                print("⚠️ CHUVAS FORTES: risco de alagamentos!")
                print("Sugestão: Integrá-los com sensores de alagamento e assistente virtual que alerta o usuário como a Alexa, Google Assitant")
            else:
                print("Sem eventos extremos previstos.")

    # Opção para sair do programa
    if opcao == "4":
        print("Saindo do programa\n")
        break


