"""
FastAPI application entry point.

Features:
- Dual DB (PostgreSQL + MongoDB)
- Lifespan management
- HTML dashboard
- API routing

"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from our_app.core.loggings import logger
from our_app.core.config import settings
from our_app.core.postgres import engine, Base
from our_app.core.mongodb_async import get_async_mongo_database, close_mongo_async_client
from our_app.routes.v1.base import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager.

    Startup:
        - Connect to MongoDB
        - Create PostgreSQL tables

    Shutdown:
        - Close MongoDB connection
    """

    logger.info("Starting Pragya's Momo Profit Predictor")
    logger.debug("Connecting to MongoDB...")
    get_async_mongo_database()
    logger.info("Creating PostgreSQL tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("App is LIVE! Open /docs")
    yield
    logger.warning("Shutting down application...")
    close_mongo_async_client()
    await engine.dispose()
    logger.info("Goodbye! See you for more momos tomorrow!")


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.include_router(api_router)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Pragya's Momo Profit Predictor</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --primary: #ff6b35;
    --primary-dark: #e65100;
    --secondary: #b71c1c;
    --gold: #ffb300;
    --text: #2a1810;
    --glass: rgba(255, 255, 255, 0.15);
    --glass-border: rgba(255, 255, 255, 0.3);
  }
  html, body { height: 100%; overflow-x: hidden; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    min-height: 100vh;
    background: linear-gradient(135deg, #2c0a0a 0%, #5a1a0a 35%, #ff6b35 100%);
    color: var(--text);
    perspective: 1500px;
    position: relative;
  }

  /* Animated background blobs */
  .bg-blob {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.5;
    z-index: 0;
    pointer-events: none;
  }
  .bg-blob.b1 { width: 500px; height: 500px; background: #ff6b35; top: -150px; left: -150px; animation: blob1 18s ease-in-out infinite; }
  .bg-blob.b2 { width: 400px; height: 400px; background: #ffb300; bottom: -100px; right: -100px; animation: blob2 22s ease-in-out infinite; }
  .bg-blob.b3 { width: 350px; height: 350px; background: #b71c1c; top: 40%; left: 50%; animation: blob3 25s ease-in-out infinite; }
  @keyframes blob1 { 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(100px,150px) scale(1.2)} }
  @keyframes blob2 { 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(-120px,-100px) scale(1.3)} }
  @keyframes blob3 { 0%,100%{transform:translate(-50%,-50%) scale(1)} 50%{transform:translate(-30%,-70%) scale(1.4)} }

  /* Floating momo emojis in background */
  .floater {
    position: fixed;
    font-size: 40px;
    opacity: 0.15;
    z-index: 0;
    pointer-events: none;
    animation: float-around 20s linear infinite;
  }
  @keyframes float-around {
    0%   { transform: translate(0,0) rotate(0deg); }
    25%  { transform: translate(40px,-60px) rotate(90deg); }
    50%  { transform: translate(-30px,-120px) rotate(180deg); }
    75%  { transform: translate(-60px,-60px) rotate(270deg); }
    100% { transform: translate(0,0) rotate(360deg); }
  }

  .page {
    position: relative;
    z-index: 1;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    gap: 40px;
    flex-wrap: wrap;
  }

  /* ============== 3D MOMO STAGE ============== */
  .stage {
    width: 360px;
    height: 360px;
    perspective: 1000px;
    position: relative;
    flex-shrink: 0;
  }
  .momo-3d {
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    animation: spin 12s linear infinite;
    transition: transform 0.2s;
  }
  @keyframes spin {
    from { transform: rotateY(0deg) rotateX(-15deg); }
    to   { transform: rotateY(360deg) rotateX(-15deg); }
  }
  /* The momo body */
  .momo-body {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 200px;
    height: 200px;
    transform: translate(-50%,-50%);
    background: radial-gradient(circle at 35% 30%, #fff8e1 0%, #ffe0b2 40%, #d4a574 80%, #a67c52 100%);
    border-radius: 50%;
    box-shadow:
      inset -25px -25px 50px rgba(120,70,30,0.5),
      inset 25px 25px 50px rgba(255,250,230,0.6),
      0 30px 60px rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 130px;
    line-height: 1;
  }
  /* Pleats on momo using radial pseudo */
  .momo-body::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background:
      repeating-conic-gradient(
        from 0deg,
        rgba(140,90,40,0.15) 0deg 8deg,
        transparent 8deg 30deg
      );
    mix-blend-mode: multiply;
  }
  /* Plate beneath */
  .plate {
    position: absolute;
    bottom: 30px;
    left: 50%;
    width: 280px;
    height: 50px;
    transform: translateX(-50%) rotateX(70deg);
    background: radial-gradient(ellipse at center, #fff 0%, #e0e0e0 50%, #888 100%);
    border-radius: 50%;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
  }

  /* Steam particles */
  .steam {
    position: absolute;
    top: 20px;
    left: 50%;
    width: 30px;
    height: 30px;
    background: radial-gradient(circle, rgba(255,255,255,0.8), rgba(255,255,255,0));
    border-radius: 50%;
    transform: translateX(-50%);
    animation: rise 3s ease-out infinite;
    opacity: 0;
  }
  .steam.s1 { animation-delay: 0s; }
  .steam.s2 { animation-delay: 0.7s; left: 42%; }
  .steam.s3 { animation-delay: 1.4s; left: 58%; }
  .steam.s4 { animation-delay: 2.1s; left: 50%; }
  @keyframes rise {
    0%   { transform: translate(-50%, 0) scale(0.5); opacity: 0; }
    20%  { opacity: 0.9; }
    100% { transform: translate(-50%, -140px) scale(2); opacity: 0; }
  }

  /* ============== GLASS CARD ============== */
  .card {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(25px) saturate(180%);
    -webkit-backdrop-filter: blur(25px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 28px;
    padding: 38px;
    max-width: 480px;
    width: 100%;
    box-shadow:
      0 25px 80px rgba(0,0,0,0.4),
      inset 0 1px 0 rgba(255,255,255,0.4);
    color: #fff;
    transform-style: preserve-3d;
    transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
  }

  h1 {
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 4px;
    background: linear-gradient(135deg, #fff 0%, #ffb300 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 2px 20px rgba(255,179,0,0.3);
  }
  .subtitle {
    color: rgba(255,255,255,0.75);
    font-size: 14px;
    margin-bottom: 26px;
    letter-spacing: 0.5px;
  }

  .field { margin-bottom: 18px; }
  label.lbl {
    display: block;
    font-weight: 600;
    margin-bottom: 8px;
    font-size: 13px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.85);
  }

  /* Momo type picker — picture cards */
  .type-picker {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }
  .type-card {
    cursor: pointer;
    padding: 14px 8px;
    background: rgba(255,255,255,0.08);
    border: 2px solid rgba(255,255,255,0.18);
    border-radius: 14px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.2,0.8,0.2,1);
    transform-style: preserve-3d;
    user-select: none;
  }
  .type-card:hover {
    transform: translateY(-4px) rotateX(8deg);
    background: rgba(255,255,255,0.15);
    border-color: rgba(255,179,0,0.6);
  }
  .type-card.active {
    background: linear-gradient(135deg, rgba(255,107,53,0.4), rgba(183,28,28,0.4));
    border-color: #ffb300;
    box-shadow: 0 8px 25px rgba(255,179,0,0.4);
    transform: translateY(-4px) scale(1.05);
  }
  .type-emoji {
    font-size: 36px;
    display: block;
    margin-bottom: 4px;
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));
    transition: transform 0.3s;
  }
  .type-card:hover .type-emoji { transform: scale(1.15) rotate(-8deg); }
  .type-label {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    color: #fff;
  }
  .type-card input { display: none; }

  input[type=number] {
    width: 100%;
    padding: 13px 16px;
    border: 2px solid rgba(255,255,255,0.2);
    border-radius: 12px;
    font-size: 15px;
    background: rgba(255,255,255,0.08);
    color: #fff;
    outline: none;
    transition: all 0.2s;
  }
  input[type=number]:focus {
    border-color: #ffb300;
    background: rgba(255,255,255,0.15);
    box-shadow: 0 0 0 4px rgba(255,179,0,0.15);
  }

  .checkbox-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 24px;
  }
  .checkbox-card {
    cursor: pointer;
    padding: 14px;
    background: rgba(255,255,255,0.08);
    border: 2px solid rgba(255,255,255,0.18);
    border-radius: 14px;
    text-align: center;
    transition: all 0.3s;
    user-select: none;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-weight: 600;
    font-size: 14px;
  }
  .checkbox-card:hover {
    transform: translateY(-3px);
    background: rgba(255,255,255,0.15);
  }
  .checkbox-card.active {
    background: linear-gradient(135deg, rgba(255,107,53,0.4), rgba(183,28,28,0.4));
    border-color: #ffb300;
    box-shadow: 0 6px 20px rgba(255,179,0,0.4);
  }
  .checkbox-card input { display: none; }

  button.submit {
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, #ff6b35 0%, #e65100 50%, #b71c1c 100%);
    background-size: 200% 200%;
    color: #fff;
    border: none;
    border-radius: 14px;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 8px 25px rgba(230,81,0,0.5);
    position: relative;
    overflow: hidden;
    animation: gradient-shift 4s ease infinite;
  }
  @keyframes gradient-shift {
    0%,100% { background-position: 0% 50%; }
    50%     { background-position: 100% 50%; }
  }
  button.submit:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 35px rgba(230,81,0,0.6);
  }
  button.submit:active { transform: translateY(-1px) scale(0.99); }
  button.submit:disabled { opacity: 0.6; cursor: not-allowed; }

  .result {
    margin-top: 22px;
    padding: 22px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(255,179,0,0.2), rgba(255,107,53,0.15));
    border: 1px solid rgba(255,179,0,0.4);
    backdrop-filter: blur(10px);
    opacity: 0;
    transform: translateY(20px) rotateX(-10deg);
    transition: all 0.6s cubic-bezier(0.2,0.8,0.2,1);
    transform-style: preserve-3d;
  }
  .result.show {
    opacity: 1;
    transform: translateY(0) rotateX(0deg);
  }
  .profit-label {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.7);
    margin-bottom: 4px;
  }
  .profit {
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(135deg, #ffd54f 0%, #ff6b35 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
    line-height: 1.1;
  }
  .recommendation {
    font-size: 15px;
    color: rgba(255,255,255,0.92);
    margin-bottom: 14px;
    line-height: 1.5;
  }
  .confidence {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .confidence.High   { background: rgba(76,175,80,0.3);  color: #b9f6ca; border:1px solid rgba(76,175,80,0.6); }
  .confidence.Medium { background: rgba(255,193,7,0.3);  color: #ffe082; border:1px solid rgba(255,193,7,0.6); }
  .confidence.Low    { background: rgba(244,67,54,0.3);  color: #ffcdd2; border:1px solid rgba(244,67,54,0.6); }

  .error {
    margin-top: 16px;
    padding: 14px;
    background: rgba(244,67,54,0.2);
    border-left: 4px solid #f44336;
    border-radius: 10px;
    color: #ffcdd2;
    font-size: 14px;
    display: none;
  }
  .error.show { display: block; }

  .footer {
    text-align: center;
    margin-top: 22px;
    font-size: 13px;
    color: rgba(255,255,255,0.7);
  }
  .footer a {
    color: #ffb300;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.2s;
  }
  .footer a:hover { color: #fff; }

  /* Confetti burst when result shows */
  .confetti {
    position: fixed;
    width: 10px;
    height: 10px;
    pointer-events: none;
    z-index: 100;
    opacity: 0;
  }
  .confetti.go { animation: confetti-fall 1.6s ease-out forwards; }
  @keyframes confetti-fall {
    0%   { opacity: 1; transform: translate(0,0) rotate(0); }
    100% { opacity: 0; transform: translate(var(--dx), var(--dy)) rotate(720deg); }
  }

  @media (max-width: 760px) {
    .stage { width: 280px; height: 280px; }
    .momo-body { width: 160px; height: 160px; font-size: 100px; }
    .plate { width: 220px; }
    h1 { font-size: 24px; }
    .card { padding: 28px; }
  }
</style>
</head>
<body>
  <!-- Background atmosphere -->
  <div class="bg-blob b1"></div>
  <div class="bg-blob b2"></div>
  <div class="bg-blob b3"></div>
  <div class="floater" style="top:10%;left:8%;animation-delay:0s">🥟</div>
  <div class="floater" style="top:70%;left:5%;animation-delay:-5s">🌶️</div>
  <div class="floater" style="top:20%;right:8%;animation-delay:-10s">🥢</div>
  <div class="floater" style="top:80%;right:10%;animation-delay:-15s">🥟</div>
  <div class="floater" style="top:45%;left:48%;animation-delay:-7s;font-size:30px">✨</div>

  <div class="page">
    <!-- 3D rotating momo with steam -->
    <div class="stage">
      <div class="steam s1"></div>
      <div class="steam s2"></div>
      <div class="steam s3"></div>
      <div class="steam s4"></div>
      <div class="momo-3d" id="momo3d">
        <div class="momo-body">🥟</div>
      </div>
      <div class="plate"></div>
    </div>

    <!-- Glass form card -->
    <div class="card" id="card">
      <h1>Pragya's Momo Profit Predictor</h1>
      <p class="subtitle">AI-POWERED · DUAL DB · MADE WITH LOVE 🥟</p>

      <form id="predictForm">
        <div class="field">
          <label class="lbl">Choose your momo</label>
          <div class="type-picker">
            <label class="type-card active" data-type="BUFF">
              <input type="radio" name="momo_type" value="BUFF" checked />
              <span class="type-emoji">🥟</span>
              <span class="type-label">BUFF</span>
            </label>
            <label class="type-card" data-type="CHICKEN">
              <input type="radio" name="momo_type" value="CHICKEN" />
              <span class="type-emoji">🍗</span>
              <span class="type-label">CHICKEN</span>
            </label>
            <label class="type-card" data-type="VEG">
              <input type="radio" name="momo_type" value="VEG" />
              <span class="type-emoji">🥬</span>
              <span class="type-label">VEG</span>
            </label>
          </div>
        </div>

        <div class="field">
          <label class="lbl" for="temperature">Temperature (°C) 🌡️</label>
          <input type="number" id="temperature" step="0.1" value="18.0" required />
        </div>

        <div class="checkbox-row">
          <label class="checkbox-card" id="weekendCard">
            <input type="checkbox" id="is_weekend" />
            <span>🎉 Weekend</span>
          </label>
          <label class="checkbox-card" id="festivalCard">
            <input type="checkbox" id="is_festival" />
            <span>🪔 Festival</span>
          </label>
        </div>

        <button type="submit" class="submit" id="submitBtn">🚀 Predict Profit</button>
      </form>

      <div class="result" id="result">
        <div class="profit-label">Predicted Profit</div>
        <div class="profit" id="profit"></div>
        <div class="recommendation" id="recommendation"></div>
        <span class="confidence" id="confidence"></span>
      </div>

      <div class="error" id="error"></div>

      <div class="footer">
        <a href="/docs">📚 Open Swagger UI →</a>
      </div>
    </div>
  </div>

<script>
  // Momo type picker
  document.querySelectorAll('.type-card').forEach(card => {
    card.addEventListener('click', () => {
      document.querySelectorAll('.type-card').forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      card.querySelector('input').checked = true;
    });
  });

  // Weekend/Festival toggles
  ['weekendCard', 'festivalCard'].forEach(id => {
    const card = document.getElementById(id);
    const input = card.querySelector('input');
    card.addEventListener('click', (e) => {
      e.preventDefault();
      input.checked = !input.checked;
      card.classList.toggle('active', input.checked);
    });
  });

  // 3D tilt on the card following the mouse
  const card = document.getElementById('card');
  document.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = (e.clientX - cx) / rect.width;
    const dy = (e.clientY - cy) / rect.height;
    card.style.transform = `rotateY(${dx * 6}deg) rotateX(${-dy * 6}deg)`;
  });
  document.addEventListener('mouseleave', () => {
    card.style.transform = 'rotateY(0) rotateX(0)';
  });

  // Confetti burst
  function burstConfetti() {
    const colors = ['#ffb300','#ff6b35','#e65100','#b71c1c','#fff8e1','#ffd54f'];
    const cx = window.innerWidth / 2;
    const cy = window.innerHeight / 2;
    for (let i = 0; i < 40; i++) {
      const el = document.createElement('div');
      el.className = 'confetti go';
      el.style.left = cx + 'px';
      el.style.top = cy + 'px';
      el.style.background = colors[Math.floor(Math.random() * colors.length)];
      el.style.setProperty('--dx', (Math.random() - 0.5) * 800 + 'px');
      el.style.setProperty('--dy', (Math.random() - 0.7) * 800 + 'px');
      el.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 1700);
    }
  }

  // Form submit
  const form = document.getElementById('predictForm');
  const resultEl = document.getElementById('result');
  const errorEl = document.getElementById('error');
  const btn = document.getElementById('submitBtn');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    resultEl.classList.remove('show');
    errorEl.classList.remove('show');
    btn.disabled = true;
    btn.textContent = '⏳ Predicting...';

    const checked = document.querySelector('input[name="momo_type"]:checked');
    const payload = {
      momo_type: checked.value,
      temperature: parseFloat(document.getElementById('temperature').value),
      is_weekend: document.getElementById('is_weekend').checked,
      is_festival: document.getElementById('is_festival').checked,
    };

    try {
      const res = await fetch('/api/v1/momo/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error('Server returned ' + res.status);
      const data = await res.json();
      document.getElementById('profit').textContent = 'NPR ' + data.predicted_profit_npr.toLocaleString();
      document.getElementById('recommendation').textContent = data.recommendation;
      const conf = document.getElementById('confidence');
      conf.textContent = data.confidence + ' Confidence';
      conf.className = 'confidence ' + data.confidence;
      resultEl.classList.add('show');
      burstConfetti();
    } catch (err) {
      errorEl.textContent = '⚠️ ' + err.message;
      errorEl.classList.add('show');
    } finally {
      btn.disabled = false;
      btn.textContent = '🚀 Predict Profit';
    }
  });
</script>
</body>
</html>
"""
