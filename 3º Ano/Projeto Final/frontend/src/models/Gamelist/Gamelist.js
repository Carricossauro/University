import React, { useEffect, useState } from "react";
import { getQuizzes } from "./API_gamelist";
import { confirmType } from "../../API_index";

export default function Gamelist({ authorRedirect, author, cookies }) {
    const [games, setGames] = useState([]);
    const [filteredGames, setFilteredGames] = useState([]);
    const [searchText, setSearchText] = useState("");

    const redirect = (page) => {
        window.location.href = page;
    };

    const minAge = (quiz) => {
        let min = 0;
        for (var questionIndex in quiz.questions) {
            if (quiz.questions[questionIndex].minage > min)
                min = quiz.questions[questionIndex].minage;
        }
        return min;
    };

    const diff = (quiz) => {
        let total = 0;
        let count = 0;

        for (var questionIndex in quiz.questions) {
            count++;
            switch (quiz.questions[questionIndex].dificulty) {
                case "E":
                    total += 1;
                    break;
                case "M":
                    total += 2;
                    break;
                case "H":
                    total += 3;
                    break;
                default:
                    count -= 1;
                    break;
            }
        }

        const average = parseInt(total / count);

        if (average === 1) return "Easy";
        else if (average === 2) return "Medium";
        return "Hard";
    };

    const changeSearchText = (e) => {
        const text = e.target.value;
        setSearchText(text);
        console.log(games);

        if (text) {
            const texts = text.split(" ");
            let regs = [];
            for (var t in texts)
                if (texts[t] !== "") regs.push(new RegExp(`.*${texts[t]}.*`));

            var newGames = [];
            for (var game in games) {
                for (var i in regs) {
                    if (
                        regs[i].test(games[game].title) ||
                        regs[i].test(games[game].author)
                    ) {
                        newGames.push(games[game]);
                    }
                }
            }

            setFilteredGames(newGames);
        } else setFilteredGames(games);
    };

    useEffect(() => {
        async function effect() {
            const data = await getQuizzes(cookies);

            if (author) {
                try {
                    const token = cookies["access_token"];
                    const username = cookies["username"];

                    const response = await confirmType(username, token, true);

                    if (!response) throw new Error();
                } catch (e) {
                    redirect("/");
                }

                let newData = [];
                for (var game in data)
                    if (data[game].author === author) newData.push(data[game]);
                setGames(newData);
                setFilteredGames(newData);
            } else {
                setGames(data);
                setFilteredGames(data);
            }
        }
        effect();
    }, []);

    return (
        <>
            <div className="w-4/5 m-auto mt-28 pt-3">
                <div className="relative z-20 flex flex-col justify-center h-full px-3 mx-auto flex-center">
                    <div className="relative items-center pl-1 flex w-full lg:max-w-68 sm:pr-2 sm:ml-0">
                        <div className="container relative left-0 z-50 flex w-3/4 h-auto h-full">
                            <div className="relative flex items-center w-full lg:w-64 h-full group">
                                <svg
                                    className="absolute left-0 z-20 hidden w-4 h-4 ml-4 text-gray-500 pointer-events-none fill-current group-hover:text-gray-400 sm:block"
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 20 20"
                                >
                                    <path d="M12.9 14.32a8 8 0 1 1 1.41-1.41l5.35 5.33-1.42 1.42-5.33-5.34zM8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"></path>
                                </svg>
                                <input
                                    type="text"
                                    className="block w-full py-1.5 pl-10 pr-4 leading-normal rounded-2xl focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500 ring-opacity-90 bg-gray-100  text-gray-400 aa-input"
                                    placeholder="Search"
                                    value={searchText}
                                    onChange={(e) => changeSearchText(e)}
                                />
                            </div>
                        </div>
                    </div>
                </div>

                <div className="h-[640px] overflow-scroll rounded-lg shadow-xl mt-8">
                    <table className="w-full ">
                        <thead className="sticky top-0">
                            <tr className="">
                                <th className="px-4 py-4 text-left bg-blue-900 text-white text-sm font-medium w-1/3 text-center rounded-tl-lg">
                                    Title
                                </th>
                                <th className="px-4 py-4 text-left bg-blue-900 text-white text-sm font-medium w-1/3 text-center">
                                    Author
                                </th>
                                <th className="px-4 py-4 text-left bg-blue-900 text-white text-sm font-medium text-center">
                                    Difficulty
                                </th>
                                <th className="px-4 py-4 text-left bg-blue-900 text-white text-sm font-medium text-center">
                                    Minimum Age
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredGames.map((quiz, index) => {
                                return (
                                    <tr
                                        className={`border-gray-200 even:bg-gray-200 cursor-pointer`}
                                        id={index}
                                        key={index}
                                        onClick={() => {
                                            redirect(
                                                `/${
                                                    authorRedirect
                                                        ? "Author"
                                                        : "Player"
                                                }/Game/${quiz.id}`
                                            );
                                        }}
                                    >
                                        <td className="px-4 py-8 border-t border-b border-gray-200 text-sm text-center">
                                            {quiz.title}
                                        </td>
                                        <td className="px-4 py-8 border-t border-b border-gray-200 text-sm text-center">
                                            {quiz.author}
                                        </td>
                                        <td className="px-4 py-8 border-t border-b border-gray-200 text-sm text-center">
                                            {diff(quiz)}
                                        </td>
                                        <td className="px-4 py-8 border-t border-b border-gray-200 text-sm text-center">
                                            {minAge(quiz)}
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>
        </>
    );
}
