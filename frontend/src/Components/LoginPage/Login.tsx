import { useState } from "react";
import "./Login.css";

import { PhoneAuthentication } from "./PhoneAuthentication";
import { SignUp } from "./SignUp";

interface loginFormProps {
	setIsLoading: (valie: boolean) => void;
	isLoading: boolean;
	setLoginState: (value: LoginState) => void;
}
export interface InfoToSignProps {
	isLogin: boolean;
	setIsLogin: (value: boolean) => void;
}
export enum LoginState {
	Unidentified,
	Identified,
	SignedUp
}
export enum AuthenticationMethod {
	NULL,
	Phone,
	Google
}
export const Login = () : JSX.Element | undefined => {
	const [authenticationMethod, setAuthenticationMethod] = useState(AuthenticationMethod.NULL);
	const [isLogin, setIsLogin] = useState(true);

	if (authenticationMethod === AuthenticationMethod.NULL) {
		return (
			<div className="container-fluid signIn-signUp-pages d-flex align-items-center justify-content-center">
				<div className="row">
					<div className="col-10 sign-box">
						<div className="row full-height align-items-center">
							<div className={`info-bg ${isLogin ? "border-right" : "border-left"}`}></div>
							<div className={`col-12 col-md-8 order-${isLogin ? "0 is-login" : "1 is-signup"}`} style={{ zIndex: 2 }}>
								<div className="row">
									<div className="col-12">
										{isLogin && <SignIn isLogin={isLogin} setIsLogin={setIsLogin} />}
										{!isLogin && <SignUp isLogin={isLogin} setIsLogin={setIsLogin} />}
									</div>
								</div>
							</div>
							<div className={`phone-hide col-md-4 full-height ${isLogin ? "1 is-login" : "0 is-signup"}`} style={{ zIndex: 2 }}>
								<div className="row full-height align-items-center">
									<div className="col-12">
										<InfoToSign isLogin={isLogin} setIsLogin={setIsLogin} />
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		);
	}
	else if (authenticationMethod === AuthenticationMethod.Phone) {
		return <PhoneAuthentication />;
	}

};

const SignIn = (props: InfoToSignProps) : JSX.Element => {
	const changeToSignInForm = () => {
		props.setIsLogin(false);
	};
	return (
		<div className="row d-flex align-items-center justify-content-center mt-5 mb-5">
			<div className="col-10 offset-1 form-area d-flex flex-column align-items-center justify-content-center">
				<div className="row login-form-title">
					<h2 className="col-12 ">Sign in to Ft-Transcendence</h2>
				</div>
				<div className="row">
					<form className="col-10 offset-1">
						<div className="row mt-4">
							<input
								className="col-10 my-0.2 my-md-1 form-control"
								placeholder="Username"
								type="text"
							/>
							<input
								className="col-10 my-1 form-control"
								placeholder="Password"
								type="password"
							/>
						</div>
						<div className="row mt-0.5 mt-md-3">
							<div className="col-12 col-md-8 offset-md-2">
								<a href="#">Forgot your password?</a>
								<button className="mt-4 btn btn-success w-100">SIGN IN</button>
							</div>
						</div>
						<div className="col-10 offset-1 mt-3">
							<div className="col-8 offset-2">
								<p className="mb-0">or</p>
								<button className="btn btn-info w-100">Sign with 42</button>
							</div>
						</div>
						<div className="small-screen-change-register row mt-4 mb-1">
							<div className="col-12">
								<button onClick={()=>changeToSignInForm()} className="btn btn-secondary">No account? Register here</button>
							</div>
						</div>
					</form>
				</div>
			</div>

		</div>
	);
};

const InfoToSign = (props: InfoToSignProps) :JSX.Element => {
	if (props.isLogin)
		return <StillHasNoAccount isLogin={props.isLogin} setIsLogin={props.setIsLogin}/>;
	else
		return <AlreadyAsAccount isLogin={props.isLogin} setIsLogin={props.setIsLogin}/>;
};

const StillHasNoAccount = (props: InfoToSignProps) : JSX.Element => {
	const changeToSignInForm = () => {
		props.setIsLogin(false);
	};
	return (
		<div className="row">
			<div className="p-3 col-12 d-flex flex-column align-items-center justify-content-center">
				<h2>New here?</h2>
				<p>Sign up, test your skills and challenge your friends</p>
				<button
					onClick={()=>changeToSignInForm()}
					className="btn btn-primary w-100 my-5">SIGN UP</button>
			</div>
		</div>
	);
};

const AlreadyAsAccount = (props: InfoToSignProps) : JSX.Element => {

	const changeToSignInForm = () => {
		props.setIsLogin(true);
	};
	return (
		<div className="row">
			<div className="p-3 col-12 d-flex flex-column align-items-center justify-content-center">
				<h2>Already have an account?</h2>
				<p>Do not waste time and login right now to play with your friends</p>
				<button
					onClick={()=>changeToSignInForm()}
					className="btn btn-primary w-100 my-5">SIGN IN</button>
			</div>
		</div>
	);
};
