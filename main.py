from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>BelPASS.edu - История Влада</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
       
        :root {
            --primary: #3b82f6;
            --danger: #f43f5e;
            --success: #10b981;
            --viber: #7360f2;
            --tg-bg: #17212b;
            --warning: #facc15;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
        body { height: 100vh; width: 100vw; background: #020617; overflow: hidden; color: #f8fafc; }

        #story-overlay {
            position: fixed; inset: 0; background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
            z-index: 5000; display: flex; align-items: center; justify-content: center; padding: 40px;
        }
        .story-container {
            display: flex; align-items: flex-end; max-width: 1100px; width: 100%; gap: 40px;
        }
        .vlad-char {
            width: 220px; height: 440px; flex-shrink: 0;
            background-size: contain; background-repeat: no-repeat; background-position: bottom;
            transition: background-image 0.3s ease;
        }
        .story-box { flex: 1; background: rgba(255,255,255,0.05); padding: 40px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px); }
        .story-text { font-size: 28px; line-height: 1.4; color: #f8fafc; margin-bottom: 30px; min-height: 120px; font-weight: 300; }
        .story-sub { font-size: 16px; color: var(--primary); text-transform: uppercase; letter-spacing: 4px; margin-bottom: 10px; font-weight: 800; }

        /* Эффект мигающего курсора */
        .typing-cursor {
            display: inline-block;
            width: 3px;
            height: 32px;
            background-color: var(--primary);
            margin-left: 4px;
            vertical-align: middle;
            animation: blink 1s step-end infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }

        .desktop {
            background: linear-gradient(rgba(2, 6, 23, 0.7), rgba(2, 6, 23, 0.7)),
                        url('https://i.redd.it/pb5d9d1uif1d1.jpeg') center/cover;
            height: calc(100vh - 65px); position: relative; padding: 40px;
        }

        .icons-grid {
            display: grid; grid-template-columns: repeat(auto-fill, 130px);
            grid-template-rows: repeat(auto-fill, 130px); gap: 25px; height: 100%; align-content: start;
        }
        .icon { width: 120px; text-align: center; cursor: pointer; padding: 12px; border-radius: 16px; transition: 0.2s; }
        .icon:hover { background: rgba(255,255,255,0.1); backdrop-filter: blur(8px); transform: scale(1.05); }
        
        .icon-img { 
            width: 80px; height: 80px; border-radius: 18px; margin: 0 auto 10px; 
            display: flex; align-items: center; justify-content: center; overflow: hidden;
            background: rgba(255,255,255,0.05); box-shadow: 0 6px 20px rgba(0,0,0,0.5); font-size: 40px;
        }
        .icon-png { width: 100%; height: 100%; object-fit: cover; }
        .icon-label { font-size: 13px; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,1); }

        .window {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 900px; height: 650px; background: #0f172a; border: 1px solid rgba(255,255,255,0.15);
            border-radius: 20px; display: none; flex-direction: column; z-index: 500; overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }
        .win-header { padding: 15px 25px; background: rgba(255,255,255,0.07); display: flex; justify-content: space-between; align-items: center; font-weight: bold; }
        .win-body { flex: 1; display: flex; overflow: hidden; }
        .close-btn { background: #f43f5e; border: none; color: white; cursor: pointer; width: 24px; height: 24px; border-radius: 50%; font-size: 14px; }

        .btn-action { padding: 12px 24px; background: var(--primary); color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: 700; font-size: 16px; transition: 0.2s; }
        .btn-action:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4); }
        
        .taskbar { height: 65px; background: rgba(15, 23, 42, 0.98); display: flex; align-items: center; padding: 0 30px; border-top: 1px solid rgba(255,255,255,0.1); }
        .xp-bar { width: 300px; height: 14px; background: #334155; border-radius: 7px; margin: 0 20px; overflow: hidden; }
        .xp-fill { height: 100%; background: linear-gradient(90deg, var(--primary), var(--success)); width: 50%; transition: 0.5s; }

        .overlay { display: none; position: fixed; inset: 0; background: rgba(2, 6, 23, 0.98); z-index: 2000; justify-content: center; align-items: center; }
        .modal-card { background: #1e293b; width: 700px; border-radius: 24px; padding: 40px; border: 1px solid var(--primary); }
        
        .mvd-img { width: 187px; height: 221px; object-fit: contain; flex-shrink: 0; }

        /* Стили для чатов */
        .chat-list { overflow-y: auto; }
        .chat-item { 
            padding: 15px 20px; border-bottom: 1px solid rgba(255,255,255,0.1); 
            cursor: pointer; transition: 0.2s; display: flex; align-items: center; gap: 12px;
        }
        .chat-item:hover { background: rgba(255,255,255,0.05); }
        .chat-item.active { background: var(--primary); }
        .chat-avatar { width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; }
        .chat-info { flex: 1; }
        .chat-name { font-weight: 600; margin-bottom: 4px; }
        .chat-last { font-size: 12px; opacity: 0.7; }
        .chat-time { font-size: 11px; opacity: 0.5; }

        /* Instagram лента */
        .insta-feed { overflow-y: auto; padding: 20px; }
        .insta-post { 
            background: white; border-radius: 12px; margin-bottom: 20px; 
            border: 1px solid #dbdbdb; color: #262626;
        }
        .post-header { padding: 14px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid #efefef; }
        .post-avatar { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(45deg, #f09433, #bc1888); }
        .post-user { font-weight: 600; }
        .post-image { height: 300px; background: #fafafa; display: flex; align-items: center; justify-content: center; font-size: 48px; }
        .post-actions { padding: 10px 14px; display: flex; gap: 16px; font-size: 24px; }
        .post-likes { padding: 0 14px 8px; font-weight: 600; font-size: 14px; }
        .post-caption { padding: 0 14px 14px; font-size: 14px; }
        .post-caption strong { margin-right: 6px; }
    </style>
</head>
<body>

    <div id="story-overlay">
        <div class="story-container">
            <div id="vlad-img" class="vlad-char" style="background-image: url('/static/beg.png');"></div>
            <div class="story-box">
                <div id="story-sub" class="story-sub">Загрузка...</div>
                <div id="story-text" class="story-text"></div>
                <button id="story-btn" class="btn-action">ВПЕРЕД!</button>
            </div>
        </div>
    </div>

    <div class="desktop">
        <div class="icons-grid">
            <div class="icon" data-win="phone-win"><div class="icon-img" style="background:#2ecc71">📞</div><div class="icon-label">Телефон</div></div>
            <div class="icon"><div class="icon-img" style="background:#4a90e2">📖</div><div class="icon-label">Эл. Дневник</div></div>
            <div class="icon" data-win="tg-win"><div class="icon-img"><img src="/static/telegram.png" class="icon-png" onerror="this.parentElement.innerHTML='💬';"></div><div class="icon-label">Telegram</div></div>
            <div class="icon"><div class="icon-img" style="background:#ffcc00">🗑️</div><div class="icon-label">Корзина</div></div>
            <div class="icon" data-win="viber-win"><div class="icon-img"><img src="/static/viber.png" class="icon-png" onerror="this.parentElement.innerHTML='💜';"></div><div class="icon-label">Viber</div></div>
            <div class="icon"><div class="icon-img" style="background:#34495e">🎮</div><div class="icon-label">Игры</div></div>
            <div class="icon" data-win="bank-win"><div class="icon-img"><img src="/static/bank.png" class="icon-png" onerror="this.parentElement.innerHTML='💳';"></div><div class="icon-label">Беларусбанк</div></div>
            <div class="icon"><div class="icon-img" style="background:#9b59b6">📁</div><div class="icon-label">Книги</div></div>
            <div class="icon" data-win="insta-win"><div class="icon-img"><img src="/static/instagram.png" class="icon-png" onerror="this.parentElement.innerHTML='📷';"></div><div class="icon-label">Instagram</div></div>
            <div class="icon" data-win="kufar-win"><div class="icon-img"><img src="/static/kufar.png" class="icon-png" onerror="this.parentElement.innerHTML='🛒';"></div><div class="icon-label">Kufar</div></div>
            <div class="icon"><div class="icon-img" style="background:#9b59b6">📁</div><div class="icon-label">Рефераты</div></div>
        </div>

        <!-- TELEGRAM -->
        <div id="tg-win" class="window">
            <div class="win-header"><span>Telegram</span><button class="close-btn">✕</button></div>
            <div class="win-body">
                <div style="width:300px; background: var(--tg-bg);" id="tg-side" class="chat-list"></div>
                <div style="flex:1; background: #0e1619; padding:25px; overflow-y: auto;" id="tg-chat"></div>
            </div>
        </div>

        <!-- VIBER -->
        <div id="viber-win" class="window">
            <div class="win-header" style="background:var(--viber)"><span>Viber</span><button class="close-btn">✕</button></div>
            <div class="win-body">
                <div style="width:300px; background:#f8f9fa; color:#333;" id="viber-side" class="chat-list"></div>
                <div style="flex:1; background:#e5ddd5; padding:25px; overflow-y: auto;" id="viber-chat"></div>
            </div>
        </div>

        <!-- INSTAGRAM как лента -->
        <div id="insta-win" class="window">
            <div class="win-header" style="background:linear-gradient(45deg, #f09433, #bc1888)"><span>Instagram</span><button class="close-btn">✕</button></div>
            <div class="win-body" style="background: #fafafa;">
                <div id="insta-feed" class="insta-feed" style="flex:1;"></div>
            </div>
        </div>

        <!-- KUFAR -->
        <div id="kufar-win" class="window">
            <div class="win-header" style="background:#ff6b00"><span>Kufar</span><button class="close-btn">✕</button></div>
            <div class="win-body">
                <div style="width:300px; background:#fff5e6; color:#333;" id="kufar-side" class="chat-list"></div>
                <div style="flex:1; background:#f9f9f9; padding:25px; overflow-y: auto;" id="kufar-chat"></div>
            </div>
        </div>

        <!-- PHONE -->
        <div id="phone-win" class="window" style="width:400px; height:450px;">
            <div class="win-header"><span>Телефон</span><button class="close-btn">✕</button></div>
            <div class="win-body" style="display: flex; flex-direction: column; padding: 30px; gap: 20px;">
                <button class="btn-action" data-action="call_parents">📞 МАМА</button>
                <button class="btn-action" data-action="call_102">📞 102 (Милиция)</button>
                <button class="btn-action" data-action="call_teacher">📞 Кл. руководитель</button>
            </div>
        </div>

        <!-- BANK -->
        <div id="bank-win" class="window" style="width:450px; height:500px;">
            <div class="win-header" style="background:#007d35"><span>Беларусбанк</span><button class="close-btn">✕</button></div>
            <div class="win-body" style="flex-direction:column; padding:30px; background:#f0f2f5; color:#333;">
                <div style="background:#007d35; color:white; padding:25px; border-radius:15px;">
                    <p style="font-size:14px; opacity:0.9;">Карта учащегося (Влад)</p>
                    <h1 id="bank-val" style="margin-top:10px;">2050.12 BYN</h1>
                </div>
                <div id="bank-ops" style="margin-top:30px;"></div>
            </div>
        </div>
    </div>

    <div id="major-overlay" class="overlay">
        <div class="modal-card">
            <div style="display: flex; align-items: center; gap: 30px; margin-bottom: 20px;">
                <img src="/static/MVD.png" class="mvd-img" alt="МВД" onerror="this.src='https://img.icons8.com/color/187/police-officer.png';">
                <div>
                    <h2 id="major-title" style="font-size: 28px;"></h2>
                    <p style="color: var(--primary); font-size: 14px; font-weight: bold;">ПОДПОЛКОВНИК МИЛИЦИИ • УПРАВЛЕНИЕ «К»</p>
                </div>
            </div>
            <p id="major-desc" style="margin:25px 0; font-size: 18px; line-height: 1.5;"></p>
            <div id="major-law" style="padding:20px; background:rgba(0,0,0,0.3); font-size:15px; color:var(--warning); margin-bottom:25px; border-radius:12px; border-left: 4px solid var(--warning);"></div>
            <button class="btn-action" id="quiz-btn" style="width:100%">Пройти проверку знаний</button>
        </div>
    </div>

    <div id="quiz-overlay" class="overlay">
        <div class="modal-card" style="width:500px;"><h3 id="quiz-q" style="font-size:22px; margin-bottom:25px;"></h3><div id="quiz-opts"></div></div>
    </div>

    <div class="taskbar">
        <strong style="font-size: 16px; color: #facc15;">Требуется срочно позвонить по телефону!</strong>
        <div class="xp-bar"><div id="xp-fill" class="xp-fill"></div></div>
        <span id="clock" style="font-size: 20px; font-weight: bold; margin-left: auto;">00:00</span>
    </div>

    <script>
        let currentLvl = 1; let storyIndex = 0; let xp = 50; let balance = 150.00;
        let activeChat = { tg: null, viber: null, kufar: null };
        let isTyping = false;  // Флаг для блокировки кликов во время печати
        let currentTypingTimeout = null;

        const vladEmotions = {
            start: '/static/beg.png',
            normal: '/static/normal.png',
            scared: '/static/strah.png',
            happy: '/static/radost.png'
        };

        const allStories = {
            1: { sub: "Глава 1: Опасная шутка", lines: ["Я Влад, только что пришел со школы.", "В чате класса какой-то треш! Кто-то пишет, что в школе заложена бомба...", "Все смеются, а мне что-то страшно. Вдруг это не шутка?"], btn: "РАЗОБРАТЬСЯ", emotion: 'scared' },
            2: { sub: "Глава 2: Легкие деньги?", lines: ["Фух, с тем чатом разобрались.", "Но теперь мне в личку в Телеге пишет какой-то чел.", "Предлагает 100 рублей за репост видео. Это же целых пять обедов!"], btn: "ОТКРЫТЬ ТЕЛЕГРАМ", emotion: 'normal' },
            3: { sub: "Глава 3: Странный звонок", lines: ["Мама всегда говорила не брать трубку от незнакомых.", "Но тут звонок в Viber, и на аватарке логотип моего банка!", "Говорят, мою карту взломали. Надо что-то делать!"], btn: "ОТВЕТИТЬ В VIBER", emotion: 'scared' },
            4: { sub: "Глава 4: Продажа на Куфаре", lines: ["Решил продать свои старые кроссовки, чтобы накопить на новый велик.", "Покупатель нашелся быстро! Пишет, что всё оплатил и кидает ссылку.", "Говорит, там мои деньги. Переходить?"], btn: "ЗАЙТИ НА КУФАР", emotion: 'normal' },
            5: { sub: "Глава 5: Внезапное богатство", lines: ["Ого! Зашел в банкинг, а там +2000 рублей!", "И тут же сообщение: 'Брат, ошибся цифрой, верни пожалуйста хотя бы 1800, а 200 оставь себе'.", "Выглядит как удача, или нет?"], btn: "ПОСМОТРЕТЬ КАРТУ", emotion: 'normal' },
            6: { sub: "Глава 6: Пост в Инсте", lines: ["Листаю ленту Instagram...", "Вижу, что создали аккаунт-хейт против Кати из параллельного класса.", "Меня отметили и просят поставить лайк. Все же ставят..."], btn: "ОТКРЫТЬ ИНСТУ", emotion: 'scared' }
        };

        // Функция для постепенного вывода текста
        function typeText(element, text, speed = 50, callback) {
            // Отменяем предыдущую анимацию, если она была
            if (currentTypingTimeout) {
                clearTimeout(currentTypingTimeout);
            }
            
            isTyping = true;
            element.innerHTML = '';
            let i = 0;
            
            // Добавляем курсор
            const cursorSpan = document.createElement('span');
            cursorSpan.className = 'typing-cursor';
            
            function typeNextChar() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    currentTypingTimeout = setTimeout(typeNextChar, speed);
                } else {
                    // Убираем курсор после завершения
                    const cursor = element.querySelector('.typing-cursor');
                    if (cursor) cursor.remove();
                    isTyping = false;
                    if (callback) callback();
                }
            }
            
            element.appendChild(cursorSpan);
            typeNextChar();
        }

        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('story-btn').addEventListener('click', handleStoryNext);
            document.getElementById('quiz-btn').addEventListener('click', showQuiz);
            document.querySelectorAll('.icon[data-win]').forEach(icon => icon.onclick = () => openWin(icon.dataset.win));
            document.querySelectorAll('.close-btn').forEach(btn => btn.onclick = () => btn.closest('.window').style.display = 'none');
            document.querySelectorAll('[data-action]').forEach(btn => btn.onclick = () => processAction(btn.dataset.action));
            updateUI();
            setInterval(() => {
                const now = new Date();
                document.getElementById('clock').innerText = now.toLocaleTimeString('ru-RU', {hour: '2-digit', minute:'2-digit'});
            }, 1000);
            setVladEmotion('start');
            handleStoryNext();
        });

        function setVladEmotion(type) {
            document.getElementById('vlad-img').style.backgroundImage = `url('${vladEmotions[type]}')`;
        }

        function handleStoryNext() {
            // Если текст еще печатается, не даем нажать кнопку
            if (isTyping) return;
            
            const currentData = allStories[currentLvl];
            const storyTextElement = document.getElementById('story-text');
            const storyBtn = document.getElementById('story-btn');
            const storySubElement = document.getElementById('story-sub');
            
            if (storyIndex < currentData.lines.length) {
                // Показываем подзаголовок
                storySubElement.innerText = currentData.sub;
                setVladEmotion(currentData.emotion || 'normal');
                
                // Печатаем текущую строку
                typeText(storyTextElement, currentData.lines[storyIndex], 40, () => {
                    storyIndex++;
                    // Если это последняя строка главы - меняем кнопку
                    if (storyIndex === currentData.lines.length) {
                        storyBtn.innerText = currentData.btn;
                        storyBtn.style.background = "var(--danger)";
                    } else {
                        storyBtn.innerText = "ДАЛЕЕ";
                        storyBtn.style.background = "var(--primary)";
                    }
                });
            } else {
                document.getElementById('story-overlay').style.display = 'none';
                setupLevel();
            }
        }

        function setupLevel() {
            const hints = {
                1: "Требуется срочно позвонить по телефону!",
                2: "Проверь, кто пишет в Telegram!",
                3: "Требуется срочно проверить Viber!",
                4: "Проверь, кто пишет в Kufar!",
                5: "Требуется срочно проверить банкинг!",
                6: "Проверь ленту в Instagram!"
            };
            document.querySelector('.taskbar strong').innerText = hints[currentLvl] || "⚠️ ПРИМЕР: Требуется срочно позвонить по телефону!";
            
            renderTg(); renderViber(); renderInsta(); renderKufar();
            const storyBtn = document.getElementById('story-btn');
            storyBtn.style.background = "var(--primary)";
            storyBtn.innerText = "ДАЛЕЕ";
        }

        function processAction(type) {
            let isWin = (type === 'ok' || (currentLvl === 1 && type === 'call_102'));
            const laws = {
                1: "Ст. 340 УК РБ: Ложное сообщение об опасности. До 7 лет лишения свободы.",
                2: "Ст. 19.11 КоАП РБ: Распространение экстремистских материалов.",
                3: "Ст. 212 УК РБ: Вишинг. Банки никогда не звонят в мессенджерах.",
                4: "Ст. 212 УК РБ: Фишинг. Настоящий сайт только kufar.by.",
                5: "Ст. 222 УК РБ: Соучастие в отмывании денег (Дропперство).",
                6: "Ст. 188 УК РБ: Клевета и оскорбление в интернете."
            };
            if (isWin) setVladEmotion('happy'); else setVladEmotion('scared');
            document.getElementById('major-title').innerText = isWin ? "МОЛОДЕЦ, ВЛАД!" : "ВНИМАНИЕ, ОШИБКА!";
            document.getElementById('major-desc').innerText = isWin ? "Ты принял верное решение и защитил себя." : "Ты совершил опасную ошибку. Посмотри, что говорит закон:";
            document.getElementById('major-law').innerHTML = laws[currentLvl];
            document.getElementById('major-overlay').style.display = 'flex';
            xp += isWin ? 20 : -30;
            updateUI();
            document.querySelectorAll('.window').forEach(w => w.style.display = 'none');
        }

        function showQuiz() {
            document.getElementById('major-overlay').style.display = 'none';
            const quizzes = {
                1: { q: "Влад увидел угрозу в чате. Его действия?", o: ["Пошутить", "Позвонить 102", "Переслать другу"], c: 1 },
                2: { q: "Владу предлагают деньги за репост. Это безопасно?", o: ["Да", "Нет, это вербовка", "Если много платят - да"], c: 1 },
                3: { q: "Владу звонят в Viber из банка. Верим?", o: ["Да", "Никогда", "Только если аватарка ок"], c: 1 },
                4: { q: "Владу прислали ссылку kufar-pay.pro. Переходим?", o: ["Да", "Нет, это фишинг", "Только с компа"], c: 1 },
                5: { q: "Владу пришли чужие 2000р. Что делать?", o: ["Оставить себе", "Вернуть в банк", "Перевести"], c: 1 },
                6: { q: "Влада просят лайкнуть пост-травлю. Это ок?", o: ["Да", "Нет, это кибербуллинг", "Если анонимно"], c: 1 }
            };
            const q = quizzes[currentLvl];
            document.getElementById('quiz-q').innerText = q.q;
            const opts = document.getElementById('quiz-opts');
            opts.innerHTML = "";
            q.o.forEach((opt, i) => {
                const b = document.createElement('button');
                b.className = "btn-action"; b.style.width = "100%"; b.style.marginBottom = "12px"; b.innerText = opt;
                b.onclick = () => {
                    alert(i === q.c ? "✅ Правильно!" : "❌ Ошибка!");
                    document.getElementById('quiz-overlay').style.display = 'none';
                    if(++currentLvl > 6) { alert("ПОЗДРАВЛЯЕМ! ВЛАД В БЕЗОПАСНОСТИ!"); location.reload(); }
                    else { storyIndex = 0; document.getElementById('story-overlay').style.display = 'flex'; handleStoryNext(); }
                };
                opts.appendChild(b);
            });
            document.getElementById('quiz-overlay').style.display = 'flex';
        }

        function updateUI() {
            document.getElementById('xp-fill').style.width = Math.max(0, Math.min(100, xp)) + "%";
            document.getElementById('bank-val').innerText = balance.toFixed(2) + " BYN";
        }

        function openWin(id) {
            document.getElementById(id).style.display = 'flex';
            if(id === 'bank-win' && currentLvl === 5) {
                document.getElementById('bank-ops').innerHTML = `
                    <div style="background:#fff; padding:15px; border-radius:10px; border:1px solid #c0392b">
                        <p style="color:#c0392b; font-weight:bold; margin-bottom:10px;">ВХОДЯЩИЙ ПЕРЕВОД: +2000.00 BYN</p>
                        <p style="font-size:14px; color:#555">Брат, ошибся цифрой, верни пожалуйста хотя бы 1800, а 200 оставь себе!</p>
                    </div>
                    <button class="btn-action" style="width:100%; margin-top:20px; margin-bottom:10px;" onclick="processAction('bad')">ПЕРЕВЕСТИ</button>
                    <button class="btn-action" style="background:var(--success); width:100%;" onclick="processAction('ok')">🚨 В БАНК</button>`;
            }
        }

        function renderTg() {
            const side = document.getElementById('tg-side');
            const chat = document.getElementById('tg-chat');
            
            let chats = [
                { id: 'class', name: '📚 10 "А" класс', last: 'Андрей: Кто пойдет завтра в кино?', time: '14:23', avatar: '📚' },
                { id: 'mom', name: '👩 Мама', last: 'Влад, купи хлеб по дороге', time: '09:15', avatar: '👩' },
                { id: 'friend', name: '👤 Дима (друг)', last: 'Го в доту вечером?', time: 'Вчера', avatar: '👤' }
            ];
            
            if (currentLvl === 2) {
                chats.push({ id: 'stranger', name: '📢 Скрытый номер', last: 'Привет! Есть предложение...', time: '10:30', avatar: '❓' });
            }
            
            side.innerHTML = chats.map(c => `
                <div class="chat-item" data-chat-id="${c.id}" onclick="selectTgChat('${c.id}')">
                    <div class="chat-avatar">${c.avatar}</div>
                    <div class="chat-info">
                        <div class="chat-name">${c.name}</div>
                        <div class="chat-last">${c.last}</div>
                    </div>
                    <div class="chat-time">${c.time}</div>
                </div>
            `).join('');
            
            chat.innerHTML = '<div style="color: #6c7883; text-align: center; margin-top: 200px;">Выберите чат</div>';
        }

        function selectTgChat(chatId) {
            const chat = document.getElementById('tg-chat');
            document.querySelectorAll('#tg-side .chat-item').forEach(el => el.classList.remove('active'));
            document.querySelector(`[data-chat-id="${chatId}"]`).classList.add('active');
            
            if (chatId === 'stranger' && currentLvl === 2) {
                chat.innerHTML = `
                    <div style="display: flex; flex-direction: column; height: 100%;">
                        <div style="flex: 1;">
                            <div style="background: #182533; padding: 15px; border-radius: 12px; margin-bottom: 10px; max-width: 80%;">
                                <img src="/static/video.png" style="width: 100%; border-radius: 8px; margin-bottom: 10px;" alt="Video thumbnail">
                                Влад, привет! Раскидай это видео по чатам, плачу 100р сразу.
                            </div>
                        </div>
                        <div style="display: flex; gap: 10px; margin-top: 20px;">
                            <button class="btn-action" style="flex: 1;" onclick="processAction('bad')">📤 ОТПРАВИТЬ</button>
                            <button class="btn-action" style="flex: 1; background:var(--success);" onclick="processAction('ok')">🚨 В МИЛИЦИЮ</button>
                        </div>
                    </div>
                `;
            } else {
                chat.innerHTML = `
                    <div style="color: #6c7883; text-align: center; margin-top: 200px;">
                        💬 Обычный чат. Ничего подозрительного.
                    </div>
                `;
            }
        }

        function renderViber() {
            const side = document.getElementById('viber-side');
            const chat = document.getElementById('viber-chat');
            
            let chats = [
                { id: 'mom_v', name: '👩 Мама', last: 'Позвони когда освободишься', time: '11:20', avatar: '👩' },
                { id: 'granny', name: '👵 Бабушка', last: 'Внучек, приезжай на блины', time: 'Вчера', avatar: '👵' },
                { id: 'masha', name: '👧 Маша (одноклассница)', last: 'Скинь дз по алгебре плиз', time: 'Пн', avatar: '👧' }
            ];
            
            if (currentLvl === 3) {
                chats.push({ id: 'bank_fake', name: '🏦 Беларусбанк', last: '⚠️ СРОЧНО! Подтвердите данные', time: '09:45', avatar: '🏦' });
            }
            
            side.innerHTML = chats.map(c => `
                <div class="chat-item" data-chat-id="${c.id}" onclick="selectViberChat('${c.id}')" style="border-bottom: 1px solid #ddd;">
                    <div class="chat-avatar" style="background: #e0e0e0;">${c.avatar}</div>
                    <div class="chat-info">
                        <div class="chat-name">${c.name}</div>
                        <div class="chat-last" style="color: #666;">${c.last}</div>
                    </div>
                    <div class="chat-time" style="color: #999;">${c.time}</div>
                </div>
            `).join('');
            
            chat.innerHTML = '<div style="color: #999; text-align: center; margin-top: 200px;">Выберите чат</div>';
        }

        function selectViberChat(chatId) {
            const chat = document.getElementById('viber-chat');
            document.querySelectorAll('#viber-side .chat-item').forEach(el => el.classList.remove('active'));
            document.querySelector(`[data-chat-id="${chatId}"]`).classList.add('active');
            
            if (chatId === 'bank_fake' && currentLvl === 3) {
                chat.innerHTML = `
                    <div style="display: flex; flex-direction: column; height: 100%;">
                        <div style="flex: 1;">
                            <div style="background: black; padding: 15px; border-radius: 12px; max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                                Влад, это служба безопасности банка! Вашу карту пытаются взломать. Чтобы заблокировать операцию, срочно назовите код из SMS!
                            </div>
                        </div>
                        <div style="display: flex; gap: 10px; margin-top: 20px;">
                            <button class="btn-action" style="flex: 1; background: #f43f5e;" onclick="processAction('bad')">📱 СКАЗАТЬ КОД</button>
                            <button class="btn-action" style="flex: 1; background: #10b981;" onclick="processAction('ok')">📞 СБРОСИТЬ</button>
                        </div>
                    </div>
                `;
            } else {
                chat.innerHTML = `
                    <div style="color: #999; text-align: center; margin-top: 200px;">
                        💬 Обычный чат с родными и друзьями.
                    </div>
                `;
            }
        }

        function renderInsta() {
            const feed = document.getElementById('insta-feed');
            
            let posts = [
                { user: 'masha_minsk', avatar: '👤', image: '<img src="static/post1.png" alt="bulling" style="width:100%; max-width:210px; height:auto; object-fit:cover; border-radius:12px;">', likes: '124', caption: 'Прогулка по парку!' },
                { user: 'dima_04', avatar: '👤', image: '<img src="static/post2.png" alt="bulling" style="width:100%; max-width:210px; height:auto; object-fit:cover; border-radius:12px;">', likes: '89', caption: 'Провожу свое время с пользой!' },
                { user: 'lyceum_1_mogilev', avatar: '🏫', image: '<img src="static/post3.png" alt="bulling" style="width:100%; max-width:210px; height:auto; object-fit:cover; border-radius:12px;">', likes: '56', caption: 'Немного фото нашего любимого лицея!' }
            ];
            
            if (currentLvl === 6) {
                posts.splice(1, 0, {
                    user: 'anonim_minsk',
                    avatar: '👁️',
                    image: '<img src="static/bulling.png" alt="bulling" style="width:100%; max-width:210px; height:auto; object-fit:cover; border-radius:12px;">',
                    likes: '5',
                    caption: 'Смотрите какая Катя из 10Б! Позор! Лайк если согласен'
                });
            }
            
            feed.innerHTML = posts.map(post => `
                <div class="insta-post">
                    <div class="post-header">
                        <div class="post-avatar" style="background: linear-gradient(45deg, #f09433, #bc1888); display: flex; align-items: center; justify-content: center; color: white; font-size: 18px;">${post.avatar}</div>
                        <span class="post-user">${post.user}</span>
                    </div>
                    <div class="post-image">${post.image}</div>
                    <div class="post-actions">
                        <span>❤️</span><span>💬</span><span>📤</span>
                    </div>
                    <div class="post-likes">${post.likes} отметок "Нравится"</div>
                    <div class="post-caption"><strong>${post.user}</strong> ${post.caption}</div>
                    ${post.user === 'anonim_minsk' && currentLvl === 6 ? `
                        <div style="padding: 14px; display: flex; gap: 10px;">
                            <button class="btn-action" style="flex: 1; padding: 8px;" onclick="processAction('bad')">❤️ ЛАЙКНУТЬ</button>
                            <button class="btn-action" style="flex: 1; padding: 8px; background: var(--success);" onclick="processAction('ok')">🚨 ЖАЛОБА</button>
                        </div>
                    ` : ''}
                </div>
            `).join('');
        }

        function renderKufar() {
            const side = document.getElementById('kufar-side');
            const chat = document.getElementById('kufar-chat');
            
            let chats = [
                { id: 'buyer1', name: '👤 Покупатель (велосипед)', last: 'Ещё продаёте?', time: '13:10', avatar: '🚲' },
                { id: 'buyer2', name: '👤 Покупатель (телефон)', last: 'А торг уместен?', time: 'Вчера', avatar: '📱' }
            ];
            
            if (currentLvl === 4) {
                chats.push({ id: 'buyer_fake', name: '👤 Покупатель (кроссовки)', last: 'Всё оплатил, проверяйте!', time: '09:30', avatar: '👟' });
            }
            
            side.innerHTML = chats.map(c => `
                <div class="chat-item" data-chat-id="${c.id}" onclick="selectKufarChat('${c.id}')" style="border-bottom: 1px solid #ffd9b3;">
                    <div class="chat-avatar" style="background: #ffe0b2;">${c.avatar}</div>
                    <div class="chat-info">
                        <div class="chat-name">${c.name}</div>
                        <div class="chat-last" style="color: #666;">${c.last}</div>
                    </div>
                    <div class="chat-time" style="color: #999;">${c.time}</div>
                </div>
            `).join('');
            
            chat.innerHTML = '<div style="color: #999; text-align: center; margin-top: 200px;">Выберите чат</div>';
        }

        function selectKufarChat(chatId) {
            const chat = document.getElementById('kufar-chat');
            document.querySelectorAll('#kufar-side .chat-item').forEach(el => el.classList.remove('active'));
            document.querySelector(`[data-chat-id="${chatId}"]`).classList.add('active');
            
            if (chatId === 'buyer_fake' && currentLvl === 4) {
                chat.innerHTML = `
                    <div style="display: flex; flex-direction: column; height: 100%;">
                        <div style="flex: 1;">
                            <div style="background: black; padding: 15px; border-radius: 12px; max-width: 80%; border: 1px solid #eee;">
                                Влад, я оплатил кроссовки! Забирайте деньги по ссылке: <br>
                                <span style="color: #0066cc; text-decoration: underline;">kufar-pay.pro/id9921</span>
                            </div>
                        </div>
                        <div style="display: flex; gap: 10px; margin-top: 20px;">
                            <button class="btn-action" style="flex: 1; background: #ff6b00;" onclick="processAction('bad')">🔗 ПЕРЕЙТИ</button>
                            <button class="btn-action" style="flex: 1; background: #10b981;" onclick="processAction('ok')">🚨 МОШЕННИКИ</button>
                        </div>
                    </div>
                `;
            } else {
                chat.innerHTML = `
                    <div style="color: #999; text-align: center; margin-top: 200px;">
                        💬 Переписка по объявлению.
                    </div>
                `;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)