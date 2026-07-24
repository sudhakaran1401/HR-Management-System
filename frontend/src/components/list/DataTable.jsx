import React from "react";

const DataTable = ({
  columns = [],
  data = [],
  loading = false,
  emptyMessage = "No records found.",
}) => {
  if (loading) {
    return (
      <div className="text-center py-5">
        <div
          className="spinner-border text-primary"
          role="status"
        >
          <span className="visually-hidden">
            Loading...
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="table-responsive">

      <table className="table table-hover align-middle mb-0">

        {/* Header */}

        <thead>

          <tr>

            {columns.map((column) => (
              <th
                key={column.key}
                className="text-nowrap fw-semibold"
                style={{
                  width: column.width || "auto",
                }}
              >
                {column.title}
              </th>
            ))}

          </tr>

        </thead>

        {/* Body */}

        <tbody>

          {data.length === 0 ? (
            <tr>

              <td
                colSpan={columns.length}
                className="text-center py-5"
              >
                {emptyMessage}
              </td>

            </tr>
          ) : (

            data.map((row, index) => (

              <tr key={row.id ?? index}>

                {columns.map((column) => (

                  <td
                    key={column.key}
                    className="table-body-cell"
                  >
                    {column.render
                      ? column.render(row)
                      : row[column.key] ?? "-"}
                  </td>

                ))}

              </tr>

            ))

          )}

        </tbody>

      </table>

    </div>
  );
};

export default DataTable;