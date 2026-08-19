import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function useCrudForm({
  createFn,
  updateFn,
  id,
  redirectPath,
  successCreate = "Created successfully.",
  successUpdate = "Updated successfully.",
}) {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const submit = async (payload) => {
    try {
      setLoading(true);

      if (id) {
        await updateFn(id, payload);
      } else {
        await createFn(payload);
      }

      navigate(redirectPath, {
        state: {
          alert: {
            type: "success",
            message: id
              ? successUpdate
              : successCreate,
          },
        },
      });

      return true;

    } catch (error) {
      console.error(error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    submit,
  };
}