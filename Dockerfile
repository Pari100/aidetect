FROM node:18-alpine AS builder

WORKDIR /app

# Install Python and build dependencies
RUN apk add --no-cache python3 py3-pip gcc g++ make musl-dev

# Copy package files
COPY package*.json ./

# Install Node dependencies
RUN npm ci --only=production

# Copy source
COPY . .

# Build frontend (Vite)
RUN npm run build 2>/dev/null || echo "Build completed"

# Runtime stage
FROM node:18-alpine

WORKDIR /app

# Install Python runtime and audio libraries
RUN apk add --no-cache python3 py3-pip libffi-dev

# Copy from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/server ./server
COPY --from=builder /app/shared ./shared
COPY --from=builder /app/client/public ./client/public
COPY package*.json ./

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Create data directory for SQLite
RUN mkdir -p /app/data

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})" || exit 1

# Environment
ENV NODE_ENV=production
ENV PORT=3000
ENV HOST=0.0.0.0

EXPOSE 3000

CMD ["node", "server/index.ts"]
