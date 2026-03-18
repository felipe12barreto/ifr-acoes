 import yfinance as yf
import pandas as pd
import ta
import streamlit as st

# =========================
# ESTILO (centralizar)
# =========================
st.markdown("""
<style>
h1, h2, h3 {
    text-align: center;
}
table {
    margin-left: auto;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LISTAS
# =========================

acoes = [
    "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "SANB4.SA", "BPAC11.SA", "B3SA3.SA", "PSSA3.SA",
    "VALE3.SA", "GOAU4.SA", "GGBR4.SA", "CMIN3.SA",
    "ABEV3.SA", "LREN3.SA", "VIVA3.SA", "GRND3.SA",
    "EZTC3.SA", "CURY3.SA",
    "TOTS3.SA", "ODPV3.SA", "ITSA4.SA", "WEGE3.SA",
    "BBSE3.SA", "CXSE3.SA", "MDIA3.SA", "SBSP3.SA"
]

fiis = [
    "KNCR11.SA",
    "BRCO11.SA",
    "HGRU11.SA",
    "MXRF11.SA",
    "XPLG11.SA",
    "BTHF11.SA"
]

btc = ["BTC-USD"]

# =========================
# FUNÇÕES IFR
# =========================

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

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()

        return round(df['rsi'].iloc[-1], 2)

    except:
        return None


def calcular_ifr_min_5anos(ticker):
    try:
        df = yf.download(
            ticker,
            period="5y",
            interval="1wk",
            auto_adjust=True,
            progress=False
        )

        if df.empty or len(df) < 50:
            return None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()

        return round(df['rsi'].min(), 2)

    except:
        return None

# =========================
# GERAR TABELA
# =========================

def gerar_tabela(lista, tipo="acao"):
    dados = []

    for ativo in lista:
        ifr = calcular_ifr(ativo)
        ifr_min = calcular_ifr_min_5anos(ativo)

        nome = ativo.replace(".SA", "").replace("-USD", "")

        # LINK TRADINGVIEW
        if tipo == "btc":
            link_tv = "https://www.tradingview.com/chart/?symbol=BTCUSD"
        else:
            link_tv = f"https://www.tradingview.com/chart/?symbol=BMFBOVESPA:{nome}"

        if tipo == "acao":
            link_fund = f"https://www.analisedeacoes.com/acoes/{nome.lower()}/"

            dados.append({
                "Ativo": f'<a href="{link_tv}" target="_blank">{nome}</a>',
                "IFR 14": ifr,
                "Min 5 anos": ifr_min,
                "📊": f'<a href="{link_fund}" target="_blank">📊</a>'
            })

        else:
            dados.append({
                "Ativo": f'<a href="{link_tv}" target="_blank">{nome}</a>',
                "IFR 14": ifr,
                "Min 5 anos": ifr_min
            })

    df = pd.DataFrame(dados)
    df = df.dropna()
    df = df.sort_values(by="IFR 14")

    return df

# =========================
# COR IFR
# =========================

def color_ifr(val):
    if val < 30:
        return 'color: green'
    elif val < 40:
        return 'color: lightgreen'
    elif val < 60:
        return 'color: white'
    else:
        return 'color: red'

# =========================
# INTERFACE
# =========================

st.title("📊 Monitor de Mercado")

# AÇÕES
st.subheader("Ações")
df_acoes = gerar_tabela(acoes, tipo="acao")
styled_acoes = df_acoes.style.applymap(color_ifr, subset=["IFR 14"])
st.markdown(styled_acoes.to_html(escape=False), unsafe_allow_html=True)

# FIIs
st.subheader("FIIs")
df_fiis = gerar_tabela(fiis, tipo="fii")
styled_fiis = df_fiis.style.applymap(color_ifr, subset=["IFR 14"])
st.markdown(styled_fiis.to_html(escape=False), unsafe_allow_html=True)

# BTC
st.subheader("Bitcoin")
df_btc = gerar_tabela(btc, tipo="btc")
styled_btc = df_btc.style.applymap(color_ifr, subset=["IFR 14"])
st.markdown(styled_btc.to_html(escape=False), unsafe_allow_html=True)
