// 게임 설정
const WIDTH = 800;
const HEIGHT = 600;
const PADDLE_WIDTH = 100;
const PADDLE_HEIGHT = 20;
const BALL_RADIUS = 10;
const BRICK_WIDTH = 80;
const BRICK_HEIGHT = 30;
const BRICK_ROWS = 5;
const BRICK_COLS = 10;

// 게임 상태
let paddleX = (WIDTH - PADDLE_WIDTH) / 2;
let ballX = WIDTH / 2;
let ballY = HEIGHT - 50;
let ballSpeedX = 5;
let ballSpeedY = -5;
let score = 0;
let lives = 3;
let gameOver = false;
let bricks = [];

// 캔버스 설정
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = WIDTH;
canvas.height = HEIGHT;

// 벽돌 초기화
function initBricks() {
    bricks = [];
    for (let row = 0; row < BRICK_ROWS; row++) {
        for (let col = 0; col < BRICK_COLS; col++) {
            bricks.push({
                x: col * (BRICK_WIDTH + 10) + 10,
                y: row * (BRICK_HEIGHT + 10) + 50,
                width: BRICK_WIDTH,
                height: BRICK_HEIGHT,
                visible: true
            });
        }
    }
}

// 게임 그리기
function draw() {
    // 화면 지우기
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // 패들 그리기
    ctx.fillStyle = '#fff';
    ctx.fillRect(paddleX, HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT);

    // 공 그리기
    ctx.beginPath();
    ctx.arc(ballX, ballY, BALL_RADIUS, 0, Math.PI * 2);
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
    ctx.fillText(`Lives: ${lives}`, WIDTH - 100, 30);

    if (gameOver) {
        ctx.font = '40px Arial';
        ctx.fillText('Game Over!', WIDTH/2 - 100, HEIGHT/2);
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
                
                // 모든 벽돌이 제거되었는지 확인
                if (bricks.every(b => !b.visible)) {
                    initBricks();
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
    if (ballX + BALL_RADIUS > WIDTH || ballX - BALL_RADIUS < 0) {
        ballSpeedX = -ballSpeedX;
    }
    if (ballY - BALL_RADIUS < 0) {
        ballSpeedY = -ballSpeedY;
    }

    // 패들 충돌
    if (ballY + BALL_RADIUS > HEIGHT - PADDLE_HEIGHT &&
        ballX > paddleX && ballX < paddleX + PADDLE_WIDTH) {
        ballSpeedY = -ballSpeedY;
    }

    // 게임 오버
    if (ballY + BALL_RADIUS > HEIGHT) {
        lives--;
        if (lives <= 0) {
            gameOver = true;
        } else {
            ballX = WIDTH / 2;
            ballY = HEIGHT - 50;
            ballSpeedX = 5;
            ballSpeedY = -5;
        }
    }

    collisionDetection();
}

// 키보드 입력 처리
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft' && paddleX > 0) {
        paddleX -= 20;
    } else if (e.key === 'ArrowRight' && paddleX < WIDTH - PADDLE_WIDTH) {
        paddleX += 20;
    }
});

// 게임 루프
function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// 게임 시작
initBricks();
gameLoop(); 