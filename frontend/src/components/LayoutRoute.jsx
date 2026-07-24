import MainLayout from "../layouts/MainLayout";
import ProtectedRoute from "./ProtectedRoute";

function LayoutRoute({ children }) {
  return (
    <ProtectedRoute>
      <MainLayout>
        {children}
      </MainLayout>
    </ProtectedRoute>
  );
}

export default LayoutRoute;