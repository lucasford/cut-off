# Kütüphane kontrol ve yükleme
import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Gerekli kütüphaneleri kontrol et ve yükle
required_packages = {
    'streamlit': 'streamlit>=1.28.0',
    'plotly': 'plotly>=5.15.0', 
    'pandas': 'pandas>=1.5.0',
    'numpy': 'numpy>=1.21.0'
}

for package_name, package_spec in required_packages.items():
    try:
        __import__(package_name)
    except ImportError:
        print(f"{package_name} yüklenmiyor, yükleniyor...")
        install_package(package_spec)

# Ana import'lar
import streamlit as st
import numpy as np
import pandas as pd

# Plotly import'ını try-except ile yap
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    st.error("⚠️ Plotly yüklenemedi. Grafik görselleştirme çalışmayabilir.")
    PLOTLY_AVAILABLE = False
    # Plotly olmadan da çalışabilir hale getir
    class DummyPlotly:
        def Figure(self): return None
        def Scatter(self, **kwargs): return None
    go = DummyPlotly()
    px = DummyPlotly()

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
    .error-box {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #f44336;
        color: #c62828;
    }
</style>
""", unsafe_allow_html=True)

# Plotly uyarısı
if not PLOTLY_AVAILABLE:
    st.markdown("""
    <div class="error-box">
        ⚠️ <strong>Grafik Kütüphanesi Sorunu:</strong><br>
        Plotly kütüphanesi yüklenemedi. Hesaplamalar çalışacak ancak grafikler görüntülenmeyecek.
        <br><br>
        <strong>Çözüm:</strong> requirements.txt dosyasında plotly>=5.15.0 olduğundan emin olun.
    </div>
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

def show_plotly_chart(fig, use_container_width=True):
    """Plotly grafiğini güvenli şekilde göster"""
    if PLOTLY_AVAILABLE and fig is not None:
        st.plotly_chart(fig, use_container_width=use_container_width)
    else:
        st.error("📊 Grafik görüntülenemiyor - Plotly kütüphanesi gerekli")

def create_simple_line_chart(x_data, y_data, title="Grafik", x_label="X", y_label="Y"):
    """Basit çizgi grafiği oluştur"""
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers'))
        fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
        return fig
    else:
        # Plotly yoksa pandas ile basit grafik göster
        df = pd.DataFrame({x_label: x_data, y_label: y_data})
        st.line_chart(df.set_index(x_label))
        return None

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
    
    if not PLOTLY_AVAILABLE:
        st.warning("""
        ⚠️ **Grafik Kütüphanesi Uyarısı:** 
        Bazı görselleştirmeler çalışmayabilir. Tüm hesaplamalar normal şekilde çalışacaktır.
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
            conversion_f
