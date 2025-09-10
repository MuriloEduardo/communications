#!/bin/bash

# Script para configurar HTTPS no Elastic Beanstalk
# Execute este script após criar o certificado SSL no AWS

echo "=== Configurando HTTPS para maestrocommunications.shop ==="

# Obter o ARN do certificado (substitua CERTIFICATE_ID pelo ID real)
echo "1. Primeiro, obtenha o ARN do certificado SSL no AWS Console"
echo "   AWS Console > Certificate Manager > Seu certificado > ARN"
echo ""

# Atualizar o arquivo de configuração
echo "2. Atualize o arquivo .ebextensions/02_https.config com o ARN real"
echo "   Substitua: arn:aws:acm:us-west-2:ACCOUNT_ID:certificate/CERTIFICATE_ID"
echo "   Pelo ARN real do seu certificado"
echo ""

echo "3. Deploy as mudanças:"
echo "   git add ."
echo "   git commit -m 'Configure HTTPS with SSL certificate'"
echo "   eb deploy communications-env"
echo ""

echo "4. Teste após o deploy:"
echo "   curl -I https://maestrocommunications.shop/"
echo "   curl -I http://maestrocommunications.shop/ (deve redirecionar para HTTPS)"
