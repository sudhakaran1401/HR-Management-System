import React from "react";
import { Download } from "lucide-react";

const ExportButtons = ({
  onCSV,
  onPDF,
}) => {
  return (
    <div className="btn-group shadow-sm">

      {/* CSV */}

      <button
        className="btn btn-success btn-sm"
        onClick={onCSV}
      >
        CSV
      </button>

      {/* Icon */}

      <button
        className="btn btn-light btn-sm"
        disabled
      >
        <Download size={16} />
      </button>

      {/* PDF */}

      <button
        className="btn btn-danger btn-sm"
        onClick={onPDF}
      >
        PDF
      </button>

    </div>
  );
};

export default ExportButtons;