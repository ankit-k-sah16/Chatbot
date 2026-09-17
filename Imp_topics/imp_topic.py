#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI / ML Engineer Placement‑Drive Roadmap → PDF generator
Author : Ankit Kumar Sah
Requires: fpdf2  (pip install fpdf2)

Run:
    python make_roadmap_pdf.py
Result:
    A file named "AI_ML_Placement_Roadmap.pdf" appears in the same folder.
"""

from fpdf import FPDF
import textwrap

# ----------------------------------------------------------------------
# --------------------------- Data to be rendered -----------------------
# ----------------------------------------------------------------------

# ---- 1️⃣ Core subjects -------------------------------------------------
core_subjects = [
    ("High",   "Mathematics for ML", "Linear Algebra, Probability & Statistics, Calculus"),
    ("High",   "Programming (Python)", "Core syntax, OOP, libraries (numpy, pandas, matplotlib)"),
    ("High",   "Data Structures & Algorithms (DSA)", "Arrays, trees, graphs, sorting, DP, etc."),
    ("High",   "Machine‑Learning Fundamentals", "Supervised/unsupervised learning, bias‑variance, regularisation"),
    ("High",   "Deep Learning", "Feed‑forward nets, CNNs, RNNs/Transformers, optimisation"),
    ("Medium", "Software‑Engineering Practices", "Clean code, OOP, design patterns, Git, testing"),
    ("Medium", "System Design & Scalability", "Data pipelines, model‑serving, micro‑services"),
    ("Medium", "MLOps & Deployment", "Docker, Kubernetes, CI/CD, model monitoring, A/B testing"),
    ("Medium", "Cloud Platforms", "AWS SageMaker, GCP Vertex AI, Azure ML"),
    ("Low",    "Domain‑Specific AI", "NLP, Computer Vision, Reinforcement Learning – dive as needed"),
    ("Low",    "Ethics, Fairness & Privacy", "Bias mitigation, GDPR/CCPA, responsible AI"),
    ("Low",    "Big‑Data Tools", "Spark, Hadoop, Flink – for massive preprocessing"),
]

# ---- 2️⃣ Detailed topics (priority checklist) -------------------------
# Each entry: (priority, heading, list of bullet strings)
detailed_topics = [
    # -------- High priority ------------------------------------------------
    ("High", "Mathematics", [
        "Linear Algebra – vectors, matrices, multiplication, eigenn values, SVD, PCA",
        "Probability & Statistics – distributions, Bayes theorem, expectation, variance, hypothesis testing",
        "Calculus – gradient, Jacobian, Hessian, chain rule, optimisation basics (gradient descent)"]),
    ("High", "Python Proficiency", [
        "List/Dict comprehensions, generators, decorators, context managers",
        "Core libraries: numpy, pandas, matplotlib / seaborn",
        "Virtual environments – venv / conda, pip install –‑‑ best practices"]),
    ("High", "DSA – Core", [
        "Arrays, linked lists, stacks, queues, hash tables",
        "Binary trees, BST, heaps, graphs (BFS/DFS)",
        "Sorting algorithms – quick‑sort, merge‑sort, heap‑sort",
        "Recursion & time/space‑complexity analysis"]),
    ("High", "DSA – Advanced", [
        "Dynamic programming (knapsack, LCS, edit distance)",
        "Sliding‑window & two‑pointer techniques",
        "Back‑tracking, bit‑masking"]),
    ("High", "Supervised Learning", [
        "Linear & logistic regression, SVM, K‑NN",
        "Decision trees, ensemble methods – Random Forest, XGBoost, LightGBM",
        "Evaluation metrics – accuracy, precision, recall, F1, ROC‑AUC"]),
    ("High", "Unsupervised Learning", [
        "K‑means, hierarchical clustering, DBSCAN",
        "Gaussian Mixture Models, dimensionality reduction – PCA, t‑SNE, UMAP"]),
    ("High", "Model Evaluation & Validation", [
        "Train/validation/test split, k‑fold CV (stratified), leakage prevention",
        "Hyper‑parameter tuning – grid search, random search, Bayesian optimisation"]),
    ("High", "Neural Networks Basics", [
        "Perceptron, activation functions (ReLU, sigmoid, tanh, softmax)",
        "Loss functions – MSE, cross‑entropy",
        "Back‑propagation, weight initialisation strategies"]),
    ("High", "Convolutional Neural Networks (CNNs)", [
        "Convolution operation, padding, stride, pooling",
        "Classic architectures – LeNet, AlexNet, VGG, ResNet, EfficientNet"]),
    ("High", "RNNs & Transformers", [
        "Vanishing‑gradient problem, LSTM/GRU cells",
        "Attention mechanism, encoder‑decoder, BERT, GPT‑style models"]),
    # -------- Medium priority -----------------------------------------------
    ("Medium", "Software‑Engineering Practices", [
        "Clean code principles, SOLID, design patterns",
        "Version control – Git (branching, PR workflow)",
        "Unit / integration testing (pytest, unittest)"]),
    ("Medium", "System Design for ML", [
        "Designing data pipelines (ETL/ELT)",
        "Model serving – REST/gRPC, batch vs. online inference",
        "Micro‑service architecture, load balancing, caching"]),
    ("Medium", "MLOps & Deployment", [
        "Containerisation – Docker, Docker‑Compose",
        "Orchestration – Kubernetes basics, Helm charts",
        "CI/CD for ML – GitHub Actions / GitLab CI, model registry (MLflow)"]),
    ("Medium", "Cloud Platforms", [
        "AWS – S3, EC2, SageMaker, Lambda",
        "GCP – Cloud Storage, AI Platform / Vertex AI",
        "Azure – Blob Storage, Azure ML"]),
    ("Medium", "Monitoring & Governance", [
        "Model drift detection, data drift, performance dashboards",
        "Logging & tracing (ELK stack, Prometheus + Grafana)",
        "Security basics – IAM, secret management"]),
    # -------- Low priority --------------------------------------------------
    ("Low", "Domain‑Specific AI", [
        "NLP – tokenisation, word‑embeddings, Transformers, spaCy, HuggingFace",
        "Computer Vision – OpenCV, image augmentation, object detection (YOLO, Faster‑RCNN)"]),
    ("Low", "Ethics & Fairness", [
        "Bias detection (fairness metrics), mitigation techniques",
        "Explainability – SHAP, LIME, counterfactuals",
        "Regulatory compliance – GDPR, CCPA"]),
    ("Low", "Big‑Data Ecosystem", [
        "Spark (PySpark)–DataFrames, MLlib basics",
        "Hive / Presto basics for ad‑hoc querying",
        "Streaming – Kafka + Structured Streaming"]),
]

# ----------------------------------------------------------------------
# --------------------------- PDF generation ----------------------------
# ----------------------------------------------------------------------


class PDF(FPDF):
    """A tiny subclass that adds a few convenience methods."""
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font("DejaVuSans", "", "DejaVuSans.ttf")
        self.set_font('DejaVuSans', '', 12)   # fallback Unicode font

    def header(self):
        # Simple header with page number
        self.set_font('DejaVuSans', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, f'Page {self.page_no()}', align='R')
        self.ln(10)

    def footer(self):
        # Empty footer – you can add your contact info here if you want
        pass

    def title_page(self, name: str):
        self.add_page()
        self.set_font('Helvetica', 'B', 24)
        self.ln(30)
        self.cell(0, 10, "AI / ML Engineer Placement Drive Roadmap", ln=1, align='C')
        self.ln(20)
        self.set_font('Helvetica', '', 16)
        self.cell(0, 10, f"Prepared for: {name}", ln=1, align='C')
        self.ln(10)
        self.set_font('Helvetica', '', 12)
        self.multi_cell(0.75 * self.w, 5,
            "This document lists the subjects and topics you should master, "
            "ordered by interview priority. Use it as a checklist while you "
            "study, code and practice mock interviews.", align='C')
        self.ln(30)

    def add_section_heading(self, txt: str, level: int = 1):
        """level 1 = big, level 2 = medium, level 3 = small"""
        sizes = {1: 16, 2: 14, 3: 12}
        self.set_font('Helvetica', 'B', sizes.get(level, 12))
        self.ln(5)
        self.cell(0, 8, txt, ln=1)

    def add_table(self, data, col_widths):
        """Simple table – data is list of rows, each row a list of cells."""
        self.set_font('Helvetica', '', 11)
        line_h = 7
        for row in data:
            for i, txt in enumerate(row):
                self.multi_cell(col_widths[i], line_h, txt, border=1,
                               align='C' if i == 0 else 'L', ln=3 if i == len(row)-1 else 0)
            self.ln(line_h)

    def add_bulleted_list(self, items, indent=10):
        bullet = u'\u2022'   # Unicode bullet
        self.set_font('Helvetica', '', 11)
        for item in items:
            # wrap long lines so they stay inside the page margin
            wrapped = textwrap.wrap(item, width=95)
            if not wrapped:
                continue
            self.cell(indent)                # indentation
            self.cell(3, 5, bullet)          # bullet
            self.multi_cell(0, 5, wrapped[0])
            for cont in wrapped[1:]:
                self.cell(indent + 6)        # align continuation lines
                self.cell(3, 5, '')
                self.multi_cell(0, 5, cont)

    def add_checklist_section(self, priority, heading, bullets):
        # colour‑code priority (optional)
        colors = {"High": (220, 0, 0), "Medium": (220, 140, 0), "Low": (0, 120, 0)}
        r, g, b = colors.get(priority, (0, 0, 0))
        self.set_text_color(r, g, b)
        self.add_section_heading(f"{priority} priority – {heading}", level=2)
        self.set_text_color(0, 0, 0)   # back to normal for bullets
        self.add_bulleted_list(bullets)
        self.ln(4)


def generate_pdf(filename: str = "AI_ML_Placement_Roadmap.pdf", owner_name: str = "Your Name"):
    pdf = PDF()
    pdf.title_page(owner_name)

    # --------- 1️⃣ Core subjects table ------------------------------------
    pdf.add_section_heading("Core Subjects – Priority Order", level=1)
    # Table header
    table_data = [["Priority", "Subject", "Key Areas / Why Important"]]
    # Add rows
    for prio, subj, desc in core_subjects:
        table_data.append([prio, subj, desc])
    # Column widths (in mm) – adjust if you change page layout
    col_w = [20, 60, 100]
    pdf.add_table(table_data, col_w)

    # --------- 2️⃣ Detailed topics checklist -------------------------------
    pdf.add_section_heading("Detailed Topics – Checklist (Priority)", level=1)

    # Group topics by priority to keep the same colour block together
    for priority in ["High", "Medium", "Low"]:
        for prio, heading, bullets in detailed_topics:
            if prio == priority:
                pdf.add_checklist_section(priority, heading, bullets)

    # Save file
    pdf.output(filename)
    print(f"\n✅ PDF generated → {filename}")


# ----------------------------------------------------------------------
# ------------------------------ Main entry -----------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # You can edit the name below – it will appear on the title page.
    YOUR_NAME = "Your Name – B.Tech CSE (Final Year)"
    generate_pdf(filename="AI_ML_Placement_Roadmap.pdf", owner_name='Ankit Kumar Sah')