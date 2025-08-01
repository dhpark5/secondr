import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("교류 회로 실험 시뮬레이터")

st.sidebar.header("실험 선택")
experiment = st.sidebar.radio("실험을 선택하세요:", ["① RC/RL 시상수 측정", "② 필터 주파수 응답", "③ RLC 공명 측정"])

if experiment == "① RC/RL 시상수 측정":
    st.header("① RC 또는 RL 회로의 시상수 측정")
    circuit_type = st.radio("회로 선택:", ["RC 회로", "RL 회로"])

    if circuit_type == "RC 회로":
        R = st.slider("저항 R (Ω)", 100, 5000, 1000)
        C = st.slider("커패시터 C (μF)", 1, 100, 10) * 1e-6
        tau = R * C
    else:
        R = st.slider("저항 R (Ω)", 10, 1000, 100)
        L = st.slider("인덕터 L (mH)", 1, 100, 10) * 1e-3
        tau = L / R

    t = np.linspace(0, 5 * tau, 500)
    v = 1 - np.exp(-t / tau)

    st.write(f"**시상수 τ = {tau * 1000:.2f} ms**")

    fig, ax = plt.subplots()
    ax.plot(t * 1000, v)
    ax.axhline(0.63, color='r', linestyle='--', label='63% 수준')
    ax.set_xlabel("시간 (ms)")
    ax.set_ylabel("정규화 전압")
    ax.set_title("충전 곡선 (정규화)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

elif experiment == "② 필터 주파수 응답":
    st.header("② 고주파/저주파 필터 특성 분석")
    filter_type = st.radio("필터 종류:", ["LPF (저역 통과)", "HPF (고역 통과)"])
    R = st.slider("저항 R (Ω)", 100, 5000, 1000)
    C = st.slider("커패시터 C (μF)", 0.1, 10.0, 1.0) * 1e-6
    f = np.logspace(2, 5, 500)
    w = 2 * np.pi * f

    if filter_type == "LPF (저역 통과)":
        H = 1 / np.sqrt(1 + (w * R * C)**2)
    else:
        H = (w * R * C) / np.sqrt(1 + (w * R * C)**2)

    fig, ax = plt.subplots()
    ax.semilogx(f, 20 * np.log10(H))
    ax.set_xlabel("주파수 (Hz)")
    ax.set_ylabel("이득 (dB)")
    ax.set_title("필터 주파수 응답")
    ax.grid(True, which='both')
    st.pyplot(fig)

elif experiment == "③ RLC 공명 측정":
    st.header("③ RLC 회로의 공명 주파수 측정")
    R = st.slider("저항 R (Ω)", 10, 1000, 100)
    L = st.slider("인덕턴스 L (mH)", 1, 100, 10) * 1e-3
    C = st.slider("커패시턴스 C (μF)", 0.1, 10.0, 0.1) * 1e-6

    f = np.linspace(1000, 10000, 1000)
    w = 2 * np.pi * f
    Z = np.sqrt(R**2 + (w*L - 1/(w*C))**2)
    I = 1 / Z

    fr = 1 / (2 * np.pi * np.sqrt(L * C))
    st.write(f"**공명 주파수 f₀ ≈ {fr:.1f} Hz**")

    fig, ax = plt.subplots()
    ax.plot(f, I / max(I))
    ax.axvline(fr, color='r', linestyle='--', label='공명 주파수')
    ax.set_xlabel("주파수 (Hz)")
    ax.set_ylabel("정규화 전류")
    ax.set_title("RLC 회로의 공명 특성")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
