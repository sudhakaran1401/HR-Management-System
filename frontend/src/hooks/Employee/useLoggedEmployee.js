const useLoggedEmployee = () => {
  return JSON.parse(
    localStorage.getItem("employee")
  );
};

export default useLoggedEmployee;