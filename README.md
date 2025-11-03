BroadcastingLawNLP

Analyzing Public Discourse on the Indonesian Broadcasting Bill (RUU Penyiaran)

This repository contains research materials and analytical scripts from the “Konvergensi Media dan Tata Kelola Penyiaran di Indonesia” project by the Center for Digital Society (CfDS), Universitas Gadjah Mada, in collaboration with Google Indonesia.
The project examines how citizens, content creators, and media outlets respond to Indonesia’s proposed Broadcasting Bill (RUU Penyiaran) using a combination of social media analytics, topic modeling, sentiment analysis, and survey research.

📊 Project Overview

The repository provides:

NLP-based topic modeling and sentiment analysis of public conversations on X (Twitter) and TikTok.

Google News data scraping and content clustering to assess media framing.

Survey-based analysis of citizens’ perceptions and trust in digital media governance.

Data visualization and communication through the #MediaKita public awareness campaign.

🧠 Main Notebooks
File	Description
scripts/X/Analisis RUU Penyiaran X.ipynb	Pre-processing and sentiment analysis of tweets related to RUU Penyiaran.
scripts/X/[X_Twitter]_Topic_Modeling_dengan_LLM.ipynb	Topic modeling of X/Twitter data using transformer-based LLM embeddings.
scripts/TikTok/Analisis Sentimen TikTok.ipynb	Sentiment classification of TikTok video comments using NLP models.
scripts/TikTok/[TikTok]_Topic_Modeling_dengan_LLM.ipynb	Topic modeling of TikTok discussions related to RUU Penyiaran.
scripts/Google News/Google News Analysis.ipynb	Google News scraping and article clustering for media coverage analysis.
scripts/Google News/[Berita]_Topic_Modeling_dengan_LLM.ipynb	Topic modeling of news coverage around the Broadcasting Bill.
📊 Public Opinion Survey Dashboard

The project also includes a public perception survey measuring:

Risk perception toward media regulation

Trust in government and institutions

Benefit perception and attitudes toward digital platforms

All responses are visualized in an interactive Google Looker Studio dashboard that allows real-time monitoring of survey results.

🔗 Access Dashboard: https://lookerstudio.google.com/reporting/9d751548-e1c9-429c-9dd7-49375c536f13

🧾 Survey Validation Script: survei/Uji Validitas dan Reliabilitas.R

📂 Repository Structure
data/                # Raw and processed datasets from X, TikTok, and Google News
scripts/             # Analysis notebooks for each platform
visualization/       # Output charts, sentiment trends, and wordclouds
crawlers/            # Custom web crawlers (Apify and Selenium)
survei/              # Survey instruments and validation scripts (R)
README.md            # Project documentation

⚙️ Requirements

Install dependencies:

pip install -r requirements.txt


Main libraries:
pandas, numpy, scikit-learn, transformers, openai, matplotlib, wordcloud

📈 Outputs

Topic clusters and sentiment trends across X, TikTok, and online news

Wordclouds and visual summaries of major discussion themes

Survey-based insights into public attitudes toward digital media governance

Policy recommendations for transparent, participatory media regulation

🧩 Contributors

Bangkit Adhi Wiguna — Center for Digital Society (CfDS), Universitas Gadjah Mada
Collaboration with Google Indonesia

📜 License

This repository is intended for academic and public policy research.
Please credit Center for Digital Society (Universitas Gadjah Mada) and link to this repository when using its data or code.
