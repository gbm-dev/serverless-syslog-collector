#!/bin/bash
# Save as scripts/verify_pipeline.sh

echo "=== Checking RSyslog Status ==="
echo "RSyslog process:"
docker exec rsyslog ps aux | grep rsyslog | grep -v grep
echo
echo "RSyslog port status:"
docker exec rsyslog netstat -tulpn | grep :514
echo
echo "Last 5 lines from RSyslog logs:"
docker exec rsyslog tail -n 5 /var/log/syslog
echo

echo "=== Checking Fluentd Status ==="
echo "Fluentd logs:"
docker logs --tail 20 fluentd | grep -v "stderr" | grep -v "stdout"
echo
echo "Fluentd port status:"
docker exec fluentd netstat -tulpn | grep :5140
echo

echo "=== Checking Loki Status ==="
echo "Loki ready status:"
curl -s http://localhost:3100/ready
echo
echo
echo "Checking Loki volume stats:"
curl -s "http://localhost:3100/loki/api/v1/index/volume" \
  --data-urlencode 'query={job="synthetic_syslog"}' | jq
echo

echo "=== Checking Loki Query ==="
echo "Last 5 log entries:"
current_time=$(date +%s)
start_time=$((current_time - 300))  # 5 minutes ago
curl -G -s "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode "query={job=\"synthetic_syslog\"}" \
  --data-urlencode "start=$start_time000000000" \
  --data-urlencode "end=$current_time000000000" \
  --data-urlencode "limit=5" | jq '.data.result[0].values'