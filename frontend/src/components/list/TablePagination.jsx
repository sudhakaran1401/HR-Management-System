import React from "react";

const TablePagination = ({ table }) => {
  const {
    page,
    rowsPerPage,
    totalRows,
    onRowsChange,
    onPrev,
    onNext,
  } = table;

  const start =
    totalRows === 0
      ? 0
      : (page - 1) * rowsPerPage + 1;

  const end = Math.min(
    page * rowsPerPage,
    totalRows
  );

  return (
    <div className="d-flex justify-content-between gap-3 m-3">

      <div className="d-flex align-items-center">

        <span className="me-2 fw-semibold">
          Rows:
        </span>

        <select
          className="form-select form-select-sm rows-select"
          value={rowsPerPage}
          onChange={(e) =>
            onRowsChange(Number(e.target.value))
          }
        >
          <option value={5}>5</option>
          <option value={10}>10</option>
          <option value={20}>20</option>
          <option value={25}>25</option>
        </select>

      </div>

      <div className="text-body-secondary">
        {start}-{end} of {totalRows}
      </div>

      <div>

        <button
          className="btn btn-primary btn-sm me-2"
          disabled={page === 1}
          onClick={onPrev}
        >
          ← Prev
        </button>

        <button
          className="btn btn-primary btn-sm"
          disabled={end >= totalRows}
          onClick={onNext}
        >
          Next →
        </button>

      </div>

    </div>
  );
};

export default TablePagination;