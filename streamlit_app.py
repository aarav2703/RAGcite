# streamlit_app.py

import streamlit as st
from arxiv.arxiv_api import fetch_arxiv_results
from arxiv.parser import parse_arxiv_response
from embeddings.vector_store import VectorStore
from emails.email_generator import generate_cold_email

# Initialize vector store
vs = VectorStore()

st.set_page_config(page_title="RAGcite - Research Paper Recommender", layout="wide")

st.title("📚 RAGcite: Research Collaboration Recommender")
st.markdown("Paste your research idea below and find matching papers + professors.")

# --- Student info fields ---
with st.expander("✍️ Personal Info (used in generated emails)", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        student_name = st.text_input("Your Full Name", placeholder="Aarav Kalkar")
        student_uni = st.text_input("University", placeholder="University of Minnesota")

    with col2:
        student_email = st.text_input("Email Address", placeholder="aarav@umn.edu")
        contact_line = st.text_input(
            "Optional Contact (LinkedIn / Phone)", placeholder="linkedin.com/in/aarav"
        )

# --- Research abstract input ---
user_abstract = st.text_area(
    "✍️ Paste your research idea or thesis abstract here", height=200
)

# Sidebar filters
st.sidebar.header("Filters")
max_results = st.sidebar.slider("Number of papers to fetch from arXiv", 5, 50, 10)
email_gen = st.sidebar.toggle("Generate cold email?", value=True)

# Search button
if st.button("🔍 Find Matches"):
    if not user_abstract.strip():
        st.warning("Please enter a research idea or abstract.")
    else:
        with st.spinner("Searching arXiv..."):
            xml = fetch_arxiv_results(user_abstract, max_results=max_results)
            papers = parse_arxiv_response(xml)

            if not papers:
                st.error("No papers found. Try different keywords.")
            else:
                # Embed and add to vector DB
                docs = [{"text": paper["summary"], "meta": paper} for paper in papers]
                vs.add_documents(docs)

                # Search top matches
                results = vs.search(user_abstract, top_k=max_results)

                st.success(f"Top {len(results)} matching papers:")
                for idx, result in enumerate(results, 1):
                    meta = result["meta"]
                    st.markdown(f"### {idx}. {meta['title']}")
                    st.write(f"**Authors:** {', '.join(meta['authors'])}")
                    st.write(f"**Published:** {meta['published']}")
                    st.write(meta["summary"])
                    st.markdown(
                        f"[🔗 View Paper]({meta['link']})  |  [📄 PDF]({meta['pdf_url']})"
                    )

                    if email_gen:
                        with st.expander("📬 Generate Cold Email to First Author"):
                            prof_name = meta["authors"][0]
                            email = generate_cold_email(
                                professor_name=prof_name,
                                university="Unknown University",
                                user_interest=user_abstract,
                                paper_title=meta["title"],
                                include_paper=True,
                                student_name=student_name,
                                student_uni=student_uni,
                                student_email=student_email,
                                contact_line=contact_line,
                            )
                            st.code(email, language="markdown")
