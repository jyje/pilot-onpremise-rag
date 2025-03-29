import argparse, os
from dotenv import load_dotenv
from loguru import logger

# Load environment variables first
load_dotenv(dotenv_path=os.environ.get('ENV_FILE', '.env'), override=True)

from rag.config import top_parser, common_parser, setup_logger
from rag.train.config import parser as train_parser


# Main parser
parser = argparse.ArgumentParser(
    formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    description = 'RAG',
    parents = [top_parser],
    add_help = False,
)

# Commands
subparsers = parser.add_subparsers(
    title = 'Commands',
    dest = 'command',
)

subparsers.add_parser(
    'train',
    help = 'Train markdown files to the vector database as the knowledge base',
    parents = [top_parser, common_parser, train_parser],
    add_help = False,
)


if __name__ == '__main__':
    args = parser.parse_args()

    command = f"with command: {args.command}" if args.command else ""
    logger.info(f"RAG Started {command}")
    
    setup_logger(args.log_level)
    logger.debug(f"Parsed arguments: {args}")
