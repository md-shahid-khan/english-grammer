const express = require('express');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// ── Security headers ──
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
        fontSrc: ["'self'", "https://fonts.gstatic.com"],
        scriptSrc: ["'self'", "'unsafe-inline'"],   // inline scripts in index.html
        imgSrc: ["'self'", "data:"],
      },
    },
  })
);

// ── Gzip / Brotli compression ──
app.use(compression());

// ── CORS ──
app.use(cors());

// ── Request logging ──
app.use(morgan(process.env.NODE_ENV === 'production' ? 'combined' : 'dev'));

// ── Cache control for static assets ──
app.use(
  express.static(path.join(__dirname, 'public'), {
    maxAge: process.env.NODE_ENV === 'production' ? '1d' : 0,
    etag: true,
    lastModified: true,
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
