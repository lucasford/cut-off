import streamlit as st
import numpy as np
import pandas as pd
import math

# Plotly'yi güvenli şekilde import et
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Sayfa yapılandırması
st.set_page_config(
    page_title="Cut-off Grade Calculator",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stil
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.3rem;
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
    .success-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Ana başlık
st.markdown('<h1 class="main-header">⛏️ Cut-off Grade Calculator</h1>', unsafe_allow_html=True)
st.markdown("*Based on Jean-Michel Rendu's 'An Introduction to Cut-off Grade Estimation'*")

# Sidebar
st.sidebar.title("📋 Module Selection")
app_mode = st.sidebar.selectbox(
    "Choose calculation module:",
    [
        "🏠 Home",
        "📊 Basic Cut-off Grade",
        "⚖️ Process Comparison", 
        "💰 NPV & Opportunity Cost",
        "🔄 Blending Optimization",
        "📈 Dynamic Strategy",
        "🏭 Capacity Optimization"
    ]
)

def show_chart(x_data, y_data, title, x_label, y_label, chart_type="line"):
    """Charts with fallback"""
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        if chart_type == "line":
            fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers', name=y_label))
        elif chart_type == "bar":
            fig.add_trace(go.Bar(x=x_data, y=y_data, name=y_label))
        fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label, height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Streamlit native charts
        df = pd.DataFrame({x_label: x_data, y_label: y_data})
        if chart_type == "line":
            st.line_chart(df.set_index(x_label))
        elif chart_type == "bar":
            st.bar_chart(df.set_index(x_label))
        st.markdown(f"**{title}**")

def home_page():
    st.markdown('<h2 class="section-header">📚 About This Application</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 Basic Calculations
        - Breakeven cut-off grade
        - Mill vs Mine cut-off
        - Grade-tonnage relationships
        - Utility functions
        """)
    
    with col2:
        st.markdown("""
        ### 💡 Advanced Analysis
        - NPV optimization
        - Opportunity cost calculation
        - Capacity constraints
        - Risk analysis
        """)
    
    with col3:
        st.markdown("""
        ### 🔧 Practical Tools
        - Interactive charts
        - Scenario comparison
        - Automatic reporting
        - Parameter optimization
        """)
    
    st.markdown('<h2 class="section-header">📖 Book Chapters</h2>', unsafe_allow_html=True)
    
    chapters = {
        "Chapter 1": "Introduction and Basic Concepts",
        "Chapter 2": "General Concepts and Utility Functions", 
        "Chapter 3": "Breakeven Cut-off Grade Calculations",
        "Chapter 4": "Capacity Constraints and Opportunity Costs",
        "Chapter 5": "Geological Constraints and Opportunity Costs",
        "Chapter 6": "Cut-off Grade and Mine Planning",
        "Chapter 7": "Cost Analysis and Costs to Include",
        "Chapter 8": "Blending Strategy",
        "Chapter 9": "Conclusions and Recommendations"
    }
    
    for chapter, description in chapters.items():
        st.markdown(f"**{chapter}:** {description}")
    
    # Status
    if PLOTLY_AVAILABLE:
        st.success("✅ All features available - Plotly graphics enabled")
    else:
        st.warning("⚠️ Basic mode - Using Streamlit native charts")

def basic_cutoff_calculator():
    st.markdown('<h2 class="section-header">📊 Basic Cut-off Grade Calculator</h2>', unsafe_allow_html=True)
    
    # Parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💎 Mine Parameters")
        metal_price = st.number_input("Metal Price ($/oz or $/lb)", value=1400.0, step=10.0)
        recovery = st.slider("Recovery (%)", 50, 95, 85) / 100
        cost_of_sales = st.number_input("Cost of Sales ($/oz or $/lb)", value=50.0, step=5.0)
        
        st.markdown("### ⛏️ Mining Costs")
        mining_cost_ore = st.number_input("Ore Mining Cost ($/ton)", value=4.50, step=0.1)
        mining_cost_waste = st.number_input("Waste Mining Cost ($/ton)", value=3.00, step=0.1)
        
    with col2:
        st.markdown("### 🏭 Processing Costs")
        processing_cost = st.number_input("Processing Cost ($/ton)", value=75.0, step=1.0)
        overhead_cost = st.number_input("Overhead Cost ($/ton)", value=15.0, step=1.0)
        
        st.markdown("### 📏 Unit Conversion")
        unit_conversion = st.selectbox("Metal Unit", ["oz/ton (Gold)", "% (Copper)"])
        if unit_conversion == "oz/ton (Gold)":
            conversion_factor = 31.1035  # g/ton to oz/ton
            unit_display = "oz/t"
        else:
            conversion_factor = 2205  # % to lb/ton
            unit_display = "%"
    
    # Calculations
    net_value = (metal_price - cost_of_sales) * recovery
    
    # Cut-off grades
    total_ore_cost = mining_cost_ore + processing_cost + overhead_cost
    mine_cutoff = total_ore_cost / (net_value * conversion_factor)
    
    mill_cost = processing_cost + overhead_cost
    mill_cutoff = mill_cost / (net_value * conversion_factor)
    
    waste_cost = mining_cost_waste
    
    # Results
    st.markdown('<h2 class="section-header">📊 Calculation Results</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Mine Cut-off", f"{mine_cutoff:.4f} {unit_display}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Mill Cut-off", f"{mill_cutoff:.4f} {unit_display}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Net Value", f"${net_value:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("Break-even", f"${total_ore_cost:.2f}/ton")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Grade-Tonnage Analysis
    st.markdown('<h2 class="section-header">📈 Grade-Tonnage Analysis</h2>', unsafe_allow_html=True)
    
    max_tonnage = st.slider("Maximum Tonnage (million tons)", 1.0, 100.0, 50.0)
    
    # Generate example data
    cutoff_range = np.linspace(mine_cutoff * 0.5, mine_cutoff * 2.5, 20)
    tonnages = [max_tonnage * np.exp(-3 * (cg - mine_cutoff * 0.5) / mine_cutoff) for cg in cutoff_range]
    avg_grades = [mine_cutoff * 0.4 + cg * 0.6 for cg in cutoff_range]
    metal_content = [t * ag for t, ag in zip(tonnages, avg_grades)]
    
    # Create charts
    col1, col2 = st.columns(2)
    
    with col1:
        show_chart(cutoff_range, tonnages, "Tonnage vs Cut-off Grade", 
                  f"Cut-off Grade ({unit_display})", "Tonnage (Mt)")
    
    with col2:
        show_chart(cutoff_range, avg_grades, "Average Grade vs Cut-off", 
                  f"Cut-off Grade ({unit_display})", f"Average Grade ({unit_display})")
    
    # Summary table
    df_summary = pd.DataFrame({
        f'Cut-off ({unit_display})': [f"{cg:.4f}" for cg in cutoff_range[::4]],
        'Tonnage (Mt)': [f"{t:.1f}" for t in tonnages[::4]],
        f'Avg Grade ({unit_display})': [f"{ag:.4f}" for ag in avg_grades[::4]],
        'Metal Content': [f"{mc:.1f}" for mc in metal_content[::4]]
    })
    
    st.dataframe(df_summary, use_container_width=True)

def process_comparison():
    st.markdown('<h2 class="section-header">⚖️ Process Comparison</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔄 Process 1 (e.g., Heap Leach)")
        recovery1 = st.slider("Recovery 1 (%)", 30, 80, 60, key="r1") / 100
        cost1 = st.number_input("Processing Cost 1 ($/ton)", value=9.0, step=0.5, key="c1")
        mining_cost1 = st.number_input("Mining Cost 1 ($/ton)", value=5.0, step=0.1, key="m1")
        
    with col2:
        st.markdown("### ⚙️ Process 2 (e.g., Mill)")
        recovery2 = st.slider("Recovery 2 (%)", 80, 98, 87, key="r2") / 100
        cost2 = st.number_input("Processing Cost 2 ($/ton)", value=35.0, step=1.0, key="c2")
        mining_cost2 = st.number_input("Mining Cost 2 ($/ton)", value=5.5, step=0.1, key="m2")
    
    # Common parameters
    metal_price = st.number_input("Metal Price ($/oz)", value=1600.0, step=10.0)
    cost_of_sales = st.number_input("Cost of Sales ($/oz)", value=50.0, step=5.0)
    
    # Calculations
    net_value = metal_price - cost_of_sales
    
    # Create grade range
    grades = np.linspace(0, 8, 100)  # g/t
    
    # Utility functions
    U1 = grades * recovery1 * net_value / 31.1035 - (mining_cost1 + cost1)
    U2 = grades * recovery2 * net_value / 31.1035 - (mining_cost2 + cost2)
    U_max = np.maximum(U1, U2)
    
    # Find cut-off
    diff = np.abs(U1 - U2)
    cutoff_idx = np.argmin(diff)
    cutoff_grade = grades[cutoff_idx]
    
    # Waste cut-offs
    waste_cutoff1 = (mining_cost1 + cost1) * 31.1035 / (recovery1 * net_value)
    waste_cutoff2 = (mining_cost2 + cost2) * 31.1035 / (recovery2 * net_value)
    
    # Results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Process 1-2 Cut-off", f"{cutoff_grade:.2f} g/t")
    with col2:
        st.metric("Waste-Process 1", f"{waste_cutoff1:.2f} g/t")  
    with col3:
        st.metric("Waste-Process 2", f"{waste_cutoff2:.2f} g/t")
    
    # Chart
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=grades, y=U1, mode='lines', name='Process 1 Utility', 
                                line=dict(width=3, color='blue')))
        fig.add_trace(go.Scatter(x=grades, y=U2, mode='lines', name='Process 2 Utility',
                                line=dict(width=3, color='red')))
        fig.add_trace(go.Scatter(x=grades, y=U_max, mode='lines', 
                                name='Maximum Utility', line=dict(width=4, color='green')))
        
        fig.add_vline(x=cutoff_grade, line_dash="dash", line_color="black",
                     annotation_text=f"Cut-off: {cutoff_grade:.2f} g/t")
        
        fig.update_layout(
            title="Process Comparison - Utility Functions",
            xaxis_title="Grade (g/t)",
            yaxis_title="Utility ($/ton)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        df_utility = pd.DataFrame({
            'Grade': grades,
            'Process 1': U1,
            'Process 2': U2,
            'Maximum': U_max
        })
        st.line_chart(df_utility.set_index('Grade'))

def npv_analysis():
    st.markdown('<h2 class="section-header">💰 NPV and Opportunity Cost Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Project Parameters")
        initial_npv = st.number_input("Initial NPV ($ million)", value=800.0, step=10.0)
        discount_rate = st.slider("Discount Rate (%)", 5, 20, 15) / 100
        mine_life = st.slider("Mine Life (years)", 5, 20, 10)
        
    with col2:
        st.markdown("### 🏭 Capacity Constraints")
        mill_capacity = st.number_input("Mill Capacity (Mt/year)", value=50.0, step=1.0)
        mine_capacity = st.number_input("Mine Capacity (Mt/year)", value=72.0, step=1.0)
    
    # NPV over time
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
    
    # Opportunity costs
    mill_opp_cost = [discount_rate * npv / mill_capacity for npv in npv_remaining]
    mine_opp_cost = [discount_rate * npv / mine_capacity for npv in npv_remaining]
    
    # Results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current NPV", f"${initial_npv:.0f}M")
    with col2:
        st.metric("Mill Opp. Cost", f"${mill_opp_cost[0]:.2f}/t")
    with col3:
        st.metric("Mine Opp. Cost", f"${mine_opp_cost[0]:.2f}/t")
    
    # Charts
    show_chart(years, npv_remaining, "NPV Over Time", "Year", "NPV ($M)")
    
    # Summary table
    df_npv = pd.DataFrame({
        'Year': years,
        'Remaining NPV ($M)': [f"{npv:.1f}" for npv in npv_remaining],
        'Mill Opp. Cost ($/t)': [f"{cost:.2f}" for cost in mill_opp_cost],
        'Mine Opp. Cost ($/t)': [f"{cost:.2f}" for cost in mine_opp_cost]
    })
    
    st.dataframe(df_npv, use_container_width=True)

def simple_blending():
    st.markdown('<h2 class="section-header">🔄 Simple Blending Optimization</h2>', unsafe_allow_html=True)
    
    st.markdown("### 📊 Two Stockpile Blending")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Stockpile 1")
        tonnage1 = st.number_input("Tonnage 1 (kt)", value=20, step=1, key="t1")
        grade1_1 = st.number_input("Sulfur 1 (%)", value=3.5, step=0.1, key="s1")
        grade1_2 = st.number_input("Gold 1 (g/t)", value=40, step=1, key="g1")
    
    with col2:
        st.markdown("#### Stockpile 2")
        tonnage2 = st.number_input("Tonnage 2 (kt)", value=40, step=1, key="t2")
        grade2_1 = st.number_input("Sulfur 2 (%)", value=1.2, step=0.1, key="s2")
        grade2_2 = st.number_input("Gold 2 (g/t)", value=90, step=1, key="g2")
    
    # Target
    target_sulfur = st.number_input("Target Sulfur (%)", value=1.5, step=0.1)
    
    # Calculate blend proportions
    # p1 * grade1_1 + p2 * grade2_1 = target_sulfur
    # p1 + p2 = 1
    # Solve: p1 = (target_sulfur - grade2_1) / (grade1_1 - grade2_1)
    
    if grade1_1 != grade2_1:
        p1 = (target_sulfur - grade2_1) / (grade1_1 - grade2_1)
        p2 = 1 - p1
        
        if 0 <= p1 <= 1 and 0 <= p2 <= 1:
            # Calculate maximum tonnage
            max_tonnage1 = tonnage1 / p1 if p1 > 0 else float('inf')
            max_tonnage2 = tonnage2 / p2 if p2 > 0 else float('inf')
            max_tonnage = min(max_tonnage1, max_tonnage2)
            
            # Used tonnages
            used_tonnage1 = max_tonnage * p1
            used_tonnage2 = max_tonnage * p2
            
            # Blended grade
            blended_gold = p1 * grade1_2 + p2 * grade2_2
            
            # Results
            st.markdown("### ✅ Blending Results")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Max Tonnage", f"{max_tonnage:.0f} kt")
            with col2:
                st.metric("Stock 1 Ratio", f"{p1*100:.1f}%")
            with col3:
                st.metric("Stock 2 Ratio", f"{p2*100:.1f}%")
            with col4:
                st.metric("Blended Gold", f"{blended_gold:.1f} g/t")
            
            # Details table
            df_blend = pd.DataFrame({
                'Stockpile': ['Stock 1', 'Stock 2', 'BLEND'],
                'Available (kt)': [tonnage1, tonnage2, tonnage1 + tonnage2],
                'Used (kt)': [used_tonnage1, used_tonnage2, max_tonnage],
                'Ratio (%)': [p1*100, p2*100, 100],
                'Sulfur (%)': [grade1_1, grade2_1, target_sulfur],
                'Gold (g/t)': [grade1_2, grade2_2, blended_gold]
            })
            
            st.dataframe(df_blend, use_container_width=True)
            
        else:
            st.error("❌ Target sulfur not achievable with these stockpiles!")
    else:
        st.error("❌ Stockpiles have same sulfur grade - blending not needed!")

# Main application control
def main():
    if app_mode == "🏠 Home":
        home_page()
    elif app_mode == "📊 Basic Cut-off Grade":
        basic_cutoff_calculator()
    elif app_mode == "⚖️ Process Comparison":
        process_comparison()
    elif app_mode == "💰 NPV & Opportunity Cost":
        npv_analysis()
    elif app_mode == "🔄 Blending Optimization":
        simple_blending()
    else:
        st.info(f"""
        🚧 **{app_mode}** module is under development.
        
        Available modules:
        - Basic Cut-off Grade ✅
        - Process Comparison ✅  
        - NPV & Opportunity Cost ✅
        - Blending Optimization ✅
        """)

# Run the app
if __name__ == "__main__":
    main()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>📚 <strong>Cut-off Grade Calculator</strong></p>
        <p>Based on "An Introduction to Cut-off Grade Estimation" by Jean-Michel Rendu</p>
        <p>🔬 For academic and educational use</p>
    </div>
    """, unsafe_allow_html=True)
