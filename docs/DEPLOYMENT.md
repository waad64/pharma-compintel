# PCI Dashboard - Deployment Guide

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Database backups enabled
- [ ] SSL/TLS certificates ready
- [ ] Monitoring configured
- [ ] Logging aggregation set up
- [ ] Disaster recovery plan tested
- [ ] Security audit completed

## Local Deployment

### 1. Setup Environment
```bash
# Clone repository
git clone <repository-url>
cd compintel

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Application
```bash
# Copy environment template
cp config/.env.example config/.env

# Edit configuration
nano config/.env
```

### 3. Run Application
```bash
# Run data pipeline (optional)
python unified_data_pipeline.py

# Start Streamlit app
streamlit run pci_dashboard.py
```

### 4. Access Application
```
http://localhost:8501
```

## Docker Deployment

### 1. Build Docker Image
```bash
docker build -t pci-dashboard:2.0.0 .
```

### 2. Run Container
```bash
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e LOG_LEVEL=INFO \
  pci-dashboard:2.0.0
```

### 3. Docker Compose
```bash
docker-compose up -d
```

## Cloud Deployment

### AWS Deployment

#### Option 1: Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Configure secrets in Streamlit Cloud dashboard
4. Deploy

#### Option 2: EC2 Instance
```bash
# SSH into instance
ssh -i key.pem ec2-user@instance-ip

# Install dependencies
sudo yum install python3 python3-pip

# Clone repository
git clone <repository-url>
cd compintel

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run with systemd
sudo systemctl start pci-dashboard
```

#### Option 3: ECS/Fargate
```bash
# Push image to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag pci-dashboard:2.0.0 <account-id>.dkr.ecr.us-east-1.amazonaws.com/pci-dashboard:2.0.0
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/pci-dashboard:2.0.0

# Create ECS task definition and service
# (Use AWS Console or CloudFormation)
```

### Azure Deployment

#### App Service
```bash
# Login to Azure
az login

# Create resource group
az group create --name pci-dashboard-rg --location eastus

# Create App Service plan
az appservice plan create --name pci-dashboard-plan --resource-group pci-dashboard-rg --sku B2

# Create web app
az webapp create --resource-group pci-dashboard-rg --plan pci-dashboard-plan --name pci-dashboard

# Deploy from GitHub
az webapp deployment source config-zip --resource-group pci-dashboard-rg --name pci-dashboard --src app.zip
```

### GCP Deployment

#### Cloud Run
```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/pci-dashboard

# Deploy to Cloud Run
gcloud run deploy pci-dashboard \
  --image gcr.io/PROJECT_ID/pci-dashboard \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Production Configuration

### 1. Environment Variables
```bash
# config/.env
DEBUG=False
LOG_LEVEL=INFO
SESSION_TIMEOUT_MINUTES=60
CACHE_TTL_SECONDS=3600
DATABASE_URL=postgresql://user:password@host:5432/pci_db
```

### 2. SSL/TLS Configuration
```bash
# Generate self-signed certificate (for testing)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Or use Let's Encrypt
certbot certonly --standalone -d yourdomain.com
```

### 3. Reverse Proxy (Nginx)
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. Load Balancer Configuration
```yaml
# AWS ALB
TargetGroups:
  - Name: pci-dashboard
    Port: 8501
    Protocol: HTTP
    HealthCheckPath: /
    HealthCheckIntervalSeconds: 30
    HealthCheckTimeoutSeconds: 5
    HealthyThresholdCount: 2
    UnhealthyThresholdCount: 3
```

## Monitoring & Logging

### 1. Application Monitoring
```bash
# CloudWatch (AWS)
aws logs create-log-group --log-group-name /pci-dashboard/app
aws logs create-log-stream --log-group-name /pci-dashboard/app --log-stream-name production

# Application Insights (Azure)
# Configure in Azure Portal
```

### 2. Log Aggregation
```bash
# ELK Stack
# Elasticsearch, Logstash, Kibana

# Or use managed services:
# - AWS CloudWatch
# - Azure Monitor
# - Google Cloud Logging
```

### 3. Performance Monitoring
```bash
# New Relic
# Datadog
# Prometheus + Grafana
```

