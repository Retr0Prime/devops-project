output "bucket_name" {
  description = "Nombre del bucket creado"
  value       = aws_s3_bucket.tasks_bucket.bucket
}

output "bucket_arn" {
  description = "ARN del bucket"
  value       = aws_s3_bucket.tasks_bucket.arn
}
