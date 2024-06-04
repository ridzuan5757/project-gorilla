# DataPrepper with AWS S3 and SQS

## `s3` source

`s3` is a source plugin that reads events from AWS S3 objects. We can configure the source to either use an AWS SQS queue or scan an S3 bucket:

- To use Amazon SQS notifications, configure S3 event notifications on your S3 bucket. After Amazon SQS is configured, the `s3` source receives messages from Amazon SQS. 
- When the SQS message indicates that an S3 object has been created, the `s3` source loads the S3 objects and then parses them using the configured `codec`.
- To use an S3 bucket, `s3` source need to be configured to use Amazon S3 Select instead of Data Prepper to parse S3 objects.

### `codec`

The `codec` parameters determines how the `s3` source parses each AWS S3 object For increased and more efficient performance, codec combinations with certain processors can be used. As for Proactive Monitoring initiative, `json` codec will be used.

The `json` codec parses each S3 object as a single JSON object from a JSON array and then creates a DataPrepper log event for each object in the array.

## `s3` sink

The `s3` sink sink saves and writes batches of DataPrepper events to AWS S3 objects. The configured `codec` determines how the `s3` sink serializes the data into Amazon S3.

The `s3` sink uses the following format when batching events:

```bash
${pathPrefix}events-%{yyyy-MM-dd'T'HH-mm-ss'Z'}-${currentTimeInNanos}-${uniquenessId}.${codecSuppliedExtension}
```

When a batch of objects is written to S3, the objects are formatted similarly to the following:

```bash
my-logs/2023/06/09/06/events-2023-06-09T06-00-01-1686290401871214927-ae15b8fa-512a-59c2-b917-295a0eff97c8.json
```

## SQS Dead Letter Queue

Currently, there are two options for how errors are handled when DataPrepper is processing the S3 object:

- Use an SQS DLQ to track the failure. This will be implemented in the Proactive Monitoring roadmap.
- Delete the message from SQS manually by finding the S3 object and correct the error.

# letak gambar kat sini

The following steps will be used to implement the SQS DLQ for the S3 pipeline:

- Create a new SQS standard qeueu to act as the DLQ.
- Configure the SQS redrive policy to use the created DLQ. Consider using value as `3` for the `Maximum Receives` setting.
- Configure the DataPrepper `s3` source to use `retain_message` for `on_error`.


## IAM permission

I n order to use the `s3` source, IAM permissions need to be configured to grant DataPrepper access to AWS S3 with the following permissions:

- `s3:GetObject`
- `s3:ListBucket`
- `s3:DeleteObject`
- `s3:PutObject`
- `sqs:ChangeMessageVisibility`
- `sqs:DeleteMessage`
- `sqs:ReceiveMessage`

## OTLP-DataPrepper-S3-SQS-DataPrepper-OpenSearch Pipeline

DataPrepper can receive OTLP data and then write it as an object in the S3 buckets. It also capable to read objects from S3 buckets using SQS queue and S3 event notifications.

By polling SQS queue for S3 event notifications, everytime an object is created into S3 buckets, it will be read and parsed by DataPrepper again.

# letak gambar kat sini

The flow of data is as follows:

- OpenTelemetry Collector transmit telemetry data to DataPrepper via:
	- `otel_trace_source` from port 21890.
	- `otel_metrics_source` from port 21891.
	- `otel_logs_source` from port 21892.
- DataPrepper produce the JSON log object into the S3 Bucket.
- S3 creates an S3 event notifications in the SQS queue.
- DataPrepper polls AWS SQS for messages and then receives the OTLP log message.
- DataPrepper downloads the content from the S3 object.
- DataPrepper sends the object to OpenSearch.

### Prerequisites

Before DataPrepper can read log data form S3, the following would be required:
- S3 bucket.
- Running OpenTelemetry Collector to transmit OTLP JSON data to DataPrepper.

# Tasks:

- Create AWS S3 buckets.
- Create AWS SQS standard queue for S3 event notifications.
- Configure bucket notifications for SQS using `ObjectCreated` event type.
- Grant AWS IAM permissions to DataPrepper for accessing SQS and S3.
- Create an SQS dead-letter queue.
- Configure an SQS redrive policy to move failed message into the DLQ.
- Configure trace. pipeline from Opentelemetry collector to DataPrepper and S3.
- Configure trace pipeline from Opentelemetry collector to DataPrepper and S3.
- Configure metrics pipeline from Opentelemetry collector to DataPrepper and S3.
- Configure log pipeline from Opentelemetry collector to DataPrepper and S3.
- Configure trace pipeline from S3 to DataPrepper to OpenSearch.
- Configure metrics pipeline from S3 to DataPrepper to OpenSearch.
- Configure logs pipeline from S3 to DataPrepper to OpenSearch.





