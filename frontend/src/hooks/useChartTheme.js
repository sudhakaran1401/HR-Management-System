import { useEffect, useState } from "react";

const useChartTheme = () => {
  const [dark, setDark] = useState(
    document.body.classList.contains("dark-mode")
  );

  useEffect(() => {
    const updateTheme = () => {
      setDark(
        document.body.classList.contains("dark-mode")
      );
    };

    window.addEventListener(
      "themeChanged",
      updateTheme
    );

    return () =>
      window.removeEventListener(
        "themeChanged",
        updateTheme
      );
  }, []);

  return {
    dark,
    textColor: dark ? "#ffffff" : "#212529",
    gridColor: dark ? "#3d3d3d" : "#e9ecef",
  };
};

export default useChartTheme;