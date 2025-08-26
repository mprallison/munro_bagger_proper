const fireworks = [];
const particles = [];

function random(min, max) {
  return Math.random() * (max - min) + min;
}

class Firework {
  constructor() {
    this.x = random(0, cw);
    this.y = ch;
    this.targetY = random(ch/4, ch/2);
    this.color = `hsl(${random(0,360)},100%,50%)`;
    this.speed = random(4, 7);
    this.exploded = false;
  }
  update() {
    this.y -= this.speed;
    if (this.y <= this.targetY && !this.exploded) {
      this.explode();
      this.exploded = true;
    }
  }
  draw() {
    if (!this.exploded) {
      ctx.beginPath();
      ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();
    }
  }
  explode() {
    for (let i = 0; i < 50; i++) {
      particles.push(new Particle(this.x, this.y, this.color));
    }
  }
}

class Particle {
  constructor(x, y, color) {
    this.x = x;
    this.y = y;
    this.color = color;
    this.speed = random(1,6);
    this.angle = random(0, Math.PI * 2);
    this.alpha = 1;
    this.friction = 0.95;
  }
  update() {
    this.x += Math.cos(this.angle) * this.speed;
    this.y += Math.sin(this.angle) * this.speed;
    this.speed *= this.friction;
    this.alpha -= 0.02;
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.globalAlpha = this.alpha;
    ctx.fill();
    ctx.globalAlpha = 1;
  }
}

let stopFireworks = false;
setTimeout(() => stopFireworks = true, 4000); // stop after 3 seconds

function animate() {
  requestAnimationFrame(animate);
  // Clear canvas with partial transparency to create trails
  ctx.clearRect(0, 0, cw, ch);

  if (!stopFireworks && Math.random() < 0.05) fireworks.push(new Firework());

  for (let i = fireworks.length - 1; i >= 0; i--) {
    fireworks[i].update();
    fireworks[i].draw();
    if (fireworks[i].exploded) fireworks.splice(i, 1);
  }

  for (let i = particles.length - 1; i >= 0; i--) {
    particles[i].update();
    particles[i].draw();
    if (particles[i].alpha <= 0) particles.splice(i, 1);
  }
};

window.animate = animate;