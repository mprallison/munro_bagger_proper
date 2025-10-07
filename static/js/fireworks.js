// shamelessly vibed

export function startFireworksOnMap(map) {
    // Append canvas to Leaflet overlayPane
    const canvas = document.createElement('canvas');
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.pointerEvents = 'none';
    map.getPane('overlayPane').appendChild(canvas);
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        const size = map.getSize();
        canvas.width = size.x;
        canvas.height = size.y;
    }

    resizeCanvas();
    map.on('resize', resizeCanvas);

    class Particle {
        constructor(x, y, color) {
            this.x = x;
            this.y = y;
            this.color = color;
            const angle = Math.random() * 2 * Math.PI;
            const speed = Math.random() * 5 + 2;
            this.velocity = { x: Math.cos(angle) * speed, y: Math.sin(angle) * speed };
            this.life = 2;
            this.alpha = 1;
        }

        update(deltaTime) {
            this.x += this.velocity.x;
            this.y += this.velocity.y;
            this.life -= deltaTime;
            this.alpha = Math.max(this.life / 2, 0);
        }

        draw() {
            ctx.save();
            ctx.globalAlpha = this.alpha;
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
            //ctx.fill();
            ctx.fillText('🏔️', this.x, this.y);
            ctx.restore();
        }
    }

    const fireworks = [];

    function createRandomFireworks() {
        const colors = ["red", "yellow", "blue", "orange", "green", "purple"];
        const color = colors[Math.floor(Math.random() * colors.length)];
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height / 2;

        for (let i = 0; i < 50; i++) {
            fireworks.push(new Particle(x, y, color));
        }
    }

    let lastTime = 0;
    function animate(timestamp) {
        const deltaTime = (timestamp - lastTime) / 1000;
        lastTime = timestamp;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        fireworks.forEach(p => p.update(deltaTime));
        fireworks.forEach(p => p.draw());

        for (let i = fireworks.length - 1; i >= 0; i--) {
            if (fireworks[i].life <= 0) fireworks.splice(i, 1);
        }   
        requestAnimationFrame(animate);
    }

    requestAnimationFrame(animate);

    // Fireworks for 2 seconds
    const interval = setInterval(createRandomFireworks, 200);
    setTimeout(() => {
        clearInterval(interval);
        setTimeout(() => {
            canvas.remove();
        }, 2000);
    }, 2000);
}

window.startFireworksOnMap = startFireworksOnMap;