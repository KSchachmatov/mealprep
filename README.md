# 🍽️ MealPrep - AI-Powered Meal Planning Assistant

An intelligent meal planning application that uses RAG (Retrieval-Augmented Generation) and Large Language Models to suggest personalized meals and generate weekly meal plans based on your available ingredients and dietary preferences.

## ✨ Features

### Mode 1: Single Meal Suggestion
- **Smart ingredient-based suggestions** - Input what you have in your kitchen
- **RAG-powered recommendations** - Searches through 2.2M+ recipes to find similar dishes
- **Personalized suggestions** - Considers dietary preferences and number of people
- **Variety enforcement** - Avoids suggesting similar meals from recent history
- **Accept/reject workflow** - Generate alternative suggestions until you find the perfect meal

### Mode 2: Multi-Day Meal Planning
- **Automated weekly meal plans** - Generate 1-14 day meal plans
- **Diverse meal selection** - Ensures variety across cuisines and cooking methods
- **Individual meal management** - Accept or regenerate specific days
- **Shopping list generation** - Automatically aggregates ingredients
- **Plan persistence** - Save and reload your favorite meal plans

## 🛠️ Tech Stack

### AI & ML
- **LLM Integration**: Claude Sonnet 4 / OpenAI GPT-4
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Search**: pgvector with PostgreSQL
- **RAG Pipeline**: Custom implementation with semantic similarity search

### Backend
- **Language**: Python 3.12
- **Framework**: Streamlit for UI
- **Database**: PostgreSQL with pgvector extension
- **Data Processing**: Pandas, Pydantic

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Package Management**: uv
- **Environment**: python-dotenv

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Anthropic or OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/mealprep.git
cd mealprep
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Add your API keys to .env
```

3. **Start the services**
```bash
docker-compose up -d
```

4. **Install dependencies**
```bash
uv sync
```

5. **Load recipe data** (optional - for RAG functionality)
```bash
python src/mealprep/insert_vectors.py
```

6. **Run the application**
```bash
streamlit run src/main.py
```

Visit `http://localhost:8501` to use the app!

## 📊 Architecture

```
mealprep/
├── src/
│   └── mealprep/
│       ├── llm/           # LLM clients (Claude, OpenAI)
│       ├── db/            # Database & vector store
│       ├── services/      # Business logic
│       └── models/        # Pydantic models
├── data/                  # Recipe datasets
├── docker-compose.yml     # Service orchestration
└── init.sql              # Database schema
```

### RAG Pipeline
1. **Indexing**: Recipe data embedded using sentence-transformers
2. **Storage**: Embeddings stored in PostgreSQL with pgvector
3. **Retrieval**: Semantic search finds similar recipes based on ingredients
4. **Generation**: Retrieved context passed to LLM for personalized suggestions

## 🎯 Use Cases

- **Reduce food waste** - Use what you already have
- **Meal planning made easy** - Weekly plans in seconds
- **Dietary compliance** - Automatic filtering for restrictions
- **Cooking inspiration** - Discover new recipes similar to your favorites
- **Time-saving** - No more "what's for dinner?" stress

## 🔮 Future Enhancements

- [ ] MCP (Model Context Protocol) integration
- [ ] Advanced text chunking for recipe processing
- [ ] PDF cookbook parsing
- [ ] Nutritional information tracking
- [ ] Meal prep scheduling with calendar integration
- [ ] Mobile app version

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Feel free to open issues or submit pull requests.

---

Built with ❤️ using Claude AI and modern Python tooling