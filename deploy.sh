#!/bin/bash

echo "🚀 E-HARMONY DEPLOY PROFISSIONAL"
echo "=================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 OPÇÕES DE DEPLOY:${NC}"
echo "1. Railway + Vercel (Recomendado - Grátis)"
echo "2. Render + Netlify (Alternativa - Grátis)"
echo "3. Manual (AWS/DigitalOcean)"
echo ""

read -p "Escolha uma opção (1-3): " choice

case $choice in
    1)
        echo -e "${GREEN}✅ Deploy com Railway + Vercel${NC}"
        echo ""
        echo "🔧 PASSO 1: Deploy do Backend (Railway)"
        echo "   1. Acesse: https://railway.app"
        echo "   2. Conecte seu GitHub"
        echo "   3. Clique 'New Project' > 'Deploy from GitHub repo'"
        echo "   4. Selecione o repositório do backend"
        echo "   5. Railway detecta Python automaticamente"
        echo "   6. Adicione PostgreSQL: Add Service > Database > PostgreSQL"
        echo "   7. Configure variáveis de ambiente:"
        echo "      - SECRET_KEY=seu_secret_key_aqui"
        echo "      - OPENAI_API_KEY=sua_chave_openai"
        echo "   8. Deploy automático em ~3 minutos"
        echo ""
        echo "🎨 PASSO 2: Deploy do Frontend (Vercel)"
        echo "   1. Acesse: https://vercel.com"
        echo "   2. Conecte seu GitHub"
        echo "   3. Import Project > selecione repo frontend"
        echo "   4. Configure Build Settings:"
        echo "      - Framework: Create React App"
        echo "      - Build Command: npm run build"
        echo "      - Output Directory: build"
        echo "   5. Adicione variável de ambiente:"
        echo "      - REACT_APP_API_URL=https://[sua-url-railway].railway.app"
        echo "   6. Deploy em ~2 minutos"
        echo ""
        echo -e "${GREEN}🎯 URLS FINAIS:${NC}"
        echo "   Frontend: https://e-harmony-[hash].vercel.app"
        echo "   Backend:  https://[projeto]-[hash].railway.app"
        ;;
    2)
        echo -e "${GREEN}✅ Deploy com Render + Netlify${NC}"
        echo ""
        echo "🔧 PASSO 1: Deploy do Backend (Render)"
        echo "   1. Acesse: https://render.com"
        echo "   2. Conecte GitHub e selecione repo backend"
        echo "   3. Configure:"
        echo "      - Environment: Python"
        echo "      - Build Command: pip install -r requirements.txt"
        echo "      - Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
        echo "   4. Adicione PostgreSQL: New > PostgreSQL"
        echo "   5. Configure variáveis de ambiente"
        echo "   6. Deploy em ~5 minutos"
        echo ""
        echo "🎨 PASSO 2: Deploy do Frontend (Netlify)"
        echo "   1. Acesse: https://netlify.com"
        echo "   2. Drag & drop da pasta build/ OU conecte GitHub"
        echo "   3. Configure Build:"
        echo "      - Build command: npm run build"
        echo "      - Publish directory: build"
        echo "   4. Adicione variável: REACT_APP_API_URL"
        echo "   5. Deploy em ~2 minutos"
        ;;
    3)
        echo -e "${YELLOW}⚙️ Deploy Manual${NC}"
        echo "Para AWS/DigitalOcean/outros provedores:"
        echo "1. Configure um servidor Linux"
        echo "2. Instale Docker e Docker Compose"
        echo "3. Execute: docker-compose -f docker-compose.prod.yml up -d"
        echo "4. Configure nginx proxy e SSL"
        ;;
    *)
        echo -e "${RED}❌ Opção inválida${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 APÓS O DEPLOY:${NC}"
echo "✅ Backend com PostgreSQL funcionando"
echo "✅ Frontend com SSL automático"
echo "✅ APIs integradas e funcionais"
echo "✅ Sistema completo online"
echo ""
echo -e "${BLUE}🔗 O E-harmony estará disponível nos URLs fornecidos!${NC}"
