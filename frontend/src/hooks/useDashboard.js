import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import useAlert from "./useAlert";

const useDashboard = ({
  endpoint,
  initialData,
  hrPath = "/hr/dashboard",
  employeePath = "/me/dashboard",
}) => {
  const navigate = useNavigate();
  const { alert, showAlert, closeAlert } = useAlert();

  const [loading, setLoading] = useState(false);

  const [isHR, setIsHR] = useState(false);

  const [dashboardMode, setDashboardMode] = useState(
    localStorage.getItem("dashboard_mode") || "HR"
  );

  const [year, setYear] = useState("");
  const [month, setMonth] = useState("");
  const [day, setDay] = useState("");

  const [data, setData] = useState(initialData);

  useEffect(() => {
    const storedAlert = sessionStorage.getItem("alert");

    if (storedAlert) {
      const parsed = JSON.parse(storedAlert);

      showAlert(parsed.type, parsed.message);

      sessionStorage.removeItem("alert");
    }
  }, []);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const res = await api.get("/api/me/");

      setIsHR(res.data.is_hr);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchDashboard = async () => {
    try {
      if (!year) {
        showAlert("warning", "Please select Year.");
        return;
      }

      setLoading(true);

      let url = `${endpoint}?year=${year}`;

      if (month) url += `&month=${month}`;

      if (day) url += `&day=${day}`;

      const res = await api.get(url);

      setData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setYear("");
    setMonth("");
    setDay("");

    setData(initialData);
  };

  const handleRoleToggle = () => {
    const next =
      dashboardMode === "hr"
        ? "employee"
        : "hr";

    setDashboardMode(next);

    localStorage.setItem(
      "dashboard_mode",
      next
    );

    navigate(
      next === "hr"
        ? hrPath
        : employeePath
    );
  };

  return {
    loading,

    alert,
    showAlert,
    closeAlert,

    isHR,

    dashboardMode,

    data,

    year,
    month,
    day,

    setYear,
    setMonth,
    setDay,

    fetchDashboard,
    handleReset,
    handleRoleToggle,
  };
};

export default useDashboard;