---
layout: post
title: "How can I get the size of an Amazon S3 bucket?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
Because Amazon S3 is an object store rather than a traditional hierarchical file system, it does not keep a real-time single-attribute counter for the total size or object count of a bucket. Iterating through the bucket (using `s3cmd du` or `s3cmd ls`) performs `LIST` API operations, which can be slow, expensive, and unscalable on buckets with millions of objects.

The most scalable and cost-effective way to track and graph bucket size and object count is via **Amazon CloudWatch**, which automatically collects these daily metrics at no cost for standard S3 metric reporting. 

---

### Method 1: Query Amazon CloudWatch (Recommended for Graphing)

AWS calculates bucket statistics once per day (usually at midnight UTC) and publishes them to CloudWatch under the `AWS/S3` namespace. You can retrieve these values instantly without scanning your bucket.

#### Important Metric Requirements
* **`BucketSizeBytes`**: Requires the dimension `StorageType` (e.g., `StandardStorage`).
* **`NumberOfObjects`**: Requires the dimension `StorageType` set to `AllStorageTypes`.

#### Using the AWS CLI

To get the bucket size in bytes:
```bash
aws cloudwatch get-metric-statistics \
    --namespace AWS/S3 \
    --metric-name BucketSizeBytes \
    --dimensions Name=BucketName,Value=YOUR_BUCKET_NAME Name=StorageType,Value=StandardStorage \
    --start-time 2023-10-01T00:00:00Z \
    --end-time 2023-10-03T00:00:00Z \
    --period 86400 \
    --statistics Average
```

To get the total number of objects:
```bash
aws cloudwatch get-metric-statistics \
    --namespace AWS/S3 \
    --metric-name NumberOfObjects \
    --dimensions Name=BucketName,Value=YOUR_BUCKET_NAME Name=StorageType,Value=AllStorageTypes \
    --start-time 2023-10-01T00:00:00Z \
    --end-time 2023-10-03T00:00:00Z \
    --period 86400 \
    --statistics Average
```

#### Using Python (Boto3)

If you are writing a script to pipe metrics into a graphing tool (like Grafana, Datadog, or Graphite):

```python
import boto3
from datetime import datetime, timedelta

cw = boto3.client('cloudwatch')
bucket_name = 'YOUR_BUCKET_NAME'

end_time = datetime.utcnow()
start_time = end_time - timedelta(days=2)

# 1. Fetch Bucket Size in Bytes
size_response = cw.get_metric_statistics(
    Namespace='AWS/S3',
    MetricName='BucketSizeBytes',
    Dimensions=[
        {'Name': 'BucketName', 'Value': bucket_name},
        {'Name': 'StorageType', 'Value': 'StandardStorage'}
    ],
    StartTime=start_time,
    EndTime=end_time,
    Period=86400,
    Statistics=['Average']
)

# 2. Fetch Object Count
count_response = cw.get_metric_statistics(
    Namespace='AWS/S3',
    MetricName='NumberOfObjects',
    Dimensions=[
        {'Name': 'BucketName', 'Value': bucket_name},
        {'Name': 'StorageType', 'Value': 'AllStorageTypes'}
    ],
    StartTime=start_time,
    EndTime=end_time,
    Period=86400,
    Statistics=['Average']
)

latest_size = sorted(size_response['Datapoints'], key=lambda x: x['Timestamp'])[-1]['Average']
latest_count = sorted(count_response['Datapoints'], key=lambda x: x['Timestamp'])[-1]['Average']

print(f"Bucket Size: {int(latest_size)} bytes")
print(f"Total Objects: {int(latest_count)}")
```

---

### Method 2: AWS CLI S3 Summary (For Real-Time Snapshots)

If you need the exact, up-to-the-minute size and object count rather than daily CloudWatch metrics, use the AWS CLI's native `--summarize` flag instead of `s3cmd`.

```bash
aws s3 ls s3://YOUR_BUCKET_NAME --recursive --human-readable --summarize
```

At the bottom of the output, you will receive:
```text
Total Objects: 14285
Total Size: 1.2 GiB
```

*Note: This command still sends `LIST` requests behind the scenes. For very large buckets (hundreds of thousands to millions of objects), it will take a significant amount of time and will incur standard S3 `LIST` request charges.*

---

### Method 3: Amazon S3 Storage Lens

If you prefer a managed, UI-driven approach:
1. Open the **Amazon S3 console**.
2. In the left navigation pane, select **Storage Lens** > **Dashboards**.
3. AWS provides a **default dashboard** that visualizes aggregated metrics, storage growth, and object counts across all buckets in your account with 30 days of historical data for free.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/84815/how-can-i-get-the-size-of-an-amazon-s3-bucket).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
