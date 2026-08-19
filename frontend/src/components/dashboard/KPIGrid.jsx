const KPIGrid = ({ cards = [] }) => {
  return (
    <div className="row">
      {cards.map((card, index) => {
        const Component = card.component;

        return (
          <Component
            key={card.key || card.title || index}
            {...card.props}
          />
        );
      })}
    </div>
  );
};

export default KPIGrid;