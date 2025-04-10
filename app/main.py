import argparse, os
from dotenv import load_dotenv
from loguru import logger

# Load environment variables first
load_dotenv(dotenv_path=os.environ.get('ENV_FILE', '.env'), override=True)

from rag.config import top_parser, common_parser, setup_logger
from rag.train.config import parser as train_parser
from rag.train.router import route as train_route
from rag.test.config import parser as test_parser
from rag.test.router import route as test_route

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

train_subparser = subparsers.add_parser(
    'train',
    help = train_parser.description,
    description = train_parser.description,
    parents = [top_parser, common_parser, train_parser],
    add_help = False,
)

test_subparser = subparsers.add_parser(
    'test',
    help = test_parser.description,
    description = test_parser.description,
    parents = [top_parser, common_parser, test_parser],
    add_help = False,
)

if __name__ == '__main__':
    args = parser.parse_args()

    command = f"with command: {args.command}" if args.command else ""
    logger.info(f"RAG Started {command}")
    
    setup_logger(args.log_level)
    logger.debug(f"Parsed arguments: {args}")

    if args.command == 'train':
        train_route(args)
    elif args.command == 'test':
        test_route(args)
