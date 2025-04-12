import argparse

parser = argparse.ArgumentParser(
    description = 'Ask RAG System. Queries the knowledge base with natural language questions, retrieves relevant context, and generates accurate, contextually-aware responses based on the retrieved information',
    add_help = False,
    formatter_class = argparse.ArgumentDefaultsHelpFormatter,
)
