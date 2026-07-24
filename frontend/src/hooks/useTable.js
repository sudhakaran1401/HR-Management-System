import { useEffect, useMemo, useState } from "react";

const useTable = (data = [], dependencies = []) => {
  const [page, setPage] = useState(1);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  useEffect(() => {
    setPage(1);
  }, [rowsPerPage, ...dependencies]);

  const totalRows = data.length;

  const totalPages = Math.max(
    1,
    Math.ceil(totalRows / rowsPerPage)
  );

  const paginatedData = useMemo(() => {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    return data.slice(start, end);
  }, [data, page, rowsPerPage]);

  const onRowsChange = (rows) => {
    setRowsPerPage(Number(rows));
    setPage(1);
  };

  const onPrev = () => {
    setPage((prev) => Math.max(prev - 1, 1));
  };

  const onNext = () => {
    setPage((prev) =>
      Math.min(prev + 1, totalPages)
    );
  };

  return {
    page,
    rowsPerPage,
    totalRows,
    totalPages,
    paginatedData,

    setPage,
    setRowsPerPage,

    onRowsChange,
    onPrev,
    onNext,
  };
};

export default useTable;