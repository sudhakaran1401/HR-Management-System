import React from "react";

const SummaryCards = ({
  cards = [],
  twoColumns = cards.length > 3,
}) => {
  return (
    <div className="row g-3 h-100">
      {cards.map((card, index) => (
        <div
          key={index}
          className={
            twoColumns
              ? "col-6"
              : cards.length === 4
              ? "col-lg-3 col-md-6"
              : "col-12"
          }
        >
          <div
            className="card summary-card shadow-sm border-0 h-100"
            style={{ "--summary-color": card.color || "#0d6efd" }}
          >
            <div className="card-body d-flex flex-column justify-content-center py-3">

              <h6 className="text-body-secondary mb-2">
                {card.title}
              </h6>

              <h4 className="summary-card-value fw-bold mb-1">
                {card.value}
              </h4>

              {card.subtitle && (
                <small className="text-body-secondary">
                  {card.subtitle}
                </small>
              )}

            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default SummaryCards;