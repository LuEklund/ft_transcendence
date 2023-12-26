class pongObject {
	constructor(x, y, radius, height, context, canvas) {
		this.color = "white";
		this.x = x;
		this.y = y;
		this.radius = radius;
		this.height = height;
		this.dirX = 4;
		this.dirY = 4;
		this.padY = 0;
		this.score = 0;
		this.context = context;
		this.canvas = canvas;
	}

	drawPad() {
		this.context.fillStyle = this.color;
		this.context.fillRect(this.x, this.y, this.radius, this.height);
	}

	drawBall() {
		this.context.beginPath();
		this.context.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
		this.context.fillStyle = this.color;
		this.context.fill();
		this.context.closePath();
	}

	drawNet() {
		for (let i = 0; i <= this.canvas.height; i += 15) {
			this.context.fillStyle = this.color;
			this.context.fillRect(this.x, i, this.radius, this.height);
		}
	}

	drawText() {
		this.context.font = "30px Arial";
		this.context.fillStyle = "white";
		this.context.fillText(this.score.toString(), this.x, this.y);
	}

	moveBall(pad1, pad2, player1Score, player2Score) {
		this.x += this.dirX;
		this.y += this.dirY;

		if ((this.x - 10 < pad1.x + pad1.radius && this.y > pad1.y && this.y < pad1.y + pad1.height) ||
		(this.x + 10 > pad2.x && this.y > pad2.y && this.y < pad2.y + pad2.height)) {
			this.dirX = -this.dirX * 1.1;

		if (this.y < pad1.y + pad1.height / 2 || this.y < pad2.y + pad2.height / 2) {
			this.dirY = -Math.abs(this.dirY) * 1.1;
		} else {
			this.dirY = Math.abs(this.dirY) * 1.1;
		}
		}

		//conditions to be satisfied in order to score a goal or ball bounce back from top of the canvas
		//additionally, reset the ball to initial position when a player scores
		if (this.y + 10 > this.canvas.height || this.y - 10 < 0)
			this.dirY = -this.dirY;
		else if (this.x + 10 > this.canvas.width) {
			player1Score.score += 1;
			this.dirX = -4;
			this.dirY = 4;
			this.x = this.canvas.width / 2;
			this.y = this.canvas.height / 2;
		} else if (this.x - 10 < 0) {
			player2Score.score += 1;
			this.dirX = 4;
			this.dirY = 4;
			this.x = this.canvas.width / 2;
			this.y = this.canvas.height / 2;
		}
	}

	movePad() {
		if (this.y + this.padY >= 0 && this.y + this.padY <= this.canvas.height - this.height)
			this.y += this.padY;
		else if (this.y + this.padY < 0)
			this.y = 0;
		else if (this.y + this.padY > this.canvas.height)
			this.y = this.canvas.height - this.height;
	}
}
