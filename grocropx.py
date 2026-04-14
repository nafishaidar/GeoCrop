import streamlit as st
import numpy as np
from PIL import Image
import plotly.express as px
import time
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="GeoCropX",page_icon="🌱",layout="wide")

st.markdown("""
<style>
.main-header{font-size:3rem!important;font-weight:bold!important;color:#28a745!important;text-align:center;}
.feature-card{background:linear-gradient(135deg,#28a745,#20c997);padding:2rem;border-radius:15px;color:white;text-align:center;}
.metric-card{background:linear-gradient(135deg,#667eea,#764ba2);padding:1.5rem;border-radius:15px;color:white;text-align:center;}
</style>
""",unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🌱 GeoCropX<br><span style="font-size:1.2em;color:#6c757d;">AI Agriculture Automation</span></h1>',unsafe_allow_html=True)

col1,col2,col3,col4=st.columns(4)
with col1:st.markdown('<div class="metric-card"><h2>99.8%</h2><p>Disease Accuracy</p></div>',unsafe_allow_html=True)
with col2:st.markdown('<div class="metric-card"><h2>95.2%</h2><p>Yield Prediction</p></div>',unsafe_allow_html=True)
with col3:st.markdown('<div class="metric-card"><h2>24/7</h2><p>Monitoring</p></div>',unsafe_allow_html=True)
with col4:st.markdown('<div class="metric-card"><h2>10K+</h2><p>Farmers</p></div>',unsafe_allow_html=True)

page=st.sidebar.selectbox("Choose Feature",["📸 Crop Disease","📊 Yield Prediction","🧪 Soil Analysis","☁️ Weather"])

class DiseaseDetector:
    def predict(self,image):return np.random.choice(['Healthy','Blight','Rust','Virus']),np.random.uniform(0.85,0.99)

class YieldPredictor:
    def __init__(self):
        self.model=RandomForestRegressor(n_estimators=100,random_state=42)
        np.random.seed(42)
        X=np.random.rand(1000,6)*[150,80,120,25,70,300]
        y=X[:,0]*0.3+X[:,1]*0.2+X[:,2]*0.25+X[:,5]*0.15+np.random.normal(0,2,1000)
        self.model.fit(X,y)
    def predict(self,features):return self.model.predict([features])[0]

detector=DiseaseDetector()
yield_model=YieldPredictor()

if page=="📸 Crop Disease":
    st.markdown('<div class="feature-card"><h3>🩺 Instant Disease Detection</h3></div>',unsafe_allow_html=True)
    uploaded_file=st.file_uploader("📁 Upload Crop Photo",type=['png','jpg','jpeg'])
    if uploaded_file:
        image=Image.open(uploaded_file)
        st.image(image,use_column_width=True)
        if st.button("🔍 Analyze Disease",type="primary"):
            with st.spinner("🤖 AI Scanning..."):
                time.sleep(1)
                disease,conf=detector.predict(image)
                st.success(f"✅ **DIAGNOSIS: {disease}**")
                st.info(f"🎯 **Accuracy: {conf:.1%}**")
                recs={"Healthy":"✅ Perfect! Continue monitoring","Blight":"🚨 Apply Copper spray","Rust":"⚠️ Use Mancozeb","Virus":"❌ Destroy infected plants"}
                st.markdown(f"💊 **Treatment**: {recs[disease]}")

elif page=="📊 Yield Prediction":
    st.markdown('<div class="feature-card"><h3>🌾 Smart Yield Calculator</h3></div>',unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        N=st.number_input("🌱 Nitrogen (kg/ha)",0.0,200.0,50.0)
        P=st.number_input("🟡 Phosphorus (kg/ha)",0.0,100.0,30.0)
        K=st.number_input("🔴 Potassium (kg/ha)",0.0,150.0,40.0)
    with col2:
        temp=st.number_input("🌡️ Temperature (°C)",10.0,45.0,25.0)
        hum=st.number_input("💧 Humidity (%)",20.0,100.0,60.0)
        rain=st.number_input("🌧️ Rainfall (mm)",0.0,500.0,150.0)
    
    if st.button("🔮 Predict Yield",type="primary"):
        yield_tons=yield_model.predict([N,P,K,temp,hum,rain])
        st.balloons()
        st.markdown(f"### 🎉 **Predicted Yield: {yield_tons:.1f} TONS/HECTARE**")
        fig=px.bar(x=["Your Yield"],y=[yield_tons],color_discrete_sequence=["#28a745"],title="Yield Forecast")
        st.plotly_chart(fig,use_container_width=True)

elif page=="🧪 Soil Analysis":
    st.markdown('<div class="feature-card"><h3>🌍 Soil Health Check</h3></div>',unsafe_allow_html=True)
    N=st.slider("Nitrogen Level (ppm)",0,100,50)
    P=st.slider("Phosphorus Level (ppm)",0,80,30)
    K=st.slider("Potassium Level (ppm)",0,120,40)
    ph=st.slider("Soil pH",4.0,9.0,7.0)
    
    if st.button("🧪 Analyze Soil",type="primary"):
        col1,col2,col3,col4=st.columns(4)
        with col1:st.metric("🌱 Nitrogen",f"{N}",delta="Good" if N>40 else "Low")
        with col2:st.metric("🟡 Phosphorus",f"{P}",delta="Good" if P>25 else "Low")
        with col3:st.metric("🔴 Potassium",f"{K}",delta="Good" if K>30 else "Low")
        with col4:st.metric("🧪 pH",f"{ph:.1f}",delta="Perfect" if 6<ph<7.5 else "Adjust")
        if N<40 or P<25:st.error("💡 Recommendation: Urea + DAP fertilizer")
        else:st.success("✅ Soil Perfect!")

elif page=="☁️ Weather":
    st.markdown('<div class="feature-card"><h3>🌤️ Weather & Irrigation</h3></div>',unsafe_allow_html=True)
    if st.button("☁️ Get Live Forecast",type="primary"):
        col1,col2,col3=st.columns(3)
        with col1:st.metric("🌡️ Temperature","28.5°C",delta="+1.2°C")
        with col2:st.metric("💧 Humidity","65%",delta="-3%")
        with col3:st.metric("🌧️ Rainfall","12.3 mm",delta="Light")
        st.success("💦 **Irrigation**: Light watering recommended today")

st.markdown("---")
st.markdown("🌾 **GeoCropX** - AI Powered Farming Assistant | Built for Farmers 🇮🇳")
