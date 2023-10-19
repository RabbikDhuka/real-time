// React UI code

import React, { useState, useEffect } from "react";
import { useQuery } from "@apollo/client";

const STOCK_QUERY = gql`
  query stocks {
    stocks {
      ticker
      name
      price
    }
  }
`;

const StockList = () => {
  const [stocks, setStocks] = useState([]);

  const { loading, error, data } = useQuery(STOCK_QUERY);

  useEffect(() => {
    if (data) {
      setStocks(data.stocks);
    }
  }, [data]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <ul>
      {stocks.map((stock) => (
        <li key={stock.ticker}>
          {stock.ticker} - {stock.name}
          <br />
          Price: ${stock.price}
        </li>
      ))}
    </ul>
  );
};

export default StockList;
