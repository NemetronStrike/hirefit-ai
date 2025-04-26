import streamlit as st
st.set_option('server.enableCORS', False)
st.set_option('server.enableXsrfProtection', False)
st.set_option('server.fileWatcherType', 'none')
from file_handler import get_text
from analyzer import calculate_match_score
from gemini_utils import get_structured_analysis, generate_resume_from_prompt
from streamlit_lottie import st_lottie
import requests

# 🚀 Streamlit Config
st.set_page_config(
    page_title="HireFit AI – Resume to JD Matcher",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 Enhanced CSS Styling
st.markdown("""
    <style>
    /* ====== GLOBAL RESET ====== */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: #1D4E89;
        color: #ffffff;
        margin: 0 !important;
        padding: 0 !important;
        height: 100vh;
        overflow: hidden !important;
    }

    /* ====== MAIN CONTAINER FIXES ====== */
    .stApp {
        background-color: #1D4E89;
        padding: 0 !important;
        margin: 0 !important;
        height: 100vh;
        overflow: hidden !important;
    }

    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* ====== FILE UPLOADER SPECIFIC FIXES ====== */
    .stFileUploader > div {
        padding: 0 !important;
        margin: 0 !important;
    }

    .stFileUploader > label {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }

    .stFileUploader > section {
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
    }

    .stFileUploader > div > div {
        padding: 0 !important;
        margin: 0 !important;
    }

    .stFileUploader .fileDropArea {
        min-height: 100px !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .stFileUploader .fileDropArea div:first-child {
        margin-top: 0 !important;
    }

    /* ====== BUTTON FIXES ====== */
    .stButton > button {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    /* ====== COLUMN LAYOUT FIXES ====== */
    .st-emotion-cache-1wrcr25 {
        padding: 0 !important;
        margin: 0 !important;
        gap: 0 !important;
    }

    /* ====== ANIMATION CONTAINER ====== */
    .animation-container {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1000;
    }

    /* ====== YOUR ORIGINAL STYLES ====== */
    h1, h2, h3, h4, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        font-weight: 700;
        color: #FFDD57 !important;
        margin-bottom: 1rem !important;
        font-size: 1.2rem;
    }

    .stTextArea, .stTextInput, .stFileUploader, .stButton > button {
        border-radius: 12px;
        margin-bottom: 1rem;
        background-color: #e1f5fe;
        color: #1a1a1a;
        padding: 10px;
    }

    .stButton > button {
        background-color: #4e54c8;
        color: white;
        font-weight: 600;
        border-radius: 12px;
    }

    .stButton > button:hover {
        background-color: #565fdd;
        transform: scale(1.02);
    }

    .stTabs [role="tab"] {
        font-weight: 600;
        font-size: 16px;
        color: #1a1a1a;
    }

    .stMetric {
        font-size: 32px !important;
        font-weight: 700;
        color: #1a1a1a;
    }

    .stTextArea textarea:focus, .stFileUploader input:focus {
        border: 2px solid #4e54c8;
    }

    .stExpander {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: none;
    }

    hr {
        display: none;
    }

    ::-webkit-scrollbar {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# 🔥 Lottie Animation Helper with caching
@st.cache_data(show_spinner=False)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 🧠 App Title
st.title("🤖 HireFit AI – Resume to JD Matcher")

# 🧱 Two-column layout
left_col, right_col = st.columns([1.2, 1.5])

# 📅 Input Section
with left_col:
    st.subheader("📝 Paste Job Description")
    jd_text = st.text_area("Enter the Job Description here", height=300)

    st.subheader("📄 Upload Your Resume")
    resume_file = st.file_uploader("Choose a file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

    submit = st.button("🚀 Submit for Analysis", key="analyze_button")

# 🔍 On submit
if submit:
    if not jd_text or not resume_file:
        st.warning("⚠️ Please paste the Job Description and upload your resume.")
    else:
        # Create centered animation container
        animation_container = st.empty()
        with animation_container.container():
            st.markdown('<div class="animation-container">', unsafe_allow_html=True)
            lottie_animation = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
            animation = st_lottie(lottie_animation, speed=1, height=300, key="processing_animation")
            st.markdown('</div>', unsafe_allow_html=True)
        
        try:
            # Process the resume and JD with caching
            resume_text = get_text(resume_file)
            match_score = calculate_match_score(resume_text, jd_text)
            ai_response = get_structured_analysis(resume_text, jd_text)

            # Clear the animation after processing
            animation_container.empty()
            
            # 📦 Section extractor utility
            def extract_section(title, text):
                start = text.find(title)
                if start == -1:
                    return ""
                end = text.find("\n\n", start)
                return text[start + len(title):end].strip() if end != -1 else text[start + len(title):].strip()

            match = extract_section("Match Percentage:", ai_response)
            strengths = extract_section("Strengths:", ai_response)
            weaknesses = extract_section("Weaknesses:", ai_response)
            conclusion = extract_section("Conclusion:", ai_response)

            match = match.replace("%", "").strip()

            # 📊 Display results
            with right_col:
                with st.expander("📊 Click to view Match Score & Analysis", expanded=True):
                    st.metric(
                        label="Resume Match with Job Description",
                        value=f"{match}%",
                    )

                    tab1, tab2, tab3, tab4 = st.tabs(["🟢 Strengths", "🟠 Weaknesses", "📘 Conclusion", "📄 Tailored Resume"])

                    with tab1:
                        st.markdown(strengths or "_No strengths identified._", unsafe_allow_html=True)

                    with tab2:
                        st.markdown(weaknesses or "_No weaknesses found._", unsafe_allow_html=True)

                    with tab3:
                        st.markdown(conclusion or "_No conclusion generated._", unsafe_allow_html=True)

                    with tab4:
                        with st.spinner("🛠️ Generating tailored resume using AI..."):
                            try:
                                prompt = f"""
You are a professional resume expert. Create a resume tailored to the following job description, using the content and strengths of the provided resume.

Instructions:
- Use **bold** text for all section headings (e.g., **SUMMARY**, **SKILLS**, **EXPERIENCE**, etc.)
- DO NOT use any stars (*), hyphens (-), or numbering for bullet points.
- Simply use line breaks for bullets inside SKILLS and EXPERIENCE.
- Keep the format professional, clean, and ATS-friendly.

--- Job Description --- 
{jd_text}

--- Candidate's Resume ---
{resume_text}
"""
                                generated_resume = generate_resume_from_prompt(prompt)

                                formatted_resume = generated_resume.replace("* ", "")
                                formatted_resume = formatted_resume.replace("**", "<b>").replace("\n", "<br>")

                                st.markdown(f"""
                                    <div style="
                                        background-color: #ffffff;
                                        padding: 1.5rem;
                                        border-radius: 10px;
                                        white-space: pre-wrap;
                                        word-wrap: break-word;
                                        font-family: 'Poppins', sans-serif;
                                        font-size: 15px;
                                        line-height: 1.6;
                                        color: #1a1a1a;
                                        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                                        overflow-x: auto;
                                    ">
                                    {formatted_resume}
                                    </div>
                                """, unsafe_allow_html=True)

                            except Exception as e:
                                st.error(f"⚠️ Failed to generate resume: {e}")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
