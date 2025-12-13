import React from "react";
import { useTheme } from "../context/ThemeContext";

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="px-3 py-1 rounded border text-sm
                 bg-gray-800 text-white dark:bg-gray-200 dark:text-black 
                 transition-colors duration-300"
    >
      {theme === "dark" ? "Light Mode" : "Dark Mode"}
    </button>
  );
}
