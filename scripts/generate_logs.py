import random
import time
import logging
import logging.handlers
from datetime import datetime
import socket
import sys
from termcolor import colored  # type: ignore # For colored console output

def setup_logger(retry_count=5, retry_delay=5):
    """Setup logger with retry mechanism"""
    logger = logging.getLogger('SyntheticLogs')
    logger.setLevel(logging.INFO)
    
    for attempt in range(retry_count):
        try:
            print(f"Attempting to connect to rsyslog (attempt {attempt + 1}/{retry_count})...")
            # Try to create the syslog handler
            handler = logging.handlers.SysLogHandler(
                address=('rsyslog', 514),
                facility=logging.handlers.SysLogHandler.LOG_LOCAL0,
                socktype=socket.SOCK_STREAM
            )
            
            # Add formatter
            formatter = logging.Formatter('%(name)s: [%(levelname)s] %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            print(colored("Successfully connected to rsyslog", "green"))
            return logger
            
        except socket.error as e:
            print(colored(f"Failed to connect to rsyslog: {e}", "red"))
            if attempt < retry_count - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(colored("Max retry attempts reached. Exiting.", "red"))
                sys.exit(1)

def get_severity_color(severity):
    """Return color for severity level"""
    colors = {
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red'
    }
    return colors.get(severity, 'white')

# Message templates
APPLICATION_MSGS = [
    "Application started successfully",
    "New user registration: user_{} created",
    "Failed login attempt from IP {}.{}.{}.{}",
    "Database connection established",
    "Cache miss for key: cache_{}",
    "Memory usage at {}%",
    "CPU load: {}%",
    "Disk usage reached {}%",
    "Network latency: {}ms",
    "Batch job {} completed in {}s"
]

SEVERITY_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

def generate_random_ip():
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def generate_log_message():
    msg_template = random.choice(APPLICATION_MSGS)
    
    # Format message with random values
    if "{}" in msg_template:
        if "IP" in msg_template:
            msg = msg_template.format(random.randint(1,255), random.randint(1,255),
                                    random.randint(1,255), random.randint(1,255))
        elif "user" in msg_template:
            msg = msg_template.format(random.randint(1000,9999))
        elif "cache" in msg_template:
            msg = msg_template.format(random.randint(1,1000))
        elif "%" in msg_template:
            msg = msg_template.format(random.randint(1,100))
        elif "ms" in msg_template:
            msg = msg_template.format(random.randint(1,500))
        elif "job" in msg_template:
            msg = msg_template.format(random.randint(1000,9999), random.randint(1,300))
        else:
            msg = msg_template
    else:
        msg = msg_template
    
    return msg

def main():
    print(colored("Starting synthetic log generation...", "cyan"))
    
    # Setup logger with retry mechanism
    logger = setup_logger()
    
    log_count = 0
    start_time = time.time()
    
    while True:
        try:
            # Select random severity level with weighted distribution
            severity = random.choices(
                list(SEVERITY_LEVELS.keys()),
                weights=[5, 70, 15, 8, 2],  # Weighted towards INFO level
                k=1
            )[0]
            
            msg = generate_log_message()
            logger.log(SEVERITY_LEVELS[severity], msg)
            
            # Print colorized output to terminal
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(colored(
                f"[{timestamp}] Sent {severity:8} : {msg}",
                get_severity_color(severity)
            ))
            
            log_count += 1
            if log_count % 100 == 0:
                elapsed = time.time() - start_time
                rate = log_count / elapsed
                print(colored(f"\nStats: Sent {log_count} logs, Rate: {rate:.2f} logs/sec\n", "cyan"))
            
        except Exception as e:
            print(colored(f"Error sending log: {e}", "red"))
            # Try to reconnect
            logger = setup_logger()
            continue
            
        # Random sleep between 0.1 and 2 seconds
        time.sleep(random.uniform(0.1, 2))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\nShutting down gracefully...", "yellow"))
        sys.exit(0)