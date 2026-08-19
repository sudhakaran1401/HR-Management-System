import { useEffect, useState } from "react";

function ThemeToggle() {
  const [dark, setDark] = useState(() => {
    return localStorage.getItem("theme") === "dark";
  });

  useEffect(() => {
    document.body.classList.toggle("dark-mode", dark);

    // Notify components on theme change
    window.dispatchEvent(new Event("themeChanged"));
  }, [dark]);

  const toggleTheme = () => {
    const nextTheme = !dark;

    setDark(nextTheme);

    document.body.classList.toggle("dark-mode", nextTheme);

    localStorage.setItem(
      "theme",
      nextTheme ? "dark" : "light"
    );

    // Notify charts and other components
    window.dispatchEvent(new Event("themeChanged"));
  };

  return (
    <div className="theme-toggle d-flex align-items-center">
      <i className="bi bi-sun-fill text-warning me-2"></i>

      <label className="switch">
        <input
          type="checkbox"
          checked={dark}
          onChange={toggleTheme}
        />

        <span className="slider round"></span>
      </label>

      <i className="bi bi-moon-fill text-light ms-2"></i>
    </div>
  );
}

export default ThemeToggle;