import { useCallback, useEffect, useMemo, useState } from "react";
import useTable from "./useTable";

const useListPage = ({
  loadData,
  dependencies = [],
  onError,
  transformData,
  filterData,
}) => {

  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);

      let data = await loadData();

      if (transformData) {
        data = transformData(data);
      }

      if (filterData) {
        data = filterData(data);
      }

      setRecords(data);

    } catch (error) {

      if (onError) {
        onError(error);
      } else {
        console.error(error);
      }

    } finally {
      setLoading(false);
    }
  }, [
    loadData,
    transformData,
    filterData,
    onError,
  ]);

  useEffect(() => {
  fetchData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, dependencies);

  const filteredRecords = useMemo(() => {

    if (!search) return records;

    const keyword = search.toLowerCase();

    return records.filter((record) =>
      JSON.stringify(record)
        .toLowerCase()
        .includes(keyword)
    );

  }, [records, search]);

  const table = useTable(filteredRecords, [search]);

  return {
    records,
    setRecords,

    loading,

    search,
    setSearch,

    table,

    reload: fetchData,
  };
};

export default useListPage;