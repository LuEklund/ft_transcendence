import { useState } from "react";
import "./Login.css";

import { SignUp } from "./SignUp";
import { InfoToSign } from "./Info";
import { SignIn } from "./SignIn";
import { Loading } from "../Loading";
import { TwoFactorAuth } from "./TwoFactorAuth";

export interface InfoToSignProps {
	isLogin: boolean;
	setIsLogin: (value: boolean) => void;
	isLoading: boolean;
	setIsLoading: (value: boolean) => void;
	setIsTwoFactAuthRequired: (value: boolean) => void;
	setIsAuth: (value: boolean) => void;
}

interface LoginProps {
	isAuthenticated: boolean;
	setIsAuthenticated: (value: boolean) => void;
}

export const Login = (props: LoginProps) : JSX.Element | undefined => {
	const [isTwoFactAuthRequired, setIsTwoFactAuthRequired] = useState(false);
	const [isLogin, setIsLogin] = useState(true);
	const [isLoading, setIsLoading] = useState(false);

	if (!isTwoFactAuthRequired) {
		return (
			<div className="container-fluid signIn-signUp-pages d-flex align-items-center justify-content-center">
				<div className="row">
					<div className="col-10 sign-box">
						<div className="row full-height align-items-center">
							<div className={`info-bg ${isLogin ? "border-right" : "border-left"} phone-hide`}></div>
							<div className={`col-12 col-md-8 order-${isLogin ? "0 is-login" : "1 is-signup"}`} style={{ zIndex: 2 }}>
								<div className="row">
									<div className="col-12">
										{isLogin && <SignIn isLogin={isLogin} setIsLogin={setIsLogin}
											isLoading={isLoading} setIsLoading={setIsLoading}
											setIsTwoFactAuthRequired={setIsTwoFactAuthRequired}
											setIsAuth={props.setIsAuthenticated}/>}
										{!isLogin && <SignUp isLogin={isLogin} setIsLogin={setIsLogin}
											isLoading={isLoading} setIsLoading={setIsLoading}
											setIsTwoFactAuthRequired={setIsTwoFactAuthRequired}
											setIsAuth={props.setIsAuthenticated}/>}
									</div>
								</div>
							</div>
							<div className={`phone-hide col-md-4 full-height ${isLogin ? "1 is-login" : "0 is-signup"}`} style={{ zIndex: 2 }}>
								<div className="row full-height align-items-center">
									<div className="col-12">
										<InfoToSign isLogin={isLogin} setIsLogin={setIsLogin}
											isLoading={isLoading} setIsLoading={setIsLoading}
											setIsTwoFactAuthRequired={setIsTwoFactAuthRequired}
											setIsAuth={props.setIsAuthenticated}/>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				{isLoading && <Loading type="border" message="" variant="success"/>}
			</div>
		);
	}
	if (isTwoFactAuthRequired)
		return <TwoFactorAuth setIsLoading={setIsLoading} setIsAuthReq={setIsTwoFactAuthRequired}/>;
};
