const express = require('express');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

const isProd = process.env.NODE_ENV === 'production';

// In development, disable etag completely so the browser always gets the fresh file
if (!isProd) {
  app.disable('etag');
}

// ── Security headers (CSP disabled — app uses inline scripts & onclick handlers) ──
app.use(
  helmet({
    contentSecurityPolicy: false,
  })
);

// ── Gzip / Brotli compression ──
app.use(compression());

// ── CORS ──
app.use(cors());

// ── Request logging ──
app.use(morgan(isProd ? 'combined' : 'dev'));

// ── Disable cache in development ──
app.use((req, res, next) => {
  if (!isProd) {
    res.set('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
    res.set('Pragma', 'no-cache');
    res.set('Expires', '0');
  }
  next();
});

// ── Cache control for static assets ──
app.use(
  express.static(path.join(__dirname, 'public'), {
    maxAge: isProd ? '1d' : 0,
    etag: isProd,
    lastModified: isProd,
  })
);

// ── SPA fallback — always serve index.html for any unknown route ──
app.get('{*path}', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// ── Error handler ──
app.use((err, req, res, next) => {
  console.error('Server error:', err.message);
  res.status(500).json({ error: 'Internal Server Error' });
});

// ── Start server ──
app.listen(PORT, '0.0.0.0', () => {
  console.log(`
  ╔═══════════════════════════════════════════════════════╗
  ║   🚀  Grammar Quiz Server is RUNNING                 ║
  ║                                                       ║
  ║   Local:    http://localhost:${PORT}                    ║
  ║   Network:  http://0.0.0.0:${PORT}                     ║
  ║   Mode:     ${(process.env.NODE_ENV || 'development').padEnd(13)}                   ║
  ╚═══════════════════════════════════════════════════════╝
  `);
});
