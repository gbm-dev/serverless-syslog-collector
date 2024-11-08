#!/usr/bin/env python3
import subprocess
import json
import time
from datetime import datetime
import sys

def get_fluentd_metrics():
    try:
        # Get Fluentd logs
        result = subprocess.run(
            ['docker', 'logs', 'fluentd', '--tail', '100'], 
            capture_output=True, 
            text=True
        )
        
        logs = result.stdout.split('\n')
        
        # Parse and analyze logs
        errors = []
        events_processed = 0
        buffer_stats = []
        
        for line in logs:
            if 'error' in line.lower():
                errors.append(line)
            if 'events processed' in line:
                events_processed += 1
            if 'buffer' in line:
                buffer_stats.append(line)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_errors': len(errors),
            'last_error': errors[-1] if errors else None,
            'events_processed': events_processed,
            'buffer_stats': buffer_stats[-5:] if buffer_stats else []
        }
    except Exception as e:
        return {
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }

def check_fluentd_port():
    try:
        result = subprocess.run(
            ['docker', 'exec', 'fluentd', 'netstat', '-tulpn'], 
            capture_output=True, 
            text=True
        )
        return '5140' in result.stdout
    except:
        return False

def main():
    print("\n=== Fluentd Monitoring ===\n")
    
    # Check if Fluentd container is running
    result = subprocess.run(
        ['docker', 'ps', '-f', 'name=fluentd'], 
        capture_output=True, 
        text=True
    )
    
    if 'fluentd' not in result.stdout:
        print("❌ Fluentd container is not running!")
        sys.exit(1)
    
    # Check port
    port_status = check_fluentd_port()
    print(f"Port 5140 listening: {'✅' if port_status else '❌'}")
    
    # Get metrics
    metrics = get_fluentd_metrics()
    print("\nMetrics:")
    print(json.dumps(metrics, indent=2))
    
    # Provide status summary
    print("\nStatus Summary:")
    if metrics.get('error'):
        print(f"❌ Error getting metrics: {metrics['error']}")
    else:
        print(f"Total Errors: {metrics['total_errors']}")
        print(f"Events Processed: {metrics['events_processed']}")
        if metrics['last_error']:
            print(f"\nLast Error: {metrics['last_error']}")
        
        print("\nRecent Buffer Stats:")
        for stat in metrics['buffer_stats']:
            print(f"  {stat}")

if __name__ == "__main__":
    main()