# 🧠 Credit Card Recommendation Agent

This project is an AI-driven system featuring **two collaborating agents** designed to assist users in selecting the most suitable credit card.

## 🔧 Project Overview

The system consists of the following agents:

### 1. 🤖 Credit Query Assistant
- Interactively engages with the user by asking relevant questions.
- Generates the **next best question** dynamically based on the user's previous responses.
- Aims to understand the user's financial needs, lifestyle, and preferences.

### 2. 🎯 Credit Recommendation Agent
- Observes the full dialogue between the user and the assistant.
- Uses the question-answer history to provide a **personalized credit card recommendation**.
- Ensures the suggestion is data-driven and user-specific.

## 🚀 How It Works

1. The user starts a conversation with the Credit Query Assistant.
2. Based on each user response, the assistant formulates the next most informative question.
3. Once sufficient information is collected, the Credit Recommendation Agent analyzes the conversation.
4. A credit card recommendation is provided based on the gathered insights.

## 📁 Files

- `main.py` – Entry point to start the agent interaction.
- `agents.py` – Contains logic for both assistant and recommender agents.
- `task.py` – Defines the sequence and flow of tasks between agents.

## 🛠️ Requirements

- Python 3.8+
- (List any frameworks or libraries you use, like LangChain, CrewAI, etc.)

## 📌 Usage

```bash
python main.py
