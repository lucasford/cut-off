import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

# Sayfa yapılandırması
st.set_page_config(
    page_title="Cut-off Grade Hesaplama Uygulaması",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stil
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #A23B72;
        border-bottom: 2px solid #A23B72;
        padding-bottom: 0.5rem;
        margin: 1rem 0;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #2E86AB;
    }
</style>
""", unsafe_allow_html=True)

# Ana başlık
st.markdown('<h1 class="main-header">⛏️ Cut-off Grade Hesaplama Uygulaması</h1>', unsafe_allow_html=True)
st.markdown("*Jean-Michel Rendu'nun 'An Introduction to Cut-off Grade Estimation' kitabına dayalı*")

# Sidebar - Uygulama Seçimi
st.sidebar.title("📋 Modül Seçimi")
app_mode = st.sidebar.selectbox(
    "Hangi hesaplama modülünü kullanmak istiyorsunuz?",
    [
        "🏠 Ana Sayfa",
        "📊 Temel Cut-off Grade Hesaplama",
        "⚖️ İki Proses Karşılaştırması", 
        "💰 NPV ve Fırsat Maliyeti Analizi",
        "🔄 Harmanlama Optimizasyonu",
        "📈 Dinamik Cut-off Grade Stratejisi",
        "🏭 Tesis Kapasitesi Optimizasyonu"
    ]
)

def home_page():
    st.markdown('<h2 class="section-header">📚 Uygulama Hakkında</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 Temel Hesaplamalar
        - Breakeven cut-off grade
        - Mill vs Mine cut-off
        - Grade-tonnage ilişkileri
        - Utility fonksiyonları
        """)
    
    with col2:
        st.markdown("""
        ### 💡 Gelişmiş Analizler
        - NPV optimizasyonu
        - Fırsat maliyeti hesabı
        - Kapasite kısıtları
        - Risk analizi
        """)
    
    with col3:
        st.markdown("""
        ### 🔧 Pratik Araçlar
        - İnteraktif grafikler
        - Senaryo karşılaştırması
        - Otomatik raporlama
        - Parametre optimizasyonu
        """)
    
    st.markdown('<h2 class="section-header">📖 Kitap Bölümleri</h2>', unsafe_allow_html=True)
    
    chapters = {
        "Bölüm 1": "Giriş ve Temel Kavramlar",
        "Bölüm 2": "Genel Kavramlar ve Utility Fonksiyonları", 
        "Bölüm 3": "Breakeven Cut-off Grade Hesaplamaları",
        "Bölüm 4": "Kapasite Kısıtları ve Fırsat Maliyetleri",
        "Bölüm 5": "Jeolojik Kısıtlar ve Fırsat Maliyetleri",
        "Bölüm 6": "Cut-off Grade ve Maden Planlaması",
        "Bölüm 7": "Maliyet Analizi ve Dahil Edilecek Maliyetler",
        "Bölüm 8": "Harmanlama Stratejisi",
        "Bölüm 9": "Sonuçlar ve Öneriler"
    }
    
    for chapter, description in chapters.items():
        st.markdown(f"**{chapter}:** {description}")

