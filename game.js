// 게임 설정
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const leftBtn = document.getElementById('leftBtn');
const rightBtn = document.getElementById('rightBtn');

// 오디오 설정
let audioContext = null;
const sounds = {
    brickHit: new Audio('sounds/brick_hit.wav'),
    paddleHit: new Audio('sounds/paddle_hit.wav'),
    gameOver: new Audio('sounds/game_over.wav'),
    levelUp: new Audio('sounds/level_up.wav')
};

// 오디오 초기화 함수
function initAudio() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        // 모든 사운드를 미리 로드
        Object.values(sounds).forEach(sound => {
            sound.load();
            // 볼륨 설정
            sound.volume = 0.5;
        });
    }
}

// 사운드 재생 함수
function playSound(soundName) {
    if (audioContext && audioContext.state === 'suspended') {
        audioContext.resume();
    }
    if (sounds[soundName]) {
        sounds[soundName].currentTime = 0;
        sounds[soundName].play().catch(error => console.log('Sound play failed:', error));
    }
}

// 게임 상태
let gameWidth = 800;
let gameHeight = 600;
let paddleWidth = 100;
let paddleHeight = 20;
let ballRadius = 10;
let brickWidth = 80;
let brickHeight = 30;
const brickRows = 5;
const brickCols = 10;

let paddleX = 0;
let ballX = 0;
let ballY = 0;
let ballSpeedX = 5;
let ballSpeedY = -5;
let score = 0;
let lives = 3;
let gameOver = false;
let bricks = [];

// 캔버스 크기 조정
function resizeCanvas() {
    const container = document.getElementById('gameContainer');
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;
    
    // 게임 비율 유지 (16:9)
    const gameRatio = 16 / 9;
    let canvasWidth = containerWidth;
    let canvasHeight = containerWidth / gameRatio;
    
    if (canvasHeight > containerHeight) {
        canvasHeight = containerHeight;
        canvasWidth = containerHeight * gameRatio;
    }
    
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;
    
    // 게임 요소 크기 조정
    gameWidth = canvasWidth;
    gameHeight = canvasHeight;
    paddleWidth = canvasWidth * 0.2;
    paddleHeight = canvasHeight * 0.03;
    ballRadius = canvasWidth * 0.015;
    brickWidth = canvasWidth * 0.1;
    brickHeight = canvasHeight * 0.05;
    
    // 게임 상태 초기화
    paddleX = (gameWidth - paddleWidth) / 2;
    ballX = gameWidth / 2;
    ballY = gameHeight - 50;
}

// 벽돌 초기화
function initBricks() {
    bricks = [];
    for (let row = 0; row < brickRows; row++) {
        for (let col = 0; col < brickCols; col++) {
            bricks.push({
                x: col * (brickWidth + 10) + 10,
                y: row * (brickHeight + 10) + 50,
                width: brickWidth,
                height: brickHeight,
                visible: true
            });
        }
    }
}

// 게임 그리기
function draw() {
    // 화면 지우기
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, gameWidth, gameHeight);

    // 패들 그리기
    ctx.fillStyle = '#fff';
    ctx.fillRect(paddleX, gameHeight - paddleHeight, paddleWidth, paddleHeight);

    // 공 그리기
    ctx.beginPath();
    ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = '#fff';
    ctx.fill();
    ctx.closePath();

    // 벽돌 그리기
    bricks.forEach(brick => {
        if (brick.visible) {
            ctx.fillStyle = '#00f';
            ctx.fillRect(brick.x, brick.y, brick.width, brick.height);
        }
    });

    // 점수 표시
    ctx.fillStyle = '#fff';
    ctx.font = '20px Arial';
    ctx.fillText(`Score: ${score}`, 10, 30);
    ctx.fillText(`Lives: ${lives}`, gameWidth - 100, 30);

    if (gameOver) {
        ctx.font = '40px Arial';
        ctx.fillText('Game Over!', gameWidth/2 - 100, gameHeight/2);
    }
}

// 충돌 감지
function collisionDetection() {
    bricks.forEach(brick => {
        if (brick.visible) {
            if (ballX > brick.x && ballX < brick.x + brick.width &&
                ballY > brick.y && ballY < brick.y + brick.height) {
                ballSpeedY = -ballSpeedY;
                brick.visible = false;
                score += 10;
                playSound('brickHit');
                
                // 모든 벽돌이 제거되었는지 확인
                if (bricks.every(b => !b.visible)) {
                    initBricks();
                    playSound('levelUp');
                }
            }
        }
    });
}

// 게임 업데이트
function update() {
    if (gameOver) return;

    // 공 이동
    ballX += ballSpeedX;
    ballY += ballSpeedY;

    // 벽 충돌
    if (ballX + ballRadius > gameWidth || ballX - ballRadius < 0) {
        ballSpeedX = -ballSpeedX;
    }
    if (ballY - ballRadius < 0) {
        ballSpeedY = -ballSpeedY;
    }

    // 패들 충돌
    if (ballY + ballRadius > gameHeight - paddleHeight &&
        ballX > paddleX && ballX < paddleX + paddleWidth) {
        ballSpeedY = -ballSpeedY;
        playSound('paddleHit');
    }

    // 게임 오버
    if (ballY + ballRadius > gameHeight) {
        lives--;
        if (lives <= 0) {
            gameOver = true;
            playSound('gameOver');
        } else {
            ballX = gameWidth / 2;
            ballY = gameHeight - 50;
            ballSpeedX = 5;
            ballSpeedY = -5;
        }
    }

    collisionDetection();
}

// 키보드 입력 처리
document.addEventListener('keydown', (e) => {
    initAudio(); // 키보드 입력 시 오디오 초기화
    if (e.key === 'ArrowLeft' && paddleX > 0) {
        paddleX -= 20;
    } else if (e.key === 'ArrowRight' && paddleX < gameWidth - paddleWidth) {
        paddleX += 20;
    }
});

// 버튼 이벤트 처리
leftBtn.addEventListener('mousedown', () => {
    initAudio(); // 버튼 클릭 시 오디오 초기화
    paddleX -= 10;
    if (paddleX < 0) paddleX = 0;
});

rightBtn.addEventListener('mousedown', () => {
    initAudio(); // 버튼 클릭 시 오디오 초기화
    paddleX += 10;
    if (paddleX > gameWidth - paddleWidth) paddleX = gameWidth - paddleWidth;
});

// 게임 루프
function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// 창 크기 변경 시 캔버스 크기 조정
window.addEventListener('resize', resizeCanvas);
window.addEventListener('orientationchange', resizeCanvas);

// 게임 초기화
window.addEventListener('load', () => {
    resizeCanvas();
    initBricks();
    gameLoop();
}); 