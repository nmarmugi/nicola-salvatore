import React, { SetStateAction } from "react";
import { IInputValue, IIsInvalid } from "./emailInput";

export interface ISwitchAuth {
	isLoginPage: boolean;
	setIsLoginPage: React.Dispatch<SetStateAction<boolean>>;
	setInputValue: React.Dispatch<SetStateAction<IInputValue>>;
	setIsInvalid: React.Dispatch<SetStateAction<IIsInvalid>>
	setShowPassword: React.Dispatch<SetStateAction<boolean>>;
	setMessage: React.Dispatch<SetStateAction<string>>;
	isSending: boolean;
}
