import { React, useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import NavBar from "./models/NavBar/NavBar";
import SignUp from "./models/SignUp/SignUp";
import Login from "./models/Login/Login";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Player from "./models/Player/Player";
import Author from "./models/Author/Author";
import About from "./models/About/About";
import Contact from "./models/Contact/Contact";
import Landing from "./models/Landing/Landing";
import { CookiesProvider, useCookies } from "react-cookie";

const Index = () => {
    const [size, setSize] = useState(window.innerWidth);
    const [showNavBar, setShowNavBar] = useState(true);
    const [isAuthor, setIsAuthor] = useState(false);
    const [cookies, setCookie, removeCookie] = useCookies([]);

    const checkSize = () => {
        setSize(window.innerWidth);
    };

    useEffect(() => {
        window.addEventListener("resize", checkSize);
        return () => {
            window.removeEventListener("resize", checkSize);
        };
    }, []);

    return (
        <div>
            <Router>
                {showNavBar && <NavBar size={size} />}
                <Routes>
                    <Route
                        path="/Player/Game/:gameid"
                        element={
                            <Player
                                setShowNavBar={setShowNavBar}
                                size={size}
                                game={true}
                            />
                        }
                    ></Route>
                    <Route
                        path="/Player/:playerPath"
                        element={
                            <Player
                                setShowNavBar={setShowNavBar}
                                size={size}
                                game={false}
                                cookies={cookies}
                                setCookie={setCookie}
                                removeCookie={removeCookie}
                            />
                        }
                    ></Route>
                    <Route
                        path="/Author/:authorPath"
                        element={
                            <Author setShowNavBar={setShowNavBar} size={size} />
                        }
                    ></Route>
                    <Route
                        path="/Login"
                        element={
                            <Login
                                setShowNavBar={setShowNavBar}
                                size={size}
                                setIsAuthor={setIsAuthor}
                                isAuthor={isAuthor}
                                cookies={cookies}
                                setCookie={setCookie}
                                removeCookie={removeCookie}
                            />
                        }
                    ></Route>
                    <Route
                        path="/SignUp"
                        element={
                            <SignUp
                                setShowNavBar={setShowNavBar}
                                size={size}
                                setIsAuthor={setIsAuthor}
                                isAuthor={isAuthor}
                            />
                        }
                    ></Route>
                    <Route
                        path="/Player"
                        element={
                            <Player
                                setShowNavBar={setShowNavBar}
                                size={size}
                                game={false}
                            />
                        }
                    ></Route>
                    <Route
                        path="/Author"
                        element={
                            <Author setShowNavBar={setShowNavBar} size={size} />
                        }
                    ></Route>
                    <Route path="/About" element={<About />}></Route>
                    <Route path="/Contact" element={<Contact />}></Route>
                    <Route path="/" element={<Landing />}></Route>
                </Routes>
            </Router>
        </div>
    );
};

const container = document.getElementById("root");
const root = createRoot(container);
root.render(
    <>
        <CookiesProvider>
            <Index />
        </CookiesProvider>
    </>
);
