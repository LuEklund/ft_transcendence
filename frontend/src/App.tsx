import React from "react";
import * as THREE from "three";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Homepage } from "./Components/homepage/Homepage";
import { Login } from "./Components/LoginPage/Login";
import { MainMenu } from "./Components/MainMenu/MainMenu";
import { Pong } from "./Components/games/Pong";
import { Pong3D } from "./Components/games/Pong3D";

function App() {
	return (
		<div className="App">
			<BrowserRouter>
				<Routes>
					<Route path="/" element={<Homepage />} />
					<Route path="/login" element={<Login />} />
					<Route path="/mainmenu" element={<MainMenu />} />
					<Route path="/pong" element={<Pong />} />
					<Route path="/pong3D" element={<Pong3D />} />
				</Routes>
			</BrowserRouter>
		</div>
	);
}

export default App;