def basic_cutoff_calculator():
    st.markdown('<h2 class="section-header">📊 Temel Cut-off Grade Hesaplama</h2>', unsafe_allow_html=True)
    
    # Parametreler
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💎 Maden Parametreleri")
        metal_price = st.number_input("Metal Fiyatı ($/oz veya $/lb)", value=1400.0, step=10.0)
        recovery = st.slider("Verim (%)", 50, 95, 85) / 100
        cost_of_sales = st.number_input("Satış Maliyeti ($/oz veya $/lb)", value=50.0, step=5.0)
        
        st.markdown("### ⛏️ Madencilik Maliyetleri")
        mining_cost_ore = st.number_input("Cevher Madencilik Maliyeti ($/ton)", value=4.50, step=0.1)
        mining_cost_waste = st.number_input("Atık Madencilik Maliyeti ($/ton)", value=3.00, step=0.1)
        
    with col2:
        st.markdown("### 🏭 İşleme Maliyetleri")
        processing_cost = st.number_input("İşleme Maliyeti ($/ton)", value=75.0, step=1.0)
        overhead_cost = st.number_input("Genel Giderler ($/ton)", value=15.0, step=1.0)
        
        st.markdown("### 📏 Birim Dönüşümü")
        unit_conversion = st.selectbox("Metal Birimi", ["oz/ton (Altın)", "% (Bakır)"])
        if unit_conversion == "oz/ton (Altın)":
            conversion_factor = 31.1035  # g/ton to oz/ton
        else:
            conversion_factor = 2205  # % to lb/ton
    
    # Hesaplamalar
    net_value = (metal_price - cost_of_sales) * recovery
    
    # Mine cut-off grade
    total_ore_cost = mining_cost_ore + processing_cost + overhead_cost
    mine_cutoff = total_ore_cost / (net_value * conversion_factor)
    
    # Mill cut-off grade  
    mill_cost = processing_cost + overhead_cost
    mill_cutoff = mill_cost / (net_value * conversion_factor)
    
    # Sonuçları göster
    st.markdown('<h2 class="section-header">📊 Hesaplama Sonuçları</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        if unit_conversion == "oz/ton (Altın)":
            st.metric("Mine Cut-off Grade", f"{mine_cutoff:.3f} oz/t", f"{mine_cutoff*31.1:.1f} g/t")
        else:
            st.metric("Mine Cut-off Grade", f"{mine_cutoff:.3f} %", "Bakır eşdeğeri")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        if unit_conversion == "oz/ton (Altın)":
            st.metric("Mill Cut-off Grade", f"{mill_cutoff:.3f} oz/t", f"{mill_cutoff*31.1:.1f} g/t")
        else:
            st.metric("Mill Cut-off Grade", f"{mill_cutoff:.3f} %", "Bakır eşdeğeri")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Net Değer", f"${net_value:.2f}", "Birim başına")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Grade-Tonnage grafiği
    st.markdown('<h2 class="section-header">📈 Grade-Tonnage İlişkisi</h2>', unsafe_allow_html=True)
    
    # Örnek grade-tonnage eğrisi oluştur
    grades = np.linspace(0, mine_cutoff * 3, 100)
    max_tonnage = st.slider("Maksimum Tonaj (milyon ton)", 1.0, 50.0, 20.0)
    
    # Exponential decay modeli
    tonnage = max_tonnage * np.exp(-2 * grades / mine_cutoff)
    avg_grade = mine_cutoff * 0.3 + grades * 0.7
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Tonaj vs Cut-off Grade', 'Ortalama Tenör vs Cut-off Grade'),
        x_title="Cut-off Grade"
    )
    
    # Tonaj grafiği
    fig.add_trace(
        go.Scatter(x=grades, y=tonnage, mode='lines', name='Tonaj', line=dict(width=3)),
        row=1, col=1
    )
    
    # Cut-off grade çizgileri
    fig.add_vline(x=mine_cutoff, line_dash="dash", line_color="red", 
                 annotation_text="Mine Cut-off", row=1, col=1)
    fig.add_vline(x=mill_cutoff, line_dash="dash", line_color="blue",
                 annotation_text="Mill Cut-off", row=1, col=1)
    
    # Ortalama tenör grafiği
    fig.add_trace(
        go.Scatter(x=grades, y=avg_grade, mode='lines', name='Ort. Tenör', 
                  line=dict(width=3, color='orange')),
        row=1, col=2
    )
    
    fig.add_vline(x=mine_cutoff, line_dash="dash", line_color="red", row=1, col=2)
    fig.add_vline(x=mill_cutoff, line_dash="dash", line_color="blue", row=1, col=2)
    
    fig.update_layout(height=500, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

def process_comparison():
    st.markdown('<h2 class="section-header">⚖️ İki Proses Karşılaştırması</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔄 Proses 1 (örn: Yığın Liç)")
        recovery1 = st.slider("Verim 1 (%)", 30, 80, 60) / 100
        cost1 = st.number_input("İşleme Maliyeti 1 ($/ton)", value=9.0, step=0.5)
        mining_cost1 = st.number_input("Madencilik Maliyeti 1 ($/ton)", value=5.0, step=0.1)
        
    with col2:
        st.markdown("### ⚙️ Proses 2 (örn: Değirmen)")
        recovery2 = st.slider("Verim 2 (%)", 80, 98, 87) / 100
        cost2 = st.number_input("İşleme Maliyeti 2 ($/ton)", value=35.0, step=1.0)
        mining_cost2 = st.number_input("Madencilik Maliyeti 2 ($/ton)", value=5.5, step=0.1)
    
    # Genel parametreler
    metal_price = st.number_input("Metal Fiyatı ($/oz)", value=1600.0, step=10.0)
    cost_of_sales = st.number_input("Satış Maliyeti ($/oz)", value=50.0, step=5.0)
    
    # Hesaplamalar
    net_value = metal_price - cost_of_sales
    
    grades = np.linspace(0, 10, 1000)
    
    # Utility fonksiyonları
    U1 = grades * recovery1 * net_value / 31.1035 - (mining_cost1 + cost1)
    U2 = grades * recovery2 * net_value / 31.1035 - (mining_cost2 + cost2)
    
    # Cut-off grade hesaplama
    diff = np.abs(U1 - U2)
    cutoff_idx = np.argmin(diff)
    cutoff_grade = grades[cutoff_idx]
    
    # Waste cut-off grades
    waste_cutoff1 = (mining_cost1 + cost1) * 31.1035 / (recovery1 * net_value)
    waste_cutoff2 = (mining_cost2 + cost2) * 31.1035 / (recovery2 * net_value)
    
    # Sonuçlar
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Proses 1-2 Cut-off", f"{cutoff_grade:.2f} g/t")
    with col2:
        st.metric("Atık-Proses 1", f"{waste_cutoff1:.2f} g/t")  
    with col3:
        st.metric("Atık-Proses 2", f"{waste_cutoff2:.2f} g/t")
    
    # Utility grafiği
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=grades, y=U1, mode='lines', name='Proses 1 Utility', 
                            line=dict(width=3, color='blue')))
    fig.add_trace(go.Scatter(x=grades, y=U2, mode='lines', name='Proses 2 Utility',
                            line=dict(width=3, color='red')))
    fig.add_trace(go.Scatter(x=grades, y=np.maximum(U1, U2), mode='lines', 
                            name='Maksimum Utility', line=dict(width=4, color='green')))
    
    # Cut-off çizgileri
    fig.add_vline(x=cutoff_grade, line_dash="dash", line_color="black",
                 annotation_text=f"Cut-off: {cutoff_grade:.2f} g/t")
    fig.add_vline(x=waste_cutoff1, line_dash="dot", line_color="blue",
                 annotation_text="Atık-P1")
    fig.add_vline(x=waste_cutoff2, line_dash="dot", line_color="red", 
                 annotation_text="Atık-P2")
    
    fig.update_layout(
        title="Proses Karşılaştırması - Utility Fonksiyonları",
        xaxis_title="Tenör (g/t)",
        yaxis_title="Utility ($/ton)",
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

def npv_opportunity_analysis():
    st.markdown('<h2 class="section-header">💰 NPV ve Fırsat Maliyeti Analizi</h2>', unsafe_allow_html=True)
    
    # Parametreler
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Proje Parametreleri")
        initial_npv = st.number_input("Başlangıç NPV ($ milyon)", value=800.0, step=10.0)
        discount_rate = st.slider("İskonto Oranı (%)", 5, 20, 15) / 100
        mine_life = st.slider("Maden Ömrü (yıl)", 5, 20, 10)
        
    with col2:
        st.markdown("### 🏭 Kapasite Kısıtları")
        mill_capacity = st.number_input("Değirmen Kapasitesi (milyon ton/yıl)", value=50.0, step=1.0)
        mine_capacity = st.number_input("Maden Kapasitesi (milyon ton/yıl)", value=72.0, step=1.0)
        smelter_capacity = st.number_input("İzabe Kapasitesi (milyon lb Cu/yıl)", value=500.0, step=10.0)
    
    # NPV'nin zaman içindeki değişimi
    years = np.arange(0, mine_life + 1)
    yearly_cashflow = initial_npv / sum([(1 + discount_rate) ** -i for i in range(mine_life)])
    
    npv_remaining = []
    for year in years:
        remaining_years = mine_life - year
        if remaining_years > 0:
            npv = sum([yearly_cashflow / (1 + discount_rate) ** i for i in range(remaining_years)])
            npv_remaining.append(npv)
        else:
            npv_remaining.append(0)
    
    # Fırsat maliyetleri hesaplama
    mill_opp_cost = [discount_rate * npv / mill_capacity for npv in npv_remaining]
    mine_opp_cost = [discount_rate * npv / mine_capacity for npv in npv_remaining]
    smelter_opp_cost = [discount_rate * npv / smelter_capacity for npv in npv_remaining]
    
    # Grafikler
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('NPV Değişimi', 'Fırsat Maliyetleri', 
                       'Cut-off Grade Değişimi', 'Kapasite Kullanımı'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # NPV grafiği
    fig.add_trace(
        go.Scatter(x=years, y=npv_remaining, mode='lines+markers', name='Kalan NPV',
                  line=dict(width=3, color='blue')),
        row=1, col=1
    )
    
    # Fırsat maliyetleri
    fig.add_trace(
        go.Scatter(x=years, y=mill_opp_cost, mode='lines', name='Değirmen F.M.',
                  line=dict(width=2, color='red')),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=years, y=mine_opp_cost, mode='lines', name='Maden F.M.',
                  line=dict(width=2, color='green')),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=years, y=smelter_opp_cost, mode='lines', name='İzabe F.M.',
                  line=dict(width=2, color='orange')),
        row=1, col=2
    )
    
    # Cut-off grade değişimi (örnek)
    base_cutoff = 0.25
    cutoff_with_mill = [base_cutoff + opp/1000 for opp in mill_opp_cost]
    cutoff_with_mine = [base_cutoff + opp/1000 for opp in mine_opp_cost]
    
    fig.add_trace(
        go.Scatter(x=years, y=cutoff_with_mill, mode='lines', name='Değirmen Kısıtı',
                  line=dict(width=2, dash='dash')),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=years, y=cutoff_with_mine, mode='lines', name='Maden Kısıtı',
                  line=dict(width=2, dash='dot')),
        row=2, col=1
    )
    
    # Kapasite kullanımı
    fig.add_trace(
        go.Bar(x=['Değirmen', 'Maden', 'İzabe'], 
               y=[100, 80, 95], name='Kapasite %'),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Özet tablo
    st.markdown("### 📊 Fırsat Maliyeti Özeti")
    
    df_summary = pd.DataFrame({
        'Yıl': years,
        'Kalan NPV ($M)': [f"{npv:.1f}" for npv in npv_remaining],
        'Değirmen F.M. ($/t)': [f"{cost:.2f}" for cost in mill_opp_cost],
        'Maden F.M. ($/t)': [f"{cost:.2f}" for cost in mine_opp_cost],
        'Cut-off Artışı (%)': [f"{(cutoff_with_mill[i] - base_cutoff)/base_cutoff*100:.1f}" 
                              for i in range(len(years))]
    })
    
    st.dataframe(df_summary, use_container_width=True)

def blending_optimization():
    st.markdown('<h2 class="section-header">🔄 Harmanlama Optimizasyonu</h2>', unsafe_allow_html=True)
    
    st.markdown("### 📊 Stok Yığını Özellikleri")
    
    # 3 stok yığını için parametreler
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Stok 1")
        tonnage1 = st.number_input("Tonaj 1 (bin ton)", value=2000, step=100, key="t1")
        grade1_1 = st.number_input("Tenör 1-1 (%)", value=1.0, step=0.1, key="g11")
        grade1_2 = st.number_input("Tenör 1-2 (g/t)", value=7.0, step=0.5, key="g12")
    
    with col2:
        st.markdown("#### Stok 2")
        tonnage2 = st.number_input("Tonaj 2 (bin ton)", value=1000, step=100, key="t2")
        grade2_1 = st.number_input("Tenör 2-1 (%)", value=2.0, step=0.1, key="g21")
        grade2_2 = st.number_input("Tenör 2-2 (g/t)", value=12.0, step=0.5, key="g22")
    
    with col3:
        st.markdown("#### Stok 3")
        tonnage3 = st.number_input("Tonaj 3 (bin ton)", value=4000, step=100, key="t3")
        grade3_1 = st.number_input("Tenör 3-1 (%)", value=0.8, step=0.1, key="g31")
        grade3_2 = st.number_input("Tenör 3-2 (g/t)", value=15.0, step=0.5, key="g32")
    
    # Hedef özellikleri
    st.markdown("### 🎯 Hedef Harmanlama Özellikleri")
    col1, col2 = st.columns(2)
    
    with col1:
        target_grade1 = st.number_input("Hedef Tenör 1 (%)", value=1.2, step=0.1)
        target_grade2 = st.number_input("Hedef Tenör 2 (g/t)", value=11.0, step=0.5)
    
    with col2:
        optimize_for = st.selectbox("Optimizasyon Hedefi", 
                                   ["Maksimum Tonaj", "Maksimum Metal İçeriği", "Belirli Tenör"])
    
    # Hesaplamalar
    def calculate_blend_proportions(t1, g11, g12, t2, g21, g22, t3, g31, g32, tg1, tg2):
        # Matris çözümü: A * p = b
        A = np.array([
            [g11, g21, g31],
            [g12, g22, g32],
            [1, 1, 1]
        ])
        b = np.array([tg1, tg2, 1])
        
        try:
            proportions = np.linalg.solve(A, b)
            return proportions
        except:
            return None
    
    proportions = calculate_blend_proportions(
        tonnage1, grade1_1, grade1_2,
        tonnage2, grade2_1, grade2_2, 
        tonnage3, grade3_1, grade3_2,
        target_grade1, target_grade2
    )
    
    if proportions is not None and all(p >= 0 for p in proportions):
        p1, p2, p3 = proportions
        
        # Maksimum tonaj hesaplama
        max_tonnages = [tonnage1/p1, tonnage2/p2, tonnage3/p3]
        max_tonnage = min(max_tonnages)
        
        # Kullanılacak tonajlar
        used_tonnage1 = max_tonnage * p1
        used_tonnage2 = max_tonnage * p2
        used_tonnage3 = max_tonnage * p3
        
        # Sonuçları göster
        st.markdown("### ✅ Harmanlama Sonuçları")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Maksimum Tonaj", f"{max_tonnage:.0f} bin ton")
        with col2:
            st.metric("Stok 1 Oranı", f"{p1*100:.1f}%")
        with col3:
            st.metric("Stok 2 Oranı", f"{p2*100:.1f}%")
        with col4:
            st.metric("Stok 3 Oranı", f"{p3*100:.1f}%")
        
        # Harmanlama diyagramı
        fig = go.Figure()
        
        # Stok noktaları
        fig.add_trace(go.Scatter(
            x=[grade1_1, grade2_1, grade3_1, grade1_1],
            y=[grade1_2, grade2_2, grade3_2, grade1_2],
            mode='lines+markers',
            name='Mümkün Bölge',
            line=dict(color='blue', width=2),
            marker=dict(size=10)
        ))
        
        # Hedef nokta
        fig.add_trace(go.Scatter(
            x=[target_grade1],
            y=[target_grade2],
            mode='markers',
            name='Hedef',
            marker=dict(size=15, color='red', symbol='star')
        ))
        
        # Etiketler
        fig.add_annotation(x=grade1_1, y=grade1_2, text="Stok 1", showarrow=True)
        fig.add_annotation(x=grade2_1, y=grade2_2, text="Stok 2", showarrow=True)
        fig.add_annotation(x=grade3_1, y=grade3_2, text="Stok 3", showarrow=True)
        
        fig.update_layout(
            title="Harmanlama Diyagramı",
            xaxis_title="Tenör 1 (%)",
            yaxis_title="Tenör 2 (g/t)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detaylı tablo
        df_blend = pd.DataFrame({
            'Stok': ['Stok 1', 'Stok 2', 'Stok 3', 'TOPLAM'],
            'Mevcut Tonaj': [tonnage1, tonnage2, tonnage3, tonnage1+tonnage2+tonnage3],
            'Kullanılan Tonaj': [used_tonnage1, used_tonnage2, used_tonnage3, max_tonnage],
            'Oran (%)': [p1*100, p2*100, p3*100, 100],
            'Tenör 1': [grade1_1, grade2_1, grade3_1, target_grade1],
            'Tenör 2': [grade1_2, grade2_2, grade3_2, target_grade2]
        })
        
        st.dataframe(df_blend, use_container_width=True)
        
    else:
        st.error("❌ Bu hedef tenörler ile harmanlama mümkün değil!")

def dynamic_cutoff_strategy():
    st.markdown('<h2 class="section-header">📈 Dinamik Cut-off Grade Stratejisi</h2>', unsafe_allow_html=True)
    
    # Parametreler
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Piyasa Parametreleri")
        base_price = st.number_input("Başlangıç Metal Fiyatı ($/oz)", value=1400.0, step=10.0)
        price_volatility = st.slider("Fiyat Volatilitesi (%)", 10, 50, 25) / 100
        price_trend = st.selectbox("Fiyat Trendi", ["Sabit", "Artan", "Azalan", "Çevrimsel"])
        
        st.markdown("### ⛏️ Maden Parametreleri")
        total_reserves = st.number_input("Toplam Rezerv (milyon ton)", value=100.0, step=5.0)
        mine_life = st.slider("Planlanan Maden Ömrü (yıl)", 10, 30, 15)
        
    with col2:
        st.markdown("### 💰 Finansal Parametreler")
        discount_rate = st.slider("İskonto Oranı (%)", 8, 18, 12) / 100
        base_cutoff = st.number_input("Başlangıç Cut-off (g/t)", value=2.0, step=0.1)
        stockpile_option = st.checkbox("Düşük Tenörlü Stoklama", value=True)
        
        st.markdown("### 🏭 Operasyonel Parametreler")
        processing_capacity = st.number_input("İşleme Kapasitesi (milyon ton/yıl)", value=8.0, step=0.5)
        recovery = st.slider("Ortalama Verim (%)", 75, 95, 85) / 100
    
    # Zaman serileri oluştur
    years = np.arange(0, mine_life)
    
    # Fiyat projeksiyonu
    if price_trend == "Sabit":
        prices = [base_price] * mine_life
    elif price_trend == "Artan":
        prices = [base_price * (1.03 ** year) for year in years]
    elif price_trend == "Azalan":
        prices = [base_price * (0.98 ** year) for year in years]
    else:  # Çevrimsel
        prices = [base_price * (1 + 0.3 * np.sin(year * np.pi / 3)) for year in years]
    
    # Volatilite ekle
    np.random.seed(42)  # Tekrarlanabilir sonuçlar için
    price_noise = np.random.normal(0, price_volatility, mine_life)
    prices = [max(p * (1 + noise), base_price * 0.5) for p, noise in zip(prices, price_noise)]
    
    # Dinamik cut-off hesaplama
    operating_cost = 50  # $/ton
    cutoffs = []
    npvs = []
    
    for year in range(mine_life):
        remaining_years = mine_life - year
        future_prices = prices[year:]
        
        # Bu yıl için optimal cut-off
        current_price = prices[year]
        net_value = (current_price - 25) * recovery  # 25$ satış maliyeti
        
        # Fırsat maliyeti hesabı (basitleştirilmiş)
        if remaining_years > 5:
            opportunity_factor = 1.2  # Yüksek fırsat maliyeti
        elif remaining_years > 2:
            opportunity_factor = 1.0
        else:
            opportunity_factor = 0.8  # Düşük fırsat maliyeti
        
        optimal_cutoff = (operating_cost * opportunity_factor * 31.1) / net_value
        cutoffs.append(optimal_cutoff)
        
        # NPV hesabı (basitleştirilmiş)
        future_cashflows = [(fp - base_price) * 1000000 / (1 + discount_rate) ** i 
                           for i, fp in enumerate(future_prices)]
        npv = sum(future_cashflows)
        npvs.append(npv / 1000000)  # Milyon $ cinsinden
    
    # Sonuçları göster
    st.markdown("### 📊 Dinamik Strateji Sonuçları")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Ortalama Cut-off", f"{np.mean(cutoffs):.2f} g/t", 
                 f"{(np.mean(cutoffs) - base_cutoff):.2f}")
    with col2:
        st.metric("Cut-off Aralığı", f"{min(cutoffs):.2f} - {max(cutoffs):.2f} g/t")
    with col3:
        st.metric("Ortalama Fiyat", f"${np.mean(prices):.0f}/oz")
    with col4:
        st.metric("Toplam NPV", f"${sum(npvs):.1f}M")
    
    # Grafikler
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Metal Fiyat Projeksiyonu', 'Dinamik Cut-off Grade',
                       'NPV Değişimi', 'Kümülatif Üretim'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Fiyat grafiği
    fig.add_trace(
        go.Scatter(x=years, y=prices, mode='lines+markers', name='Metal Fiyatı',
                  line=dict(width=3, color='gold')),
        row=1, col=1
    )
    fig.add_hline(y=base_price, line_dash="dash", line_color="gray", row=1, col=1)
    
    # Cut-off grafiği
    fig.add_trace(
        go.Scatter(x=years, y=cutoffs, mode='lines+markers', name='Dinamik Cut-off',
                  line=dict(width=3, color='red')),
        row=1, col=2
    )
    fig.add_hline(y=base_cutoff, line_dash="dash", line_color="gray", row=1, col=2)
    
    # NPV grafiği
    fig.add_trace(
        go.Scatter(x=years, y=npvs, mode='lines+markers', name='Yıllık NPV',
                  line=dict(width=3, color='green')),
        row=2, col=1
    )
    
    # Kümülatif üretim (örnek)
    annual_production = [processing_capacity] * mine_life
    cumulative_production = np.cumsum(annual_production)
    
    fig.add_trace(
        go.Scatter(x=years, y=cumulative_production, mode='lines+markers', 
                  name='Kümülatif Üretim', line=dict(width=3, color='blue')),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Strateji tablosu
    st.markdown("### 📋 Yıllık Strateji Tablosu")
    
    df_strategy = pd.DataFrame({
        'Yıl': years + 1,
        'Metal Fiyatı ($/oz)': [f"${p:.0f}" for p in prices],
        'Cut-off Grade (g/t)': [f"{c:.2f}" for c in cutoffs],
        'Beklenen NPV ($M)': [f"{npv:.1f}" for npv in npvs],
        'Üretim (Mt)': [f"{prod:.1f}" for prod in annual_production],
        'Strateji': ['Yüksek Cut-off' if c > base_cutoff + 0.5 else 
                    'Düşük Cut-off' if c < base_cutoff - 0.5 else 
                    'Normal' for c in cutoffs]
    })
    
    st.dataframe(df_strategy, use_container_width=True)

def facility_capacity_optimization():
    st.markdown('<h2 class="section-header">🏭 Tesis Kapasitesi Optimizasyonu</h2>', unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Mevcut Tesis Durumu")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Madencilik")
        current_mine_cap = st.number_input("Mevcut Maden Kapasitesi (Mt/yıl)", value=10.0, step=0.5)
        mine_utilization = st.slider("Maden Kapasite Kullanımı (%)", 60, 100, 85)
        mine_expand_cost = st.number_input("Maden Genişletme Maliyeti ($M/Mt)", value=50.0, step=5.0)
        
    with col2:
        st.markdown("#### İşleme")
        current_mill_cap = st.number_input("Mevcut Değirmen Kapasitesi (Mt/yıl)", value=8.0, step=0.5)
        mill_utilization = st.slider("Değirmen Kapasite Kullanımı (%)", 70, 100, 90)
        mill_expand_cost = st.number_input("Değirmen Genişletme Maliyeti ($M/Mt)", value=80.0, step=5.0)
        
    with col3:
        st.markdown("#### Finansal")
        metal_price = st.number_input("Metal Fiyatı ($/oz)", value=1500.0, step=10.0)
        recovery = st.slider("Verim (%)", 80, 95, 87) / 100
        operating_margin = st.number_input("Operasyon Marjı ($/ton)", value=25.0, step=1.0)
    
    # Optimizasyon seçenekleri
    st.markdown("### 🎯 Optimizasyon Seçenekleri")
    
    expansion_options = st.multiselect(
        "Hangi genişletmeleri değerlendirmek istiyorsunuz?",
        ["Maden Kapasitesi +25%", "Maden Kapasitesi +50%", 
         "Değirmen Kapasitesi +25%", "Değirmen Kapasitesi +50%",
         "Her İkisi +25%", "Her İkisi +50%"],
        default=["Maden Kapasitesi +25%", "Değirmen Kapasitesi +25%"]
    )
    
    payback_period = st.slider("Maksimum Geri Ödeme Süresi (yıl)", 3, 10, 5)
    min_irr = st.slider("Minimum İç Verim Oranı (%)", 15, 30, 20) / 100
    
    # Senaryo analizi
    scenarios = []
    
    for option in expansion_options:
        scenario = {"name": option}
        
        if "Maden" in option and "25%" in option:
            new_mine_cap = current_mine_cap * 1.25
            new_mill_cap = current_mill_cap
            capex = (new_mine_cap - current_mine_cap) * mine_expand_cost
        elif "Maden" in option and "50%" in option:
            new_mine_cap = current_mine_cap * 1.5
            new_mill_cap = current_mill_cap
            capex = (new_mine_cap - current_mine_cap) * mine_expand_cost
        elif "Değirmen" in option and "25%" in option:
            new_mine_cap = current_mine_cap
            new_mill_cap = current_mill_cap * 1.25
            capex = (new_mill_cap - current_mill_cap) * mill_expand_cost
        elif "Değirmen" in option and "50%" in option:
            new_mine_cap = current_mine_cap
            new_mill_cap = current_mill_cap * 1.5
            capex = (new_mill_cap - current_mill_cap) * mill_expand_cost
        elif "Her İkisi" in option and "25%" in option:
            new_mine_cap = current_mine_cap * 1.25
            new_mill_cap = current_mill_cap * 1.25
            capex = ((new_mine_cap - current_mine_cap) * mine_expand_cost + 
                    (new_mill_cap - current_mill_cap) * mill_expand_cost)
        else:  # Her ikisi +50%
            new_mine_cap = current_mine_cap * 1.5
            new_mill_cap = current_mill_cap * 1.5
            capex = ((new_mine_cap - current_mine_cap) * mine_expand_cost + 
                    (new_mill_cap - current_mill_cap) * mill_expand_cost)
        
        # Yeni üretim kapasitesi (kısıtlayıcı faktör)
        new_production = min(new_mine_cap, new_mill_cap)
        current_production = min(current_mine_cap, current_mill_cap)
        
        # Ek üretim ve gelir
        additional_production = new_production - current_production
        additional_revenue = additional_production * operating_margin * 1000000  # $M
        
        # Basit geri ödeme süresi
        simple_payback = capex / additional_revenue if additional_revenue > 0 else 999
        
        # NPV hesabı (basitleştirilmiş)
        discount_rate = 0.15
        cash_flows = [additional_revenue] * 10  # 10 yıl varsayımı
        npv = -capex + sum([cf / (1 + discount_rate) ** i for i, cf in enumerate(cash_flows, 1)])
        
        # IRR hesabı (yaklaşık)
        irr_approx = (additional_revenue / capex) if capex > 0 else 0
        
        scenario.update({
            "mine_cap": new_mine_cap,
            "mill_cap": new_mill_cap,
            "production": new_production,
            "additional_prod": additional_production,
            "capex": capex,
            "additional_revenue": additional_revenue,
            "payback": simple_payback,
            "npv": npv,
            "irr": irr_approx
        })
        
        scenarios.append(scenario)
    
    # Sonuçları göster
    if scenarios:
        st.markdown("### 📊 Senaryo Karşılaştırması")
        
        # En iyi seçenekleri bul
        best_npv = max(scenarios, key=lambda x: x["npv"])
        best_payback = min([s for s in scenarios if s["payback"] < 999], 
                          key=lambda x: x["payback"], default=None)
        
        if best_payback:
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"🏆 En Yüksek NPV: {best_npv['name']} (${best_npv['npv']:.1f}M)")
            with col2:
                st.success(f"⚡ En Hızlı Geri Ödeme: {best_payback['name']} ({best_payback['payback']:.1f} yıl)")
        
        # Senaryo tablosu
        df_scenarios = pd.DataFrame([{
            'Senaryo': s['name'],
            'Yeni Maden Kap. (Mt)': f"{s['mine_cap']:.1f}",
            'Yeni Değirmen Kap. (Mt)': f"{s['mill_cap']:.1f}",
            'Ek Üretim (Mt)': f"{s['additional_prod']:.1f}",
            'CapEx ($M)': f"{s['capex']:.1f}",
            'Ek Gelir ($M/yıl)': f"{s['additional_revenue']:.1f}",
            'Geri Ödeme (yıl)': f"{s['payback']:.1f}" if s['payback'] < 999 else "∞",
            'NPV ($M)': f"{s['npv']:.1f}",
            'IRR (%)': f"{s['irr']*100:.1f}",
            'Değerlendirme': '✅ Uygun' if s['payback'] <= payback_period and s['irr'] >= min_irr 
                           else '❌ Uygun Değil'
        } for s in scenarios])
        
        st.dataframe(df_scenarios, use_container_width=True)
        
        # Grafik
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=[s['payback'] for s in scenarios if s['payback'] < 999],
            y=[s['npv'] for s in scenarios if s['payback'] < 999],
            mode='markers+text',
            text=[s['name'].split(' ')[0] + ' ' + s['name'].split(' ')[-1] for s in scenarios if s['payback'] < 999],
            textposition="top center",
            marker=dict(
                size=[s['additional_prod']*10 for s in scenarios if s['payback'] < 999],
                color=[s['irr'] for s in scenarios if s['payback'] < 999],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="IRR")
            ),
            name='Senaryolar'
        ))
        
        # Kabul edilebilir bölge
        fig.add_vline(x=payback_period, line_dash="dash", line_color="red", 
                     annotation_text="Max Geri Ödeme")
        fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="NPV=0")
        
        fig.update_layout(
            title="Senaryo Değerlendirmesi (Balon Boyutu: Ek Üretim, Renk: IRR)",
            xaxis_title="Geri Ödeme Süresi (yıl)",
            yaxis_title="NPV ($M)",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Ana uygulama kontrolü
def main():
    if app_mode == "🏠 Ana Sayfa":
        home_page()
    elif app_mode == "📊 Temel Cut-off Grade Hesaplama":
        basic_cutoff_calculator()
    elif app_mode == "⚖️ İki Proses Karşılaştırması":
        process_comparison()
    elif app_mode == "💰 NPV ve Fırsat Maliyeti Analizi":
        npv_opportunity_analysis()
    elif app_mode == "🔄 Harmanlama Optimizasyonu":
        blending_optimization()
    elif app_mode == "📈 Dinamik Cut-off Grade Stratejisi":
        dynamic_cutoff_strategy()
    elif app_mode == "🏭 Tesis Kapasitesi Optimizasyonu":
        facility_capacity_optimization()

# Uygulamayı çalıştır
if __name__ == "__main__":
    main()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>📚 <strong>Cut-off Grade Hesaplama Uygulaması</strong></p>
        <p>Jean-Michel Rendu'nun "An Introduction to Cut-off Grade Estimation" kitabına dayalı</p>
        <p>🔬 Akademik ve eğitim amaçlı kullanım için tasarlanmıştır</p>
    </div>
    """, unsafe_allow_html=True)
    