// src/components/Results.js

import React, { useEffect, useState } from "react";
import axios from "axios";
import { Box, Typography, List, ListItem, ListItemText } from "@mui/material";

function Results({ data, setEcoScore }) {
  const [ecoScoreData, setEcoScoreData] = useState(null);

  useEffect(() => {
    const calculateEcoScore = async () => {
      try {
        const response = await axios.post(
          `${process.env.REACT_APP_API_URL}/calculate-eco-score`,
          {
            items: data.identified_items,
          }
        );
        setEcoScoreData(response.data);
        setEcoScore(response.data);
      } catch (error) {
        console.error(error);
        alert("Error calculating eco-score");
      }
    };

    if (data && data.identified_items.length > 0) {
      calculateEcoScore();
    }
  }, [data, setEcoScore]);

  if (!data) return null;

  return (
    <Box marginTop="2rem">
      <Typography variant="h5" gutterBottom>
        Identified Items:
      </Typography>
      <List>
        {data.identified_items.map((item, index) => (
          <ListItem key={index}>
            <ListItemText
              primary={item}
              secondary={`Carbon Score: ${
                data.carbon_scores[item.toLowerCase()] || 0
              } kg CO₂`}
            />
          </ListItem>
        ))}
      </List>

      {ecoScoreData && (
        <>
          <Typography variant="h6" gutterBottom>
            Total Carbon Score: {ecoScoreData.total_carbon_score} kg CO₂
          </Typography>
          <Typography variant="h6" gutterBottom>
            Eco-Reward Points: {ecoScoreData.eco_reward_points}
          </Typography>
        </>
      )}
    </Box>
  );
}

export default Results;
