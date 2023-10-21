import "./Pong.css";
import { useEffect, useRef } from "react";

export const Pong = () : JSX.Element => {
	const canvasRef = useRef<HTMLCanvasElement>(null);

	class gameObject {
		color:	string;
		x:		number;
		y:		number;
		radius:	number;
		height:	number;
		speed:	number;
		dirX:	boolean;
		dirY:	boolean;

		constructor(x: number, y: number, radius: number, height: number, dirX: boolean, dirY: boolean) {
			this.color = "white";
			this.x = x;
			this.y = y;
			this.radius = radius;
			this.height = height;
			this.speed = 8;
			this.dirX = dirX;
			this.dirY = dirY;
		}

		drawPad() {
			if (canvasRef.current) {
				const canvas = canvasRef.current;
				const context = canvas.getContext("2d");

				if (context) {
					context.fillStyle = this.color;
					context.fillRect(this.x, this.y, this.radius, this.height);
				}
			}
		}

		drawBall() {
			if (canvasRef.current) {
				const canvas = canvasRef.current;
				const context = canvas.getContext("2d");

				if (context) {
					context.beginPath();
					context.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
					context.fillStyle = this.color;
					context.fill();
					context.closePath();
				}
			}
		}

		moveBall() {
			if (canvasRef.current) {
				const canvas = canvasRef.current;
				const context = canvas.getContext("2d");

				if (context) {
					context.clearRect(0, 0, canvas.width + 100, canvas.height);
					this.drawPad();
					if (this.dirY) this.y += this.speed;
					if (this.dirX) this.x += this.speed;
					if (!this.dirY) this.y -= this.speed;
					if (!this.dirX) this.x -= this.speed;

					// Check for boundary collision
					if (this.y + this.radius > canvas.height || this.y - this.radius < 0) {
						this.dirY = !this.dirY;
					}
					if (this.x + this.radius > canvas.width || this.x - this.radius < 0) {
						this.dirX = !this.dirX;
					}

					// Add acceleration
					this.speed *= 0.99;
					this.speed += 0.25;

					context.fillRect(canvas.width / 2 - 5, 0, 10, canvas.height);
					context.fillStyle = "white";
					context.fill();
					this.drawBall();
				}
			}
		}

	}

	function drawPads(canvas: HTMLCanvasElement) {
		const pad1 = new gameObject(50, 325, 25, 100, false, false);
		const pad2 = new gameObject(canvas.width-50, 325, 25, 100, false, false);
		// const ball = new gameObject(canvas.width/2, canvas.height/2, 10, 10);

		pad1.drawPad();
		pad2.drawPad();
		// ball.drawBall();
	}

	function moveBallLoop(ball :gameObject) {
		ball.drawBall();
		if(requestAnimationFrame) {
			requestAnimationFrame(() => {
				moveBallLoop(ball);
			});
		}
	}

	useEffect(() => {
		if (canvasRef.current) {
			const canvas = canvasRef.current;
			const context = canvas.getContext("2d");

			if (context) {
				canvas.width = 750;
				canvas.height = 750;
				context.fillStyle = "black";
				context.fillRect(0, 0, canvas.width, canvas.height);
			}
			drawPads(canvas);

			const ball = new gameObject(canvas.width / 2, canvas.height / 2, 10, 10, true, true);
			moveBallLoop(ball);
		}
	}, []);

	return (
		<div>
			<a> WEEEEEEELCOME xD</a>
			<canvas className = "myCanvas" ref={canvasRef} />
		</div>
	);
};
