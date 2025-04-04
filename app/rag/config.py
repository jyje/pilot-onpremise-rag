import argparse, os, sys
from pathlib import Path
from loguru import logger

# Logger format constants
TIME_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS!UTC}Z"
FILE_FORMAT = f"{TIME_FORMAT} | {{level: <8}} | {{name}}:{{function}}:{{line}} - {{message}}"
CONSOLE_FORMAT_FULL = f"<green>{TIME_FORMAT}</green> | <level>{{level: <8}}</level> | <cyan>{{name}}</cyan>:<cyan>{{function}}</cyan>:<cyan>{{line}}</cyan> - <level>{{message}}</level>\n"
CONSOLE_FORMAT_SIMPLE = f"<green>{TIME_FORMAT}</green> | <level>{{level: <8}}</level> | <level>{{message}}</level>\n"

# Initial logger setup
logger.remove()
logger.add(
    sink = sys.stderr,
    level = "INFO", 
    format = lambda record: CONSOLE_FORMAT_SIMPLE if record["level"].name == "INFO" else CONSOLE_FORMAT_FULL,
    colorize = True
)

def setup_logger(log_level: str):
    """Configure logger with specified level and outputs"""
    
    logger.remove()
    
    log_dir = Path("app/logs")
    log_dir.mkdir(exist_ok=True, parents=True)
    
    # File handler
    logger.add(
        sink = log_dir / "app.log",
        level = log_level,
        rotation = "500 MB",
        format = FILE_FORMAT,
        serialize = False,
        enqueue = True,
        backtrace = True,
        diagnose = True,
        catch = True
    )
    
    # Console handler
    logger.add(
        sink = sys.stderr,
        level = log_level,
        format = lambda record: CONSOLE_FORMAT_SIMPLE if record["level"].name == "INFO" else CONSOLE_FORMAT_FULL,
        colorize = True
    )
    
    logger.debug(f"Logger configured with level: {log_level}")


class EnvDefault(argparse.Action):
    """Argparse action that uses environment variables as defaults"""
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if envvar and envvar in os.environ:
            env_value = os.environ[envvar]
            # Convert string environment variable to boolean
            if kwargs.get('nargs') is None and kwargs.get('const') is not None:  # store_true/store_false case
                default = env_value.lower() in ('true', '1', 'yes', 'on')
            else:
                default = env_value
            logger.debug(f"Using {envvar}={default} from environment")
        
        if envvar:
            kwargs["help"] += f" (envvar: {envvar})"
        
        if required and default:
            required = False
            
        super(EnvDefault, self).__init__(default=default, required=required, **kwargs)
        self.envvar = envvar

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values if values is not None else self.default)


# Top-level parser with common options
top_parser = argparse.ArgumentParser(add_help=False)

top_parser.add_argument(
    '-h', '--help',
    help = 'Show help message and exit',
    default = argparse.SUPPRESS,
    action = 'help',
)

top_parser.add_argument(
    '--env-file',
    envvar = 'ENV_FILE',
    help = 'Path to environment file',
    default = '.env',
    type = str,
    action = EnvDefault,
)

top_parser.add_argument(
    '--log-level',
    envvar = 'LOG_LEVEL',
    help = 'Logging level',
    default = 'INFO',
    type = lambda x: x.upper(),
    choices = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    required = False,
    action = EnvDefault,
)

top_parser.add_argument(
    '--log-path',
    envvar = 'LOG_PATH',
    help = 'Path to log file',
    default = 'app/logs',
    type = str,
    required = False,
    action = EnvDefault,
)

top_parser.add_argument(
    '--log-save',
    envvar = 'LOG_SAVE',
    help = 'Save log to file. If this flag is set, the log will be saved to the file specified in the `--log-path`.',
    default = False,
    const = True,
    nargs = 0,
    type = bool,
    required = False,
    action = EnvDefault,
)

common_parser = argparse.ArgumentParser(
    add_help = False,
)
