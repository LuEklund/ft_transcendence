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
		score:	number;
		dirX:	number;
		dirY:	number;
		padY:	number;

		constructor(x: number, y: number, radius: number, height: number) {
			this.color = "white";
			this.x = x;
			this.y = y;
			this.radius = radius;
			this.height = height;
			this.dirX = 4;
			this.dirY = 4;
			this.padY = 0;
			this.score = 0;
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

		drawNet() {
			if (canvasRef.current) {
				const canvas = canvasRef.current;
				const context = canvas.getContext("2d");

				if (context) {
					for (let i = 0; i <= canvas.height; i+=15) {
						context.fillStyle = this.color;
						context.fillRect(this.x, i, this.radius, this.height);
					}
				}
			}
		}

		drawText() {
			if (canvasRef.current) {
				const canvas = canvasRef.current;
				const context = canvas.getContext("2d");

				if (context) {
					context.font = "30px Arial";
					context.fillStyle = "white";
					context.fillText(this.score.toString(), this.x, this.y);
				}
			}
		}

		moveBall(pad1: gameObject, pad2: gameObject, player1Score: gameObject, player2Score: gameObject){
			if (canvasRef.current) {
				const canvas = canvasRef.current;
				const context = canvas.getContext("2d");

				if (context) {
					this.x += this.dirX;
					this.y += this.dirY;

					// Collision detection with pads
					if ((this.x - 10 < pad1.x + pad1.radius && this.y > pad1.y && this.y < pad1.y + pad1.height) ||
					(this.x + 10 > pad2.x && this.y > pad2.y && this.y < pad2.y + pad2.height)) {
						this.dirX = -this.dirX * 1.1;

						// If the ball hits the top half of the paddle, make it bounce upwards
						// If it hits the bottom half, make it bounce downwards
						if (this.y < pad1.y + pad1.height / 2 || this.y < pad2.y + pad2.height / 2) {
							this.dirY = -Math.abs(this.dirY) * 1.1;
						}
						else {
							this.dirY = Math.abs(this.dirY) * 1.1;
						}
					}

					//Condition to bounce at top or bottom of the screen and reset after scoring
					if (this.y + 10 > canvas.height || this.y - 10 < 0)
						this.dirY = - this.dirY;
					else if (this.x + 10 > canvas.width) {
						player1Score.score += 1;
						this.dirX = -4;
						this.dirY = 4;
						this.x = canvas.width/2;
						this.y = canvas.height/2;
					}
					else if (this.x - 10 < 0) {
						player2Score.score += 1;
						this.dirX = 4;
						this.dirY = 4;
						this.x = canvas.width/2;
						this.y = canvas.height/2;
					}
				}
			}
		}

		movePad(){
			if (canvasRef.current) {
				const canvas = canvasRef.current;
				const context = canvas.getContext("2d");

				if (context) {
					if (this.y + this.padY >= 0 && this.y + this.padY <= canvas.height - this.height)
						this.y += this.padY;
					else if (this.y + this.padY < 0)
						this.y = 0;
					else if (this.y + this.padY > canvas.height)
						this.y = canvas.height - this.height;
				}
			}
		}
	}

	function drawObjects(canvas: HTMLCanvasElement, ball: gameObject, pad1: gameObject, pad2: gameObject,
		player1Score : gameObject, player2Score: gameObject) {
		const net = new gameObject(canvas.width/2 - 1, 0, 2, 10);

		pad1.drawPad();
		pad2.drawPad();
		ball.drawBall();
		net.drawNet();
		player1Score.drawText();
		player2Score.drawText();
	}

	function drawCanvas(canvas: HTMLCanvasElement, context: CanvasRenderingContext2D) {
		canvas.width = 800;
		canvas.height = 600;
		context.fillStyle = "black";
		context.fillRect(0, 0, canvas.width, canvas.height);
	}

	useEffect(() => {
		if (canvasRef.current) {
			const canvas = canvasRef.current;
			const context = canvas.getContext("2d");

			if (context) {
				const ball = new gameObject(canvas.width/2, canvas.height/2, 10, 10);
				const pad1 = new gameObject(5, 255, 25, 100);
				const pad2 = new gameObject(canvas.width-30, 255, 25, 100);
				const player1Score = new gameObject(canvas.width/4, canvas.height/10, 25, 50);
				const player2Score = new gameObject(canvas.width*0.75, canvas.height/10, 25, 50);
				drawObjects(canvas, ball, pad1, pad2, player1Score, player2Score);

				const handleKeyDown = (event: KeyboardEvent) => {
					switch (event.key) {
					case "w":
						pad1.padY = -4;
						break;
					case "s":
						pad1.padY = 4;
						break;
					case "ArrowUp":
						pad2.padY = -4;
						break;
					case "ArrowDown":
						pad2.padY = 4;
						break;
					}
				};

				const handleKeyUp = (event: KeyboardEvent) => {
					switch (event.key) {
					case "w":
					case "s":
						pad1.padY = 0;
						break;
					case "ArrowUp":
					case "ArrowDown":
						pad2.padY = 0;
						break;
					}
				};

				window.addEventListener("keydown", handleKeyDown);
				window.addEventListener("keyup", handleKeyUp);

				const gameLoop = () => {
					context.clearRect(0, 0, canvas.width, canvas.height);
					drawCanvas(canvas, context);
					ball.moveBall(pad1, pad2, player1Score, player2Score);
					pad1.movePad();
					pad2.movePad();
					drawObjects(canvas, ball, pad1, pad2, player1Score, player2Score);
					window.requestAnimationFrame(gameLoop);
				};

				gameLoop();

				return () => {
					window.removeEventListener("keydown", handleKeyDown);
					window.removeEventListener("keyup", handleKeyUp);
				};
			}
		}
	}, []);

	return (
		<div>
			<a> WEEEEEEELCOME xD </a>
			<canvas className = "myCanvas" ref={canvasRef} />
		</div>
	);
};
