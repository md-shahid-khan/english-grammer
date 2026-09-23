import json

with open('public/voice_questions.json', 'r', encoding='utf-8') as f:
    voice_questions = json.load(f)

with open('public/para_jumbles.json', 'r', encoding='utf-8') as f:
    pj_questions = json.load(f)

print(f"Loaded {len(voice_questions)} voice and {len(pj_questions)} PJ questions.")

for q in voice_questions:
    q['type'] = 'voice'
    if 'id' not in q:
        q['id'] = 1

for q in pj_questions:
    q['type'] = 'parajumbles'

voice_json_str = json.dumps(voice_questions, ensure_ascii=False)
pj_json_str = json.dumps(pj_questions, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SSC English PYQ Practice Test — Voice &amp; Para Jumbles</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --primary: #4f46e5;
            --primary-light: #818cf8;
            --primary-dark: #3730a3;
            --success: #059669;
            --success-bg: #d1fae5;
            --danger: #dc2626;
            --danger-bg: #fee2e2;
            --warning: #d97706;
            --warning-bg: #fef3c7;
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #1e293b;
            --text-secondary: #64748b;
            --border: #e2e8f0;
            --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
            --shadow-lg: 0 10px 25px rgba(0,0,0,0.1), 0 6px 10px rgba(0,0,0,0.08);
            --radius: 12px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            line-height: 1.6;
        }

        /* ── Header ── */
        .header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 16px 24px;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 4px 12px rgba(79,70,229,0.3);
        }
        .header-inner {
            max-width: 900px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .header h1 {
            font-size: 18px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .header h1 .icon { font-size: 22px; }
        .header-stats {
            display: flex;
            gap: 16px;
            font-size: 14px;
            font-weight: 500;
        }
        .header-stats span {
            display: flex;
            align-items: center;
            gap: 5px;
            background: rgba(255,255,255,0.18);
            padding: 5px 12px;
            border-radius: 20px;
            backdrop-filter: blur(4px);
        }

        /* ── Timer Badge ── */
        .timer-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255,255,255,0.18);
            padding: 5px 14px;
            border-radius: 20px;
            backdrop-filter: blur(4px);
            transition: all 0.3s ease;
        }
        .timer-badge.urgent {
            background: #fee2e2 !important;
            color: #dc2626 !important;
            font-weight: 800;
            box-shadow: 0 0 0 2px #ef4444;
            animation: timerPulse 0.9s infinite alternate;
        }
        @keyframes timerPulse {
            from { transform: scale(1); }
            to { transform: scale(1.05); }
        }

        /* ── Progress Bar ── */
        .progress-wrapper {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px 24px 0;
        }
        .progress-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 6px;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-secondary);
        }
        .progress-bar {
            height: 8px;
            background: var(--border);
            border-radius: 20px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--primary-light));
            border-radius: 20px;
            transition: width 0.3s ease;
            width: 0%;
        }

        /* ── Main Container ── */
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px 24px 40px;
        }

        /* ── Mode Selection on Start Screen ── */
        .mode-selection-title {
            font-size: 16px;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 12px;
            text-align: left;
        }
        .mode-cards {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 30px;
            text-align: left;
        }
        .mode-card {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 18px 20px;
            background: var(--card);
            border: 2px solid var(--border);
            border-radius: var(--radius);
            cursor: pointer;
            transition: all 0.2s ease;
            user-select: none;
        }
        .mode-card:hover {
            border-color: var(--primary-light);
            background: #f0f0ff;
        }
        .mode-card.active {
            border-color: var(--primary);
            background: #eef2ff;
            box-shadow: 0 0 0 3px rgba(79,70,229,0.15);
        }
        .mode-card-radio {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            border: 2px solid #cbd5e1;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            transition: all 0.2s ease;
        }
        .mode-card.active .mode-card-radio {
            border-color: var(--primary);
            background: var(--primary);
        }
        .mode-card.active .mode-card-radio::after {
            content: '';
            width: 8px;
            height: 8px;
            background: white;
            border-radius: 50%;
        }
        .mode-card-icon {
            font-size: 28px;
            flex-shrink: 0;
        }
        .mode-card-info {
            flex: 1;
        }
        .mode-card-name {
            font-size: 16px;
            font-weight: 700;
            color: var(--text);
        }
        .mode-card-sub {
            font-size: 13px;
            color: var(--text-secondary);
            margin-top: 2px;
        }
        .mode-card-badge {
            font-size: 12px;
            font-weight: 700;
            color: var(--primary);
            background: #e0e7ff;
            padding: 4px 12px;
            border-radius: 20px;
        }

        /* ── Question Card ── */
        .question-card {
            background: var(--card);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 32px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
        }
        .question-top-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            gap: 10px;
            flex-wrap: wrap;
        }
        .question-badge {
            display: inline-flex;
            align-items: center;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
            font-size: 12px;
            font-weight: 700;
            padding: 4px 14px;
            border-radius: 20px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .topic-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 20px;
            background: #e0e7ff;
            color: var(--primary);
        }
        .question-prompt {
            font-size: 17px;
            font-weight: 600;
            line-height: 1.6;
            color: var(--text);
            margin-bottom: 20px;
        }

        /* ── Para Jumbles Sentences Box ── */
        .pj-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 24px;
        }
        .pj-sentence-row {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 12px 16px;
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 8px;
            transition: all 0.15s ease;
        }
        .pj-sentence-row:hover {
            background: #f1f5f9;
        }
        .pj-tag {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 32px;
            height: 28px;
            padding: 0 8px;
            background: var(--primary);
            color: white;
            font-weight: 700;
            font-size: 13px;
            border-radius: 6px;
            flex-shrink: 0;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        .pj-text {
            font-size: 15px;
            color: var(--text);
            line-height: 1.55;
            padding-top: 2px;
        }

        /* ── Options ── */
        .options-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .option {
            display: flex;
            align-items: flex-start;
            gap: 14px;
            padding: 16px 20px;
            border: 2px solid var(--border);
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
            background: var(--card);
            user-select: none;
        }
        .option:hover {
            border-color: var(--primary-light);
            background: #f0f0ff;
        }
        .option.selected {
            border-color: var(--primary);
            background: #eef2ff;
            box-shadow: 0 0 0 3px rgba(79,70,229,0.15);
        }
        .option-radio {
            width: 22px;
            height: 22px;
            min-width: 22px;
            border-radius: 50%;
            border: 2px solid #cbd5e1;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 2px;
            transition: all 0.2s ease;
        }
        .option.selected .option-radio {
            border-color: var(--primary);
            background: var(--primary);
        }
        .option.selected .option-radio::after {
            content: '';
            width: 8px;
            height: 8px;
            background: white;
            border-radius: 50%;
        }
        .option-label {
            font-weight: 700;
            color: var(--primary);
            min-width: 24px;
        }
        .option-text {
            font-size: 15px;
            line-height: 1.6;
            color: var(--text);
            font-weight: 500;
        }

        /* Review mode option coloring */
        .option.correct-answer {
            border-color: var(--success);
            background: var(--success-bg);
        }
        .option.correct-answer .option-radio {
            border-color: var(--success);
            background: var(--success);
        }
        .option.correct-answer .option-radio::after {
            content: '✓';
            color: white;
            font-size: 13px;
            font-weight: 700;
        }
        .option.wrong-answer {
            border-color: var(--danger);
            background: var(--danger-bg);
        }
        .option.wrong-answer .option-radio {
            border-color: var(--danger);
            background: var(--danger);
        }
        .option.wrong-answer .option-radio::after {
            content: '✕';
            color: white;
            font-size: 13px;
            font-weight: 700;
        }

        /* ── Navigation ── */
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 28px;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: inherit;
        }
        .btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }
        .btn-secondary {
            background: var(--border);
            color: var(--text);
        }
        .btn-secondary:hover:not(:disabled) {
            background: #cbd5e1;
        }
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
            box-shadow: 0 4px 12px rgba(79,70,229,0.3);
        }
        .btn-primary:hover:not(:disabled) {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(79,70,229,0.4);
        }
        .btn-success {
            background: linear-gradient(135deg, var(--success), #047857);
            color: white;
            box-shadow: 0 4px 12px rgba(5,150,105,0.3);
        }
        .btn-success:hover:not(:disabled) {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(5,150,105,0.4);
        }

        /* ── Question Navigator Palette ── */
        .question-nav-palette {
            background: var(--card);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 20px;
            margin-top: 24px;
            border: 1px solid var(--border);
        }
        .palette-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }
        .palette-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(38px, 1fr));
            gap: 6px;
        }
        .palette-btn {
            width: 100%;
            aspect-ratio: 1;
            border: 2px solid var(--border);
            border-radius: 8px;
            background: var(--card);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            color: var(--text-secondary);
        }
        .palette-btn:hover {
            border-color: var(--primary-light);
            background: #f0f0ff;
        }
        .palette-btn.current {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        .palette-btn.answered {
            background: #e0e7ff;
            border-color: var(--primary-light);
            color: var(--primary);
        }
        .palette-btn.answered.current {
            background: var(--primary);
            color: white;
        }

        /* Review palette */
        .palette-btn.review-correct {
            background: var(--success-bg);
            border-color: var(--success);
            color: var(--success);
        }
        .palette-btn.review-wrong {
            background: var(--danger-bg);
            border-color: var(--danger);
            color: var(--danger);
        }
        .palette-btn.review-correct.current {
            background: var(--success);
            color: white;
        }
        .palette-btn.review-wrong.current {
            background: var(--danger);
            color: white;
        }

        /* ── Legend ── */
        .legend {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            margin-top: 12px;
            font-size: 12px;
            color: var(--text-secondary);
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .legend-dot {
            width: 14px;
            height: 14px;
            border-radius: 4px;
            border: 2px solid var(--border);
        }
        .legend-dot.not-visited { background: var(--card); }
        .legend-dot.answered-dot { background: #e0e7ff; border-color: var(--primary-light); }
        .legend-dot.current-dot { background: var(--primary); border-color: var(--primary); }

        /* ── Start Screen ── */
        .start-screen {
            text-align: center;
            padding: 40px 20px;
        }
        .start-screen .logo {
            font-size: 56px;
            margin-bottom: 16px;
        }
        .start-screen h2 {
            font-size: 30px;
            font-weight: 800;
            margin-bottom: 8px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .start-screen .subtitle {
            font-size: 16px;
            color: var(--text-secondary);
            margin-bottom: 30px;
        }
        .test-info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 16px;
            max-width: 580px;
            margin: 0 auto 32px;
        }
        .test-info-item {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 16px;
            box-shadow: var(--shadow);
        }
        .test-info-item .num {
            font-size: 26px;
            font-weight: 800;
            color: var(--primary);
        }
        .test-info-item .label {
            font-size: 13px;
            color: var(--text-secondary);
            font-weight: 500;
        }

        /* ── Result Screen ── */
        .result-screen {
            text-align: center;
        }
        .score-circle {
            width: 190px;
            height: 190px;
            border-radius: 50%;
            margin: 0 auto 28px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow-lg);
        }
        .score-circle.excellent {
            background: linear-gradient(135deg, #d1fae5, #a7f3d0);
            border: 4px solid var(--success);
        }
        .score-circle.good {
            background: linear-gradient(135deg, #dbeafe, #bfdbfe);
            border: 4px solid #3b82f6;
        }
        .score-circle.average {
            background: linear-gradient(135deg, var(--warning-bg), #fde68a);
            border: 4px solid var(--warning);
        }
        .score-circle.poor {
            background: linear-gradient(135deg, var(--danger-bg), #fecaca);
            border: 4px solid var(--danger);
        }
        .score-value {
            font-size: 46px;
            font-weight: 800;
            line-height: 1;
        }
        .score-total {
            font-size: 15px;
            font-weight: 600;
            opacity: 0.7;
        }
        .score-percent {
            font-size: 16px;
            font-weight: 700;
            margin-top: 4px;
        }
        .result-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            max-width: 500px;
            margin: 0 auto 28px;
        }
        .stat-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 16px;
            box-shadow: var(--shadow);
        }
        .stat-card .stat-num {
            font-size: 28px;
            font-weight: 800;
        }
        .stat-card .stat-label {
            font-size: 12px;
            color: var(--text-secondary);
            font-weight: 500;
        }
        .stat-card.correct .stat-num { color: var(--success); }
        .stat-card.wrong .stat-num { color: var(--danger); }
        .stat-card.unanswered .stat-num { color: var(--warning); }

        .result-message {
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .result-sub {
            font-size: 15px;
            color: var(--text-secondary);
            margin-bottom: 24px;
        }
        .result-actions {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        /* ── Modal Overlay ── */
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.6);
            z-index: 999;
            display: none;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(2px);
        }
        .modal-overlay.active {
            display: flex;
        }

        /* ── Timer ── */
        .timer {
            font-variant-numeric: tabular-nums;
        }

        /* ── Responsive ── */
        @media (max-width: 640px) {
            .header h1 { font-size: 15px; }
            .header-stats { gap: 8px; font-size: 12px; }
            .question-card { padding: 20px; }
            .question-prompt { font-size: 15px; }
            .option { padding: 12px 14px; gap: 10px; }
            .btn { padding: 10px 18px; font-size: 14px; }
            .palette-grid { grid-template-columns: repeat(auto-fill, minmax(34px, 1fr)); }
            .start-screen h2 { font-size: 22px; }
            .score-circle { width: 150px; height: 150px; }
            .score-value { font-size: 38px; }
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeIn 0.25s ease forwards;
        }

        .hidden { display: none !important; }
    </style>
</head>
<body>

<!-- ═════════════ HEADER ═════════════ -->
<div class="header">
    <div class="header-inner">
        <h1><span class="icon">📝</span> <span id="headerTitle">SSC English PYQ Practice</span></h1>
        <div class="header-stats" id="headerStats">
            <span class="timer-badge" id="timerBadge">⏱ <span class="timer" id="timerDisplay">45:00</span></span>
            <span>📊 <span id="answeredCount">0</span>/<span id="headerTotal">100</span></span>
        </div>
    </div>
</div>

<!-- ═════════════ START SCREEN ═════════════ -->
<div class="container" id="startScreen">
    <div class="start-screen fade-in">
        <div class="logo">🎯</div>
        <h2>SSC English Practice Test</h2>
        <p class="subtitle">Official Previous Year Questions — 45 Minutes Time Limit</p>

        <!-- Mode Selector Cards -->
        <div style="max-width:580px; margin:0 auto;">
            <div class="mode-selection-title">Choose Topic to Practice:</div>
            <div class="mode-cards">
                <div class="mode-card active" id="modeCardVoice" onclick="chooseMode('voice')">
                    <div class="mode-card-radio"></div>
                    <div class="mode-card-icon">🗣️</div>
                    <div class="mode-card-info">
                        <div class="mode-card-name">Active &amp; Passive Voice</div>
                        <div class="mode-card-sub">100 Questions — Voice PYQ Practice (Episode 1)</div>
                    </div>
                    <div class="mode-card-badge">100 Qs</div>
                </div>

                <div class="mode-card" id="modeCardPJ" onclick="chooseMode('parajumbles')">
                    <div class="mode-card-radio"></div>
                    <div class="mode-card-icon">🧩</div>
                    <div class="mode-card-info">
                        <div class="mode-card-name">Para Jumbles / Rearrangement</div>
                        <div class="mode-card-sub">25 Questions — Sentence Rearrangement (Episode 4)</div>
                    </div>
                    <div class="mode-card-badge">25 Qs</div>
                </div>

                <div class="mode-card" id="modeCardBoth" onclick="chooseMode('both')">
                    <div class="mode-card-radio"></div>
                    <div class="mode-card-icon">📚</div>
                    <div class="mode-card-info">
                        <div class="mode-card-name">Both Topics (Full Practice)</div>
                        <div class="mode-card-sub">Combined 125 Questions — Voice + Para Jumbles</div>
                    </div>
                    <div class="mode-card-badge">125 Qs</div>
                </div>
            </div>
        </div>

        <div class="test-info-grid">
            <div class="test-info-item">
                <div class="num" id="infoQuestionsCount">100</div>
                <div class="label">Questions</div>
            </div>
            <div class="test-info-item">
                <div class="num">4</div>
                <div class="label">Options Each</div>
            </div>
            <div class="test-info-item">
                <div class="num">45 min</div>
                <div class="label">Time Limit</div>
            </div>
        </div>

        <button class="btn btn-primary" id="startBtn" onclick="startTest()" style="font-size:18px; padding:16px 48px; cursor:pointer;">
            🚀 Start Test
        </button>
    </div>
</div>

<!-- ═════════════ QUIZ SCREEN ═════════════ -->
<div class="hidden" id="quizScreen">
    <div class="progress-wrapper">
        <div class="progress-info">
            <span id="progressText">Question 1 of 100</span>
            <span id="progressPercent">0%</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" id="progressFill"></div>
        </div>
    </div>
    <div class="container">
        <div class="question-card fade-in" id="questionCard">
            <div class="question-top-row">
                <div class="question-badge" id="questionBadge">Question 1</div>
                <div class="topic-badge" id="topicBadge">🗣️ Active &amp; Passive Voice</div>
            </div>
            <div class="question-prompt" id="questionPrompt"></div>
            <!-- Para jumble sentences container -->
            <div class="pj-container hidden" id="pjContainer"></div>
            <!-- Options list -->
            <div class="options-list" id="optionsList"></div>
        </div>

        <div class="nav-buttons">
            <button class="btn btn-secondary" id="prevBtn" onclick="navigate(-1)" disabled>
                ← Previous
            </button>
            <button class="btn btn-secondary" id="clearBtn" onclick="clearSelection()">
                ✕ Clear
            </button>
            <button class="btn btn-primary" id="nextBtn" onclick="navigate(1)">
                Next →
            </button>
            <button class="btn btn-success hidden" id="submitBtn" onclick="confirmSubmit()">
                ✅ Submit Test
            </button>
        </div>

        <div class="question-nav-palette">
            <div class="palette-title">Question Navigator</div>
            <div class="palette-grid" id="paletteGrid"></div>
            <div class="legend">
                <div class="legend-item"><div class="legend-dot not-visited"></div> Not Visited</div>
                <div class="legend-item"><div class="legend-dot answered-dot"></div> Answered</div>
                <div class="legend-item"><div class="legend-dot current-dot"></div> Current</div>
            </div>
        </div>
    </div>
</div>

<!-- ═════════════ RESULT SCREEN ═════════════ -->
<div class="hidden" id="resultScreen">
    <div class="container">
        <div class="result-screen fade-in" id="resultContent"></div>
    </div>
</div>

<!-- ═════════════ REVIEW SCREEN ═════════════ -->
<div class="hidden" id="reviewScreen">
    <div class="progress-wrapper">
        <div class="progress-info">
            <span id="reviewProgressText">Reviewing 1 of 100</span>
            <span id="reviewFilter">
                <select id="filterSelect" onchange="applyFilter()" style="padding:5px 10px; border-radius:6px; border:1px solid var(--border); font-family:inherit; font-size:13px; font-weight:600;">
                    <option value="all">All Questions</option>
                    <option value="wrong">Wrong Only</option>
                    <option value="correct">Correct Only</option>
                    <option value="unanswered">Unanswered Only</option>
                </select>
            </span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" id="reviewProgressFill"></div>
        </div>
    </div>
    <div class="container">
        <div class="question-card fade-in" id="reviewQuestionCard">
            <div class="question-top-row">
                <div class="question-badge" id="reviewBadge">Question 1</div>
                <div class="topic-badge" id="reviewTopicBadge">🗣️ Active &amp; Passive Voice</div>
            </div>
            <div id="reviewStatus" style="margin-bottom:14px; font-size:14px; font-weight:700;"></div>
            <div class="question-prompt" id="reviewQuestionPrompt"></div>
            <div class="pj-container hidden" id="reviewPjContainer"></div>
            <div class="options-list" id="reviewOptionsList"></div>
        </div>

        <div class="nav-buttons">
            <button class="btn btn-secondary" id="reviewPrevBtn" onclick="reviewNavigate(-1)">
                ← Previous
            </button>
            <button class="btn btn-secondary" id="reviewBackBtn" onclick="showResults()">
                📊 Back to Score
            </button>
            <button class="btn btn-primary" id="reviewNextBtn" onclick="reviewNavigate(1)">
                Next →
            </button>
        </div>

        <div class="question-nav-palette">
            <div class="palette-title">Review Navigator</div>
            <div class="palette-grid" id="reviewPaletteGrid"></div>
            <div class="legend">
                <div class="legend-item"><div class="legend-dot" style="background:#d1fae5;border-color:#059669"></div> Correct</div>
                <div class="legend-item"><div class="legend-dot" style="background:#fee2e2;border-color:#dc2626"></div> Wrong</div>
                <div class="legend-item"><div class="legend-dot" style="background:#fef3c7;border-color:#d97706"></div> Unanswered</div>
            </div>
        </div>
    </div>
</div>

<!-- ═════════════ CONFIRM SUBMIT MODAL ═════════════ -->
<div id="confirmModal" class="modal-overlay">
    <div style="background:white;border-radius:16px;padding:32px;max-width:420px;width:90%;text-align:center;box-shadow:var(--shadow-lg);">
        <div style="font-size:48px;margin-bottom:12px;">⚠️</div>
        <h3 style="font-size:20px;margin-bottom:8px;">Submit Test?</h3>
        <p id="confirmText" style="color:var(--text-secondary);margin-bottom:24px;line-height:1.5;"></p>
        <div style="display:flex;gap:12px;justify-content:center;">
            <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
            <button class="btn btn-success" onclick="submitTest()">Yes, Submit</button>
        </div>
    </div>
</div>

<script>
// ═══════════════════════════════════════════════════
// QUESTION DATA
// ═══════════════════════════════════════════════════
const VOICE_DATA = __VOICE_DATA__;
const PJ_DATA = __PJ_DATA__;

// ═══════════════════════════════════════════════════
// APPLICATION STATE
// ═══════════════════════════════════════════════════
const MAX_TIME_SECONDS = 45 * 60; // 45 minutes = 2700s
let selectedMode = 'voice'; // 'voice' | 'parajumbles' | 'both'
let activeQuestions = [];
let currentQ = 0;
let userAnswers = [];
let timerInterval = null;
let remainingSeconds = MAX_TIME_SECONDS;
let autoSubmittedDueToTime = false;
let isSubmitted = false;
let reviewIndex = 0;
let filteredIndices = [];

// ═══════════════════════════════════════════════════
// MODE SELECTION
// ═══════════════════════════════════════════════════
function chooseMode(mode) {
    selectedMode = mode;
    document.getElementById('modeCardVoice').classList.toggle('active', mode === 'voice');
    document.getElementById('modeCardPJ').classList.toggle('active', mode === 'parajumbles');
    document.getElementById('modeCardBoth').classList.toggle('active', mode === 'both');

    const count = mode === 'voice' ? 100 : (mode === 'parajumbles' ? 25 : 125);
    document.getElementById('infoQuestionsCount').textContent = count;
}

// ═══════════════════════════════════════════════════
// TIMER (45 MINUTES COUNTDOWN + AUTO SUBMISSION)
// ═══════════════════════════════════════════════════
function startTimer() {
    clearInterval(timerInterval);
    updateTimerDisplay();
    timerInterval = setInterval(() => {
        remainingSeconds--;
        if (remainingSeconds <= 0) {
            remainingSeconds = 0;
            updateTimerDisplay();
            clearInterval(timerInterval);
            autoSubmitTest();
            return;
        }
        updateTimerDisplay();
    }, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
}

function updateTimerDisplay() {
    const m = String(Math.floor(remainingSeconds / 60)).padStart(2, '0');
    const s = String(remainingSeconds % 60).padStart(2, '0');
    const displayEl = document.getElementById('timerDisplay');
    if (displayEl) displayEl.textContent = `${m}:${s}`;

    const badge = document.getElementById('timerBadge');
    if (badge) {
        // Red pulse warning when 5 minutes or less remain
        badge.classList.toggle('urgent', remainingSeconds <= 300 && remainingSeconds > 0);
    }
}

function autoSubmitTest() {
    autoSubmittedDueToTime = true;
    closeModal();
    isSubmitted = true;
    showResults();
}

function getTimeUsedString() {
    const used = MAX_TIME_SECONDS - remainingSeconds;
    const m = Math.floor(used / 60);
    const s = used % 60;
    return `${m}m ${s}s`;
}

// ═══════════════════════════════════════════════════
// START TEST
// ═══════════════════════════════════════════════════
function startTest() {
    // Populate active questions based on mode
    if (selectedMode === 'voice') {
        activeQuestions = VOICE_DATA.map(q => ({
            type: 'voice',
            prompt: q.q,
            options: q.options,
            answer: q.answer,
            category: 'Active & Passive Voice'
        }));
        document.getElementById('headerTitle').textContent = 'Voice PYQ Practice (100 Qs)';
    } else if (selectedMode === 'parajumbles') {
        activeQuestions = PJ_DATA.map(q => ({
            type: 'parajumbles',
            prompt: q.prompt,
            sentences: q.sentences,
            options: q.options,
            answer: q.answer,
            category: 'Para Jumbles'
        }));
        document.getElementById('headerTitle').textContent = 'Para Jumbles Practice (25 Qs)';
    } else {
        // Both topics
        const vList = VOICE_DATA.map(q => ({
            type: 'voice',
            prompt: q.q,
            options: q.options,
            answer: q.answer,
            category: 'Active & Passive Voice'
        }));
        const pList = PJ_DATA.map(q => ({
            type: 'parajumbles',
            prompt: q.prompt,
            sentences: q.sentences,
            options: q.options,
            answer: q.answer,
            category: 'Para Jumbles'
        }));
        activeQuestions = [...vList, ...pList];
        document.getElementById('headerTitle').textContent = 'Complete English Mock Test (125 Qs)';
    }

    currentQ = 0;
    userAnswers = new Array(activeQuestions.length).fill(null);
    remainingSeconds = MAX_TIME_SECONDS;
    autoSubmittedDueToTime = false;
    isSubmitted = false;

    document.getElementById('headerTotal').textContent = activeQuestions.length;
    document.getElementById('answeredCount').textContent = '0';
    updateTimerDisplay();

    document.getElementById('startScreen').classList.add('hidden');
    document.getElementById('resultScreen').classList.add('hidden');
    document.getElementById('reviewScreen').classList.add('hidden');
    document.getElementById('quizScreen').classList.remove('hidden');

    buildPalette();
    renderQuestion();
    startTimer();
}

// ═══════════════════════════════════════════════════
// RENDER QUESTION
// ═══════════════════════════════════════════════════
function renderQuestion() {
    const q = activeQuestions[currentQ];
    const total = activeQuestions.length;

    document.getElementById('questionBadge').textContent = `Question ${currentQ + 1}`;
    
    // Topic badge
    const isPJ = q.type === 'parajumbles';
    document.getElementById('topicBadge').innerHTML = isPJ ? '🧩 Para Jumbles' : '🗣️ Active &amp; Passive Voice';

    // Prompt
    document.getElementById('questionPrompt').textContent = q.prompt;

    // Para jumbles sentences
    const pjBox = document.getElementById('pjContainer');
    if (isPJ && q.sentences && q.sentences.length > 0) {
        pjBox.innerHTML = '';
        q.sentences.forEach(s => {
            const row = document.createElement('div');
            row.className = 'pj-sentence-row';
            row.innerHTML = `
                <div class="pj-tag">${s.label}</div>
                <div class="pj-text">${s.text}</div>
            `;
            pjBox.appendChild(row);
        });
        pjBox.classList.remove('hidden');
    } else {
        pjBox.classList.add('hidden');
    }

    // Options
    const optLabels = ['A', 'B', 'C', 'D'];
    const list = document.getElementById('optionsList');
    list.innerHTML = '';

    q.options.forEach((opt, i) => {
        const div = document.createElement('div');
        div.className = 'option' + (userAnswers[currentQ] === i ? ' selected' : '');
        div.onclick = () => selectOption(i);
        div.innerHTML = `
            <div class="option-radio"></div>
            <span class="option-label">${optLabels[i]}.</span>
            <span class="option-text">${opt}</span>
        `;
        list.appendChild(div);
    });

    // Nav buttons
    document.getElementById('prevBtn').disabled = currentQ === 0;
    if (currentQ === total - 1) {
        document.getElementById('nextBtn').classList.add('hidden');
        document.getElementById('submitBtn').classList.remove('hidden');
    } else {
        document.getElementById('nextBtn').classList.remove('hidden');
        document.getElementById('submitBtn').classList.add('hidden');
    }

    updateProgress();
    updatePalette();
}

function selectOption(idx) {
    userAnswers[currentQ] = idx;
    renderQuestion();
    updateAnsweredCount();
}

function clearSelection() {
    userAnswers[currentQ] = null;
    renderQuestion();
    updateAnsweredCount();
}

function navigate(dir) {
    const total = activeQuestions.length;
    currentQ += dir;
    if (currentQ < 0) currentQ = 0;
    if (currentQ >= total) currentQ = total - 1;
    renderQuestion();
}

function updateProgress() {
    const total = activeQuestions.length;
    const pct = ((currentQ + 1) / total) * 100;
    document.getElementById('progressFill').style.width = pct + '%';
    document.getElementById('progressText').textContent = `Question ${currentQ + 1} of ${total}`;
    document.getElementById('progressPercent').textContent = Math.round(pct) + '%';
}

function updateAnsweredCount() {
    const count = userAnswers.filter(a => a !== null).length;
    document.getElementById('answeredCount').textContent = count;
}

// ═══════════════════════════════════════════════════
// PALETTE
// ═══════════════════════════════════════════════════
function buildPalette() {
    const grid = document.getElementById('paletteGrid');
    grid.innerHTML = '';
    const total = activeQuestions.length;
    for (let i = 0; i < total; i++) {
        const btn = document.createElement('button');
        btn.className = 'palette-btn';
        btn.textContent = i + 1;
        btn.onclick = () => { currentQ = i; renderQuestion(); };
        grid.appendChild(btn);
    }
}

function updatePalette() {
    const btns = document.getElementById('paletteGrid').children;
    const total = activeQuestions.length;
    for (let i = 0; i < total; i++) {
        btns[i].className = 'palette-btn';
        if (userAnswers[i] !== null) btns[i].classList.add('answered');
        if (i === currentQ) btns[i].classList.add('current');
    }
}

// ═══════════════════════════════════════════════════
// SUBMIT
// ═══════════════════════════════════════════════════
function confirmSubmit() {
    const total = activeQuestions.length;
    const answered = userAnswers.filter(a => a !== null).length;
    const unanswered = total - answered;
    document.getElementById('confirmText').textContent =
        `You have answered ${answered} out of ${total} questions.` +
        (unanswered > 0 ? ` ${unanswered} question(s) are unanswered and will be marked wrong.` : '') +
        ' Are you sure you want to submit your test?';
    document.getElementById('confirmModal').classList.add('active');
}

function closeModal() {
    document.getElementById('confirmModal').classList.remove('active');
}

function submitTest() {
    closeModal();
    stopTimer();
    isSubmitted = true;
    showResults();
}

// ═══════════════════════════════════════════════════
// RESULTS
// ═══════════════════════════════════════════════════
function showResults() {
    document.getElementById('quizScreen').classList.add('hidden');
    document.getElementById('reviewScreen').classList.add('hidden');
    document.getElementById('resultScreen').classList.remove('hidden');

    const total = activeQuestions.length;
    let correct = 0, wrong = 0, unanswered = 0;
    for (let i = 0; i < total; i++) {
        if (userAnswers[i] === null) unanswered++;
        else if (userAnswers[i] === activeQuestions[i].answer) correct++;
        else wrong++;
    }

    const pct = Math.round((correct / total) * 100);
    let grade, msg, sub;
    if (pct >= 80) {
        grade = 'excellent';
        msg = '🎉 Outstanding Performance!';
        sub = 'You have demonstrated mastery in this section. Keep up the high standards!';
    } else if (pct >= 60) {
        grade = 'good';
        msg = '👏 Solid Effort!';
        sub = 'Good grasp of the concepts! Review mistakes to aim for 90%+.';
    } else if (pct >= 40) {
        grade = 'average';
        msg = '📖 Keep Practicing!';
        sub = 'A good foundation, but regular revision of rules and patterns will boost your accuracy.';
    } else {
        grade = 'poor';
        msg = '💪 Keep Pushing!';
        sub = 'Review the detailed answers below and re-attempt to solidify your concepts.';
    }

    const autoSubmitBanner = autoSubmittedDueToTime
        ? `<div style="background:#fee2e2; border:1px solid #f87171; color:#991b1b; padding:12px 18px; border-radius:10px; margin-bottom:24px; font-weight:700; display:inline-flex; align-items:center; gap:8px;">
            ⏰ Time's Up! The 45-minute limit was reached and your test was automatically submitted.
           </div>`
        : '';

    document.getElementById('resultContent').innerHTML = `
        ${autoSubmitBanner}
        <div class="score-circle ${grade}">
            <div class="score-value">${correct}</div>
            <div class="score-total">out of ${total}</div>
            <div class="score-percent">${pct}%</div>
        </div>
        <div class="result-message">${msg}</div>
        <p class="result-sub">${sub}</p>
        <p style="color:var(--text-secondary); font-size:14px; margin-bottom:24px;">⏱ Time used: <strong>${getTimeUsedString()}</strong> (out of 45m 00s limit)</p>
        <div class="result-stats">
            <div class="stat-card correct"><div class="stat-num">${correct}</div><div class="stat-label">Correct</div></div>
            <div class="stat-card wrong"><div class="stat-num">${wrong}</div><div class="stat-label">Wrong</div></div>
            <div class="stat-card unanswered"><div class="stat-num">${unanswered}</div><div class="stat-label">Unanswered</div></div>
        </div>
        <div class="result-actions">
            <button class="btn btn-primary" onclick="startReview()">📋 Review All Answers</button>
            <button class="btn btn-secondary" onclick="startTest()">🔄 Retake This Test</button>
            <button class="btn btn-secondary" onclick="backToStart()">🔀 Switch Test Topic</button>
        </div>
    `;
}

function backToStart() {
    stopTimer();
    remainingSeconds = MAX_TIME_SECONDS;
    updateTimerDisplay();
    document.getElementById('resultScreen').classList.add('hidden');
    document.getElementById('reviewScreen').classList.add('hidden');
    document.getElementById('quizScreen').classList.add('hidden');
    document.getElementById('startScreen').classList.remove('hidden');
    document.getElementById('headerTitle').textContent = 'SSC English PYQ Practice';
}

// ═══════════════════════════════════════════════════
// REVIEW
// ═══════════════════════════════════════════════════
function startReview() {
    document.getElementById('resultScreen').classList.add('hidden');
    document.getElementById('reviewScreen').classList.remove('hidden');
    document.getElementById('filterSelect').value = 'all';
    applyFilter();
}

function applyFilter() {
    const filter = document.getElementById('filterSelect').value;
    const total = activeQuestions.length;
    filteredIndices = [];
    for (let i = 0; i < total; i++) {
        const isCorrect = userAnswers[i] === activeQuestions[i].answer;
        const isUnanswered = userAnswers[i] === null;
        if (filter === 'all') filteredIndices.push(i);
        else if (filter === 'wrong' && !isUnanswered && !isCorrect) filteredIndices.push(i);
        else if (filter === 'correct' && isCorrect) filteredIndices.push(i);
        else if (filter === 'unanswered' && isUnanswered) filteredIndices.push(i);
    }
    reviewIndex = 0;
    buildReviewPalette();
    if (filteredIndices.length > 0) {
        renderReview();
    } else {
        document.getElementById('reviewQuestionCard').innerHTML = '<p style="text-align:center;color:var(--text-secondary);padding:40px;">No questions match this filter.</p>';
        document.getElementById('reviewPrevBtn').disabled = true;
        document.getElementById('reviewNextBtn').disabled = true;
    }
}

function buildReviewPalette() {
    const grid = document.getElementById('reviewPaletteGrid');
    grid.innerHTML = '';
    const total = activeQuestions.length;
    for (let i = 0; i < total; i++) {
        const btn = document.createElement('button');
        btn.className = 'palette-btn';
        const isCorrect = userAnswers[i] === activeQuestions[i].answer;
        const isUnanswered = userAnswers[i] === null;
        if (isUnanswered) {
            btn.style.background = '#fef3c7';
            btn.style.borderColor = '#d97706';
            btn.style.color = '#d97706';
        } else if (isCorrect) {
            btn.classList.add('review-correct');
        } else {
            btn.classList.add('review-wrong');
        }
        btn.textContent = i + 1;
        btn.onclick = () => {
            const idx = filteredIndices.indexOf(i);
            if (idx !== -1) {
                reviewIndex = idx;
                renderReview();
            }
        };
        grid.appendChild(btn);
    }
}

function renderReview() {
    if (filteredIndices.length === 0) return;
    const qi = filteredIndices[reviewIndex];
    const q = activeQuestions[qi];
    const userAns = userAnswers[qi];
    const correctAns = q.answer;
    const isPJ = q.type === 'parajumbles';

    document.getElementById('reviewBadge').textContent = `Question ${qi + 1}`;
    document.getElementById('reviewTopicBadge').innerHTML = isPJ ? '🧩 Para Jumbles' : '🗣️ Active &amp; Passive Voice';

    // Status
    const status = document.getElementById('reviewStatus');
    if (userAns === null) {
        status.innerHTML = '<span style="color:#d97706; background:#fef3c7; padding:4px 10px; border-radius:6px;">⚠️ Unanswered — Correct option was ' + String.fromCharCode(65 + correctAns) + '</span>';
    } else if (userAns === correctAns) {
        status.innerHTML = '<span style="color:#059669; background:#d1fae5; padding:4px 10px; border-radius:6px;">✅ Correct — You selected ' + String.fromCharCode(65 + userAns) + '</span>';
    } else {
        status.innerHTML = '<span style="color:#dc2626; background:#fee2e2; padding:4px 10px; border-radius:6px;">❌ Incorrect — Your answer: ' + String.fromCharCode(65 + userAns) + ' | Correct answer: ' + String.fromCharCode(65 + correctAns) + '</span>';
    }

    document.getElementById('reviewQuestionPrompt').textContent = q.prompt;

    // Para jumbles sentences
    const pjBox = document.getElementById('reviewPjContainer');
    if (isPJ && q.sentences && q.sentences.length > 0) {
        pjBox.innerHTML = '';
        q.sentences.forEach(s => {
            const row = document.createElement('div');
            row.className = 'pj-sentence-row';
            row.innerHTML = `
                <div class="pj-tag">${s.label}</div>
                <div class="pj-text">${s.text}</div>
            `;
            pjBox.appendChild(row);
        });
        pjBox.classList.remove('hidden');
    } else {
        pjBox.classList.add('hidden');
    }

    // Options
    const optLabels = ['A', 'B', 'C', 'D'];
    const list = document.getElementById('reviewOptionsList');
    list.innerHTML = '';

    q.options.forEach((opt, i) => {
        const div = document.createElement('div');
        let cls = 'option';
        if (i === correctAns) cls += ' correct-answer';
        else if (i === userAns && i !== correctAns) cls += ' wrong-answer';
        div.className = cls;
        div.style.cursor = 'default';
        div.innerHTML = `
            <div class="option-radio"></div>
            <span class="option-label">${optLabels[i]}.</span>
            <span class="option-text">${opt}</span>
        `;
        list.appendChild(div);
    });

    // Nav
    document.getElementById('reviewPrevBtn').disabled = reviewIndex === 0;
    document.getElementById('reviewNextBtn').disabled = reviewIndex === filteredIndices.length - 1;

    // Progress
    const pct = ((reviewIndex + 1) / filteredIndices.length) * 100;
    document.getElementById('reviewProgressFill').style.width = pct + '%';
    document.getElementById('reviewProgressText').textContent = `Reviewing ${reviewIndex + 1} of ${filteredIndices.length}`;

    // Highlight current in palette
    const btns = document.getElementById('reviewPaletteGrid').children;
    for (let i = 0; i < activeQuestions.length; i++) {
        btns[i].classList.remove('current');
    }
    if (btns[qi]) btns[qi].classList.add('current');
}

function reviewNavigate(dir) {
    reviewIndex += dir;
    if (reviewIndex < 0) reviewIndex = 0;
    if (reviewIndex >= filteredIndices.length) reviewIndex = filteredIndices.length - 1;
    renderReview();
}
</script>

</body>
</html>
"""

# Replace placeholders
final_html = html_template.replace('__VOICE_DATA__', voice_json_str)
final_html = final_html.replace('__PJ_DATA__', pj_json_str)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Generated public/index.html with 45-minute countdown and auto-submission successfully! Length:", len(final_html))
