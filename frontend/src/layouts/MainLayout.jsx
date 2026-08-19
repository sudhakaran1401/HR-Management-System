import Navbar from "../components/Navbar";

function MainLayout({ children }) {
  return (
    <>
      <Navbar />
      <div className="container-fluid mt-4">
        {children}
      </div>
    </>
  );
}

export default MainLayout;