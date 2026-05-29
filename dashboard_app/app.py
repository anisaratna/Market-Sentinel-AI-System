import streamlit as st
import pandas as pd
import psycopg2
import os
import plotly.express as px
from groq import Groq
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- 1. SETUP & DATABASE CONNECTION ---
DATABASE_URL = os.getenv("DATABASE_URL")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@st.cache_data(ttl=600)
def get_data():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        query = "SELECT topic, source, title, sentiment, score, created_at FROM sentiment_history ORDER BY created_at DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame()

# --- 2. AI Q&A LOGIC (RAG-LITE) ---
def ask_ai(question, context_titles, topic_name):
    context = "\n- ".join(context_titles)
    prompt = f"""
    You are a Market Intelligence Assistant. Answer the user's question based ONLY on the provided news context for the topic '{topic_name}'.
    If the answer isn't in the context, say you don't have enough data yet.
    Context (Recent News):
    {context}
    User Question: {question}
    """
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {e}"

# --- 3. UI HELPER: CUSTOM CARDS ---
def draw_ai_card(icon, title, content):
    st.markdown(f"""
        <div style="
            background-color: #1e1e1e; 
            padding: 20px; 
            border-left: 5px solid #00cc96; 
            border-radius: 10px; 
            margin-bottom: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        ">
            <h3 style="color: #00cc96; margin: 0; font-size: 24px;">{icon} {title}</h3>
            <p style="color: #ffffff; font-size: 18px; line-height: 1.6; margin-top: 10px;">{content}</p>
        </div>
    """, unsafe_allow_html=True)


# --- 4. PAGE CONFIGURATION ---
st.set_page_config(page_title="Market Sentinel Intelligence", layout="wide")

st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 42px; font-weight: bold; }
    [data-testid="stMetricLabel"] { font-size: 20px; }
    h1 { font-size: 50px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🌐 Market Sentinel Dashboard")
st.markdown("Automated sentiment monitoring for global trade routes and market-moving events.")

df_raw = get_data()

if not df_raw.empty:
    # Sidebar
    st.sidebar.header("🔍 Filter Analytics")
    available_topics = ["All Topics"] + list(df_raw['topic'].unique())
    selected_topic = st.sidebar.selectbox("Select Intelligence Feed:", available_topics)

    if selected_topic == "All Topics":
        df = df_raw.copy()
    else:
        df = df_raw[df_raw['topic'] == selected_topic].copy()

    # --- ROW 1: DYNAMIC METRICS ---
    st.subheader(f"📊 Intelligence Summary: {selected_topic}")
    m1, m2, m3, m4, m5 = st.columns(5)
    
    with m1:
        st.metric("Total Articles", len(df))
    with m2:
        pos = len(df[df['sentiment'] == 'positive'])
        st.metric("✅ Positive", pos)
    with m3:
        neu = len(df[df['sentiment'] == 'neutral'])
        st.metric("⚪ Neutral", neu)
    with m4:
        neg = len(df[df['sentiment'] == 'negative'])
        st.metric("🔴 Negative", neg)
    with m5:
        avg_score = df['score'].mean()
        st.metric("Avg. Confidence", f"{round(avg_score*100, 1)}%")

    # --- ROW 2: SENTIMENT TRENDS ---
    st.markdown("---")
    st.subheader(f"📈 Trend Analysis")
    
    df['timestamp'] = pd.to_datetime(df['created_at'])
    
    # Kelompokkan per 4 jam 
    trend_df = df.groupby([df['timestamp'].dt.floor('4h'), 'sentiment']).size().reset_index(name='count')
    trend_df.columns = ['time_period', 'sentiment', 'count']
    trend_df = trend_df.sort_values('time_period')

    fig = px.line(trend_df, x='time_period', y='count', color='sentiment', 
                  color_discrete_map={'positive':'#00cc96', 'neutral':'#636efa', 'negative':'#ef553b'},
                  markers=True)
    
    fig.update_layout(
        font=dict(size=14),
        legend=dict(font=dict(size=14)),
        xaxis=dict(
            title=dict(text="Time Interval (4-Hourly)", font=dict(size=16)),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title=dict(text="Volume of News", font=dict(size=16)),
            tickfont=dict(size=12)
        ),
        template="plotly_dark",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

   # --- ROW 3: TOPIC MODELING ---
    st.markdown("---")
    st.subheader("🎯 Key Topics & Keyword Cloud")
    
    col_wc, col_bar = st.columns([1, 1.25])

    text = " ".join(df['title'].tolist())
    custom_stopwords = set(['market','semiconductor', 'global', 'inflation', 'iran', 'trump', 'a', 'us', 'as', 'u', 's', 'in', 'the', 'of', 'and', 'to', 'on', 'for', 'with', 'by', 'is', 'at', 'from', 'ai', 'impact', 'export', 'chip', 'strait', 'hormuz', 'says', 'amid', 'after', 'today', 'new'])
    
    with col_wc:
        wc = WordCloud(
            width=600, 
            height=500, 
            background_color="#0e1117", 
            colormap="viridis", 
            stopwords=custom_stopwords
        ).generate(text)
        
        fig_wc, ax = plt.subplots(facecolor='#0e1117') 
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.tight_layout(pad=0)
        st.pyplot(fig_wc)

    with col_bar:
        # Top 10 words
        words = pd.Series(" ".join(df['title']).lower().split()).value_counts()
        words = words[~words.index.isin(list(custom_stopwords))].head(10).reset_index()
        words.columns = ['Word', 'Frequency']
        
        words = words.sort_values(by='Frequency', ascending=True)
        
        fig_bar = px.bar(
            words, 
            x='Frequency', 
            y='Word', 
            orientation='h', 
            template="plotly_dark",
            color_discrete_sequence=['#00cc96']
        )
        
        fig_bar.update_layout(
            height=450,
            margin=dict(l=150, r=20, t=30, b=20), 
            font=dict(size=14),
            xaxis=dict(title=dict(font=dict(size=16)), tickfont=dict(size=14)),
            yaxis=dict(title=dict(text=""), tickfont=dict(size=16)) 
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- ROW 4: GEN-AI Q&A (RAG-LITE) ---
    st.markdown("---")
    st.subheader(f"💬 Ask anything about {selected_topic}")
    user_q = st.text_input("Example: What is the main cause of the current tension?", placeholder="Type your question here...")
    
    if user_q:
        with st.spinner("AI is checking records..."):
            context_titles = df['title'].head(100).tolist()
            answer = ask_ai(user_q, context_titles, selected_topic)
            st.markdown(f"""
            <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border-left: 5px solid #636efa;">
                <p style="font-size: 18px;"><b>AI Response:</b><br>{answer}</p>
            </div>
            """, unsafe_allow_html=True)

    # --- ROW 5: DETAILED LOGS ---
    st.subheader("📰 Recent Intelligence Logs")
    def color_sentiment(val):
        color = '#ef553b' if val == 'negative' else '#00cc96' if val == 'positive' else '#636efa'
        return f'color: {color}; font-weight: bold'

    st.dataframe(
        df[['created_at', 'topic', 'source', 'title', 'sentiment', 'score']]
        .style.map(color_sentiment, subset=['sentiment']), 
        use_container_width=True
    )

else:
    st.warning("No data found in database. Automated ingestor is likely still processing.")

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**System Status:** Running 🟢
                
**Architecture:**
- **Pipeline:** GitHub Actions
- **Warehouse:** PostgreSQL (Neon)
- **Sentiment AI:** FinBERT
- **Contextual AI:** Llama 3 (Groq)
- **Delivery:** FastAPI & Docker
""")