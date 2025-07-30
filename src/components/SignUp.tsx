import {type ChangeEvent, type FormEvent, useState} from "react";
import axios from "../axios";
import {Link, useNavigate} from "react-router-dom";
import type {SignUpFormType} from "../types";
import type {AxiosError} from "axios";

export function SignUp() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState<SignUpFormType>({
    name: "",
    username: "",
    password: ""
  });

  const [error, setError] = useState<string>("");

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const {name, value} = e.target;
    setFormData(prev => ({...prev, [name]: value}));
  };

  async function handleSignUp(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    try {
      await axios.post("register/", formData);
      navigate("/");
    } catch (error) {
      const err = error as AxiosError;
      setError(err.message || "Signup failed");
    }
  }

  return (
    <form onSubmit={handleSignUp}
          className={'w-1/3 h-max mx-auto rounded-2xl border-2 border-gray-300 flex flex-col items-center justify-center mt-20'}>

      <h1 className={'mt-10'}>SIGNUP</h1>

      <input
        type="text"
        name="name"
        placeholder="name"
        className="w-1/2 border-2 border-amber-300 rounded-xl mt-10 mb-5 box-border pl-5 py-2"
        value={formData.name}
        onChange={handleChange}
      />

      <input
        type="text"
        name="username"
        placeholder="username"
        className="w-1/2 border-2 border-amber-300 rounded-xl mt-5 mb-5 box-border pl-5 py-2"
        value={formData.username}
        onChange={handleChange}
      />

      <input
        type="password"
        name="password"
        placeholder="password"
        className="w-1/2 border-2 border-amber-300 rounded-xl mt-5 mb-10 box-border pl-5 py-2"
        value={formData.password}
        onChange={handleChange}
      />

      <input type="submit" className="border-2 px-3 py-1 rounded-2xl mb-10 cursor-pointer"/>

      <Link to="/" className="text-blue-300 mb-10">SignedUp?</Link>

      {error && <h2 className="text-red-500">{error}</h2>}
    </form>
  );
}
