import yfinance as yf
import pandas as pd
import ta
import streamlit as st

# SUA LISTA DE AÇÕES
acoes = [
    "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "SANB4.SA", "BPAC11.SA", "B3SA3.SA", "PSSA3.SA",
    "VALE3.SA", "GOAU4.SA", "GGBR4.SA", "CMIN3.SA",
    "ABEV3.SA", "LREN3.SA", "VIVA3.SA", "GRND3.SA",
    "EZTC3.SA", "CURY3.SA",
    "TOTS3.SA", "ODPV3.SA", "ITSA4.SA", "WEGE3.SA",
    "BBSE3.SA", "CXSE3.SA", "MDIA3.SA", "SBSP3.SA"
]

# FUNÇÃO PRA CALCULAR IFR
def calcular_ifr(ticker):
    try:
        df = yf.download(
            ticker,
            period="1y",
            interval="1wk",
            auto_adjust=True,
            progress=False
        )

        if df.empty or len(df) < 20:
            return None

        # corrigir colunas multi-index
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()

        return round(df['rsi'].iloc[-1], 2)

    except Exception as e:
        print(f"Erro em {ticker}: {e}")
        return None

# GERAR DADOS
dados = []

for acao in acoes:
    ifr = calcular_ifr(acao)

    ticker_limpo = acao.replace(".SA", "")
   link = f"https://www.tradingview.com/chart/?symbol=BMFBOVESPA:{ticker_limpo}"

    dados.append({
        "Ação": f'<a href="{link}" target="_blank">{ticker_limpo}</a>',
        "IFR 14 Semanal": ifr
    })

# CRIAR DATAFRAME
df = pd.DataFrame(dados)

# REMOVER None
df = df.dropna()

# ORDENAR
df = df.sort_values(by="IFR 14 Semanal")

# FUNÇÃO DE COR
def color_ifr(val):
    if val < 30:
        return 'color: green'
    elif val < 40:
        return 'color: lightgreen'
    elif val < 60:
        return 'color: white'
    else:
        return 'color: red'

# APLICAR ESTILO
styled_df = df.style.applymap(color_ifr, subset=["IFR 14 Semanal"])

# INTERFACE
st.title("Ações - IFR 14 Semanal")

# MOSTRAR COM LINKS
st.markdown(styled_df.to_html(escape=False), unsafe_allow_html=True)
