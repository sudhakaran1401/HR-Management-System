import SearchBar from "../components/Searchbar";
import DataTable from "../components/list/DataTable";
import TablePagination from "../components/list/TablePagination";
import LayoutHeader from "../components/LayoutHeader";

const ModuleLayout = ({
  title,
  buttonText,
  onButtonClick,

  // Search
  searchPlaceholder = "Search...",
  search = "",
  onSearch,

  // Table
  columns = [],
  data = [],
  loading = false,

  // Table Hook
  table,
}) => {
  const actions = buttonText ? (
    <button
      className="btn btn-success btn-sm"
      onClick={onButtonClick}
    >
      {buttonText}
    </button>
  ) : null;

  return (
    <div className="container mt-4">

      <LayoutHeader
        title={title}
        actions={actions}
      />

      <div className="card shadow-sm border module-layout-card">

        <div className="card-body">

          <SearchBar
            placeholder={searchPlaceholder}
            value={search}
            onChange={onSearch}
          />

          <DataTable
            columns={columns}
            data={data}
            loading={loading}
          />

          <TablePagination table={table} />

        </div>

      </div>

    </div>
  );
};

export default ModuleLayout;