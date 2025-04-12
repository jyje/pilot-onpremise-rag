import argparse

parser = argparse.ArgumentParser(
    description = 'Train RAG System. Processes documents, extracts knowledge, generates embeddings, and builds a searchable vector database for efficient semantic retrieval and contextual responses',
    add_help = False,
    formatter_class = argparse.ArgumentDefaultsHelpFormatter,
)