### 4. Alerting
```yaml
# Alert Rules
- name: HighErrorRate
  condition: error_rate > 5%
  action: notify_team

- name: HighLatency
  condition: response_time > 5s
  action: notify_team

- name: LowDiskSpace
  condition: disk_usage > 90%
  action: notify_ops
```

## Database Setup

### PostgreSQL
```bash
# Create database
createdb pci_dashboard

# Create user
createuser pci_user
psql -c "ALTER USER pci_user WITH PASSWORD 'secure_password';"

# Grant privileges
psql -c "GRANT ALL PRIVILEGES ON DATABASE pci_dashboard TO pci_user;"
```

### Backup Strategy
```bash
# Daily backup
0 2 * * * pg_dump pci_dashboard | gzip > /backups/pci_dashboard_$(date +\%Y\%m\%d).sql.gz

# Weekly full backup
0 3 * * 0 pg_dump -Fc pci_dashboard > /backups/pci_dashboard_full_$(date +\%Y\%m\%d).dump
```

## Security Hardening

### 1. Firewall Rules
```bash
# Allow only necessary ports
- 443 (HTTPS)
- 22 (SSH, restricted to admin IPs)
- 5432 (PostgreSQL, internal only)
```

### 2. Authentication
```bash
# Enable MFA for admin accounts
# Use strong passwords
# Rotate credentials regularly
```

### 3. Data Encryption
```bash
# Enable encryption at rest
# Enable encryption in transit (TLS)
# Encrypt sensitive data in database
```

### 4. Access Control
```bash
# Implement RBAC
# Use IAM roles
# Audit access logs
```

## Performance Tuning

### 1. Database Optimization
```sql
-- Create indexes
CREATE INDEX idx_company_name ON companies(name);
CREATE INDEX idx_trial_status ON trials(overall_status);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM trials WHERE overall_status = 'COMPLETED';
```

### 2. Caching Configuration
```python
# Increase cache TTL for stable data
Config.performance.CACHE_TTL_SECONDS = 7200

# Implement Redis for distributed caching
# Configure connection pooling
```

### 3. Resource Allocation
```bash
# CPU: 2+ cores
# Memory: 4GB+ RAM
# Disk: 50GB+ SSD
# Network: 100Mbps+
```

## Maintenance

### Daily Tasks
- Monitor application logs
- Check system health
- Verify backups

### Weekly Tasks
- Review performance metrics
- Update security patches
- Test disaster recovery

### Monthly Tasks
- Database optimization
- Security audit
- Capacity planning

### Quarterly Tasks
- Full security assessment
- Performance review
- Disaster recovery drill

## Rollback Procedure

### 1. Identify Issue
```bash
# Check logs
tail -f logs/pci_dashboard.log

# Check metrics
# Review error rates
```

### 2. Rollback Steps
```bash
# Stop current version
docker stop pci-dashboard

# Restore previous version
docker run -d --name pci-dashboard pci-dashboard:1.9.0

# Verify functionality
curl http://localhost:8501
```

### 3. Post-Rollback
- Notify stakeholders
- Investigate root cause
- Plan fix
- Test thoroughly

## Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check logs
docker logs pci-dashboard

# Verify configuration
cat config/.env

# Check dependencies
pip list
```

#### High Memory Usage
```bash
# Monitor memory
docker stats pci-dashboard

# Increase cache TTL
# Reduce batch size
# Optimize queries
```

#### Slow Performance
```bash
# Check database performance
EXPLAIN ANALYZE SELECT ...

# Monitor network latency
ping database-host

# Check CPU usage
top
```

#### Database Connection Issues
```bash
# Test connection
psql -h host -U user -d database

# Check connection pool
# Verify firewall rules
# Check credentials
```

## Support & Escalation

### Support Channels
- Email: support@pci-dashboard.com
- Slack: #pci-dashboard-support
- GitHub Issues: issues

### Escalation Path
1. Level 1: Support Team
2. Level 2: Engineering Team
3. Level 3: DevOps Team
4. Level 4: Management

---

**Version**: 2.0.0
**Last Updated**: 2024
**Status**: Production Ready
